"""Size optimisation used by every chapter build (print + screen PDF).
Pipeline:
 1. measure(page): DOM pass -> needed pixels of every <img> at its placed size (object-fit aware, max over uses)
 2. make_assets(): resample each image to target ppi (only downsample, never below floor),
    JPEG q~86 4:2:0 for opaque images, alpha-bled PNG for cutouts (so the later JPEG of the colour plane has no halo)
 3. rewrite_html(): point the HTML to the optimised copies
 4. postprocess(): pikepdf - Flate RGB images -> DCT (keeps the Flate soft mask), dedupe identical streams,
    strip XMP/metadata, linearize, object streams. Text/vector/fonts untouched (no Ghostscript).
"""
import os,re,io,hashlib,json
import numpy as np
from PIL import Image
import pikepdf
MEASURE_JS="""()=>{const m={};document.querySelectorAll('img').forEach(i=>{
 if(!i.naturalWidth)return;const w=i.clientWidth,h=i.clientHeight;if(!w||!h)return;
 const fit=getComputedStyle(i).objectFit;const sx=w/i.naturalWidth,sy=h/i.naturalHeight;
 const s=(fit=='cover')?Math.max(sx,sy):(fit=='contain'||fit=='scale-down')?Math.min(sx,sy):Math.max(sx,sy);
 const src=decodeURIComponent(i.getAttribute('src'));const r=s;            // css px per image px
 if(!m[src]||m[src]<r)m[src]=r});return m}"""
def has_alpha(im):
    if im.mode in('RGBA','LA') or (im.mode=='P' and 'transparency' in im.info):
        a=np.asarray(im.convert('RGBA'))[...,3];return a.min()<250
    return False
def bleed(rgba):
    """extend edge colours into fully transparent pixels so JPEG/scaling never mixes in the matte colour"""
    import cv2
    a=rgba[...,3].astype(np.float32)/255.;rgb=rgba[...,:3].astype(np.float32)
    w=(a>0.5).astype(np.float32);out=rgb.copy();todo=a<0.02
    filled=np.zeros(a.shape,bool)
    for s in (1.5,4,12,40,120):
        num=cv2.GaussianBlur(rgb*w[...,None],(0,0),s);den=cv2.GaussianBlur(w,(0,0),s)
        ok=todo&~filled&(den>0.03)
        out[ok]=num[ok]/den[ok,None];filled|=ok
    out[todo&~filled]=rgb[w>0].mean(0) if w.any() else 255
    return np.dstack([np.clip(out,0,255).astype(np.uint8),rgba[...,3]])
def make_assets(root,meas,outdir,ppi=320,floor=300,q=86,slack=1.03,log=None):
    """meas: src -> css px per image px. returns src->new relative path"""
    mp={};rep=[]
    for src,r in meas.items():
        p=os.path.join(root,src)
        if not os.path.isfile(p): continue
        im=Image.open(p);im.load();W,H=im.size
        cur=96/r                          # current ppi at placed size
        tgt=W*r*ppi/96                    # px width needed for target ppi
        scale=min(1.0,tgt/W) if cur>ppi*slack else 1.0
        nw,nh=max(1,round(W*scale)),max(1,round(H*scale))
        alpha=has_alpha(im)
        rel=os.path.splitext(src)[0]+('.png' if alpha else '.jpg');dst=os.path.join(outdir,rel)
        os.makedirs(os.path.dirname(dst),exist_ok=True)
        if alpha:
            a=im.convert('RGBA')
            if scale<1: a=a.resize((nw,nh),Image.LANCZOS)
            a=Image.fromarray(bleed(np.asarray(a)),'RGBA');a.save(dst,optimize=True)
        else:
            c=im.convert('RGB')
            if scale<1: c=c.resize((nw,nh),Image.LANCZOS)
            c.save(dst,quality=q,subsampling=2,optimize=True,progressive=False)
            if scale==1 and src.lower().endswith(('.jpg','.jpeg')) and os.path.getsize(dst)>os.path.getsize(p)*0.9:
                import shutil;shutil.copyfile(p,dst)   # not worth a re-encode
        newppi=cur/scale
        if newppi<floor-0.5: raise SystemExit(f'{src}: would drop to {newppi:.0f}ppi')
        mp[src]=os.path.relpath(dst,root);rep.append((src,W,H,round(cur),nw,nh,round(newppi),bool(alpha)))
    if log: json.dump(rep,open(log,'w'),indent=0)
    return mp
def rewrite_html(html,mp):
    for s,d in sorted(mp.items(),key=lambda x:-len(x[0])):
        html=html.replace(f'src="{s}"',f'src="{d}"')
    return html
def postprocess(src,dst,q=86,min_px=48):
    pdf=pikepdf.open(src);seen={};nconv=0;ndup=0
    for o in list(pdf.objects):
        if not isinstance(o,pikepdf.Stream) or str(o.get('/Subtype'))!='/Image': continue
        if str(o.get('/Filter'))=='/DCTDecode' or o.get('/ImageMask',False): continue
        csv=o.get('/ColorSpace')
        if isinstance(csv,pikepdf.Array) and str(csv[0])=='/ICCBased': ncomp=int(csv[1].get('/N',0))
        else: ncomp={'/DeviceRGB':3,'/DeviceGray':1}.get(str(csv),0)
        if ncomp!=3 or int(o.get('/BitsPerComponent',8))!=8: continue   # gray (soft masks) stay lossless
        w,h=int(o.Width),int(o.Height)
        if w<min_px or h<min_px: continue
        raw=o.read_bytes();im=Image.frombytes('RGB',(w,h),raw)
        b=io.BytesIO();im.save(b,'JPEG',quality=q,subsampling=2,optimize=True)
        if len(b.getvalue())<len(o.read_raw_bytes())*0.9:
            o.write(b.getvalue(),filter=pikepdf.Name.DCTDecode);
            for k in ('/DecodeParms',): 
                if k in o: del o[k]
            nconv+=1
    # dedupe identical image streams
    for page in pdf.pages:
        def walk(res):
            nonlocal ndup
            if '/XObject' not in res: return
            xo=res.XObject
            for k in list(xo.keys()):
                x=xo[k]
                if str(x.get('/Subtype'))=='/Image':
                    hsh=hashlib.md5(x.read_raw_bytes()+repr(sorted((kk,str(vv)) for kk,vv in x.items() if kk!='/SMask')).encode()+ (x.SMask.read_raw_bytes() if '/SMask' in x else b'')).hexdigest()
                    if hsh in seen and seen[hsh].objgen!=x.objgen: xo[k]=seen[hsh];ndup+=1
                    else: seen[hsh]=x
                elif str(x.get('/Subtype'))=='/Form' and '/Resources' in x: walk(x.Resources)
        walk(page.Resources)
    if '/Metadata' in pdf.Root: del pdf.Root['/Metadata']
    pdf.docinfo=pdf.make_indirect(pikepdf.Dictionary(Title=pikepdf.String('Vocabulario visual · Español')))
    pdf.remove_unreferenced_resources()
    pdf.save(dst,linearize=True,object_stream_mode=pikepdf.ObjectStreamMode.generate,compress_streams=True,recompress_flate=True)
    return nconv,ndup

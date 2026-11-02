import json,sys,os,re,shutil,asyncio,hashlib,html
sys.path.insert(0,'/workspace/trilingual/es/v6/_build')
from base_v6 import V3
from data_v6 import CH02,CH11
import edge_tts,subprocess
from PIL import Image
R='/workspace/trilingual/es/v6';W=f'{R}/web'
D3=json.load(open('/workspace/trilingual/es/ch01_bathroom_v3/data.json'));O=D3['order']
CUT11={'bus','taxi','ticket','suitcase','plane','bike','car','moto','lights','backpack','helmet'}
jobs={}
def aud(text,lang='es'):
    key=hashlib.md5((lang+text).encode()).hexdigest()[:10];fn=f'{lang}_{key}.mp3';jobs[fn]=(text,lang);return f'audio/{fn}'
# size-optimized web assets (standing rule): WebP 1x/2x fitted to the card box, lazy-loaded
BOX=(260,110);WQ=80
TTS=f'{R}/_build/tts_cache';os.makedirs(TTS,exist_ok=True);os.makedirs(f'{W}/img',exist_ok=True);os.makedirs(f'{W}/audio',exist_ok=True)
def img(src,name,alt=''):
    base=os.path.splitext(name)[0];im=Image.open(src);im.load()
    im=im.convert('RGBA') if (im.mode in('RGBA','LA','P') and 'A' in im.convert('RGBA').getbands() and im.convert('RGBA').getextrema()[3][0]<255) else im.convert('RGB')
    out=[]
    for k in (1,2):
        bw,bh=BOX[0]*k,BOX[1]*k;s=min(bw/im.width,bh/im.height,1.0)
        w,h=max(1,round(im.width*s)),max(1,round(im.height*s))
        fn=f'{base}_{k}x.webp';im.resize((w,h),Image.LANCZOS).save(f'{W}/img/{fn}','WEBP',quality=WQ,method=6)
        out.append((fn,w,h))
    (f1,w1,h1),(f2,_,_)=out
    return f'<img src="img/{f1}" srcset="img/{f1} 1x, img/{f2} 2x" width="{w1}" height="{h1}" loading="lazy" decoding="async" alt="{html.escape(alt)}">'
def card(im,es,g,p,en,ko,extra=''):
    a=aud(es);im=im.replace('alt=""',f'alt="{html.escape(en)}"')
    return f'<div class="card"><button class="pl" data-a="{a}" aria-label="play">▶</button><div class="im">{im}</div><div class="es">{es} <span class="g">{g}</span></div><div class="p">[{p}]</div><div class="t">{en} · {ko}</div>{extra}</div>'
def line(es,en,ko,lab=''):
    return f'<div class="ln"><button class="pl" data-a="{aud(es)}">▶</button><div><div class="es2">{lab}{es}</div><div class="t">{en} · {ko}</div></div></div>'
S=''
# ch01
c=''
for i in V3:
    ex=i.get('ex')
    extra=f'<div class="ex"><button class="pl s" data-a="{aud(ex[0])}">▶</button> {ex[0]}<br><span>{ex[2]}</span></div>' if ex else ''
    c+=card(img(f'{R}/ch01/img/t_{i["img"]}',f'ch01_{i["img"]}'),i['es'],i['g'],i['p'],i['en'],i['ko'],extra)
S+=f'<section id="ch01"><h2>01 · El baño <small>욕실 · Granada</small></h2><div class="grid">{c}</div>'
S+='<h3>§4 Bloques de palabras · 단어 블록</h3>'+''.join(line(t['es'],t['en'],t['ko']) for t in O['sent'])
S+='<h3>§5 ¿Dónde va «me»? · me의 자리</h3>'+''.join(line(es,where,ko) for es,where,ko in O['clitic'])
S+='<h3>§6 Sin sujeto · 주어 생략</h3>'+''.join(line(es,'',ko) for es,ko in O['subj'])
S+='<h3>§8 Ordena las palabras · 정답 듣기</h3>'+''.join(line(ans[0].upper()+ans[1:]+'.' if not ans.endswith('.') else ans,' / '.join(sc),ko) for sc,ans,ko in O['practice'])
S+='<h3>Escenas · 장면 문장</h3>'+''.join(line(es,en,ko) for es,en,ko in D3['scenes'])+'</section>'
# ch02
c=''.join(card(img(f'{R}/ch02/img/{k}.jpg',f'ch02_{k}.jpg'),es,g,p,en,ko) for (k,es,g,p,en,ko,*_) in CH02)
S+=f'<section id="ch02"><h2>02 · La cocina <small>부엌 · València</small></h2><div class="grid">{c}</div></section>'
c=''
for (k,es,g,p,en,ko,*_) in CH11:
    src=f'{R}/ch11/img/c_{k}.png' if k in CUT11 else f'{R}/ch11/img/{k}.jpg'
    c+=card(img(src,f'ch11_{os.path.basename(src)}'),es,g,p,en,ko)
S+=f'<section id="ch11"><h2>11 · El transporte <small>교통 · Madrid</small></h2><div class="grid">{c}</div></section>'
CSS='''body{margin:0;background:#f3ecdf;color:#1f1b17;font-family:system-ui,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}
header{position:sticky;top:0;background:#1f1b17;color:#f6efdc;padding:10px 16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;z-index:2}
header b{font-family:Georgia,serif;font-style:italic;font-size:20px}header a{color:#f6c38a;text-decoration:none;font-size:14px}
header label{font-size:13px;margin-left:auto}
main{max-width:1100px;margin:0 auto;padding:12px 16px 60px}h2{font-family:Georgia,serif;font-style:italic;font-weight:400;font-size:30px;border-bottom:2px solid #a4533a;margin:28px 0 12px}
h2 small{font-style:normal;font-size:15px;color:#6b5e50}h3{font-size:16px;color:#a4533a;margin:22px 0 8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}
.card{position:relative;background:#fffdf8;border-radius:6px;padding:10px;box-shadow:0 1px 3px rgba(0,0,0,.12)}
.im{height:110px;display:flex;align-items:center;justify-content:center}.im img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain}
.es{font-family:Georgia,serif;font-weight:700;font-size:17px;margin-top:6px}.g{font:500 11px system-ui;color:#a4533a}
.p{font-size:13px;color:#3e5a86}.p b{color:#1f1b17}.t{font-size:12px;color:#6b5e50}
.ex{font-size:12px;margin-top:6px;border-top:1px dashed #d8cbb5;padding-top:5px}.ex span{color:#6b5e50}
.pl{border:0;background:#a4533a;color:#fff;border-radius:50%;width:30px;height:30px;cursor:pointer;font-size:12px}
.card>.pl{position:absolute;right:8px;top:8px}.pl.s{width:22px;height:22px;font-size:9px;background:#3e5a86}
.ln{display:flex;gap:10px;align-items:center;background:#fffdf8;border-radius:6px;padding:8px 10px;margin-bottom:6px}.es2{font-family:Georgia,serif;font-size:16px}
.pl.on{background:#1f1b17}'''
JS='''let a=new Audio(),rate=1;document.querySelectorAll('.pl').forEach(b=>b.onclick=()=>{document.querySelectorAll('.pl.on').forEach(x=>x.classList.remove('on'));b.classList.add('on');a.src=b.dataset.a;a.preload='none';a.playbackRate=rate;a.play();a.onended=()=>b.classList.remove('on')});
document.getElementById('slow').onchange=e=>{rate=e.target.checked?0.75:1};'''
H=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vocabulario visual · v6</title><style>{CSS}</style></head><body>
<header><b>Vocabulario visual</b><a href="#ch01">01 El baño</a><a href="#ch02">02 La cocina</a><a href="#ch11">11 El transporte</a><label><input type="checkbox" id="slow"> 천천히 (0.75×)</label></header>
<main><p style="font-size:13px;color:#6b5e50">▶를 누르면 스페인어(스페인 표준 발음, 음성 합성)로 들려요. [ ] 안은 한글 발음, <b>굵은 글자</b>가 강세예요. 사진 출처는 PDF의 Créditos 페이지에 있어요.</p>{S}</main><script>{JS}</script></body></html>'''
open(f'{W}/index.html','w').write(H)
async def gen():
    sem=asyncio.Semaphore(4)
    async def one(fn,t,l):
        p=f'{TTS}/{fn}'
        if os.path.exists(p) and os.path.getsize(p)>500: return
        async with sem:
            for k in range(3):
                try:
                    await edge_tts.Communicate(t,'es-ES-ElviraNeural' if l=='es' else 'en-US-AriaNeural',rate='-5%').save(p);return
                except Exception as e: err=e;await asyncio.sleep(2)
            print('FAIL',fn,t,err)
    await asyncio.gather(*[one(fn,t,l) for fn,(t,l) in jobs.items()])
asyncio.run(gen())
# speech audio: mono 24 kHz MP3 32 kbps (TTS masters stay in _build/tts_cache)
for fn in jobs:
    src,dst=f'{TTS}/{fn}',f'{W}/audio/{fn}'
    if os.path.exists(src): subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-ac','1','-ar','24000','-c:a','libmp3lame','-b:a','32k','-map_metadata','-1',dst],check=True)
print('audio jobs',len(jobs),'files',len(os.listdir(f'{W}/audio')))

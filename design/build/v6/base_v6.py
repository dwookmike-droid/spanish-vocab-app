import json,random,sys
sys.path.insert(0,'/workspace/trilingual/es/v6/_build')
from data_v6 import CH02,CH11,NOTE02,NOTE11
R='/workspace/trilingual/es/v6'
V3=json.load(open('/workspace/trilingual/es/ch01_bathroom_v3/data.json'))['items']
GL={'f':'f','m':'m','fpl':'f pl','mpl':'m pl'}
def ff(n,f,w=400,s='normal'): return f"@font-face{{font-family:'{n}';src:url(fonts/{f});font-weight:{w};font-style:{s}}}\n"
def lab(es,g,p,en,ko):
    return (f'<div class="lab"><div class="l1"><span class="w">{es}</span><span class="g g{g[0]}">{GL[g]}</span></div>'
            f'<div class="lp"><span class="pr">[{p}]</span></div><div class="l2"><span class="en">{en}</span> · <span class="ko">{ko}</span></div></div>')
def tape(w=30,h=9,seed=0,col='rgba(226,214,180,.74)',stripes=None):
    random.seed(seed*31+w)
    pts=[(0,0)]+[(w*k/6+random.uniform(-.8,.8),random.uniform(-.5,.5)) for k in range(1,6)]+[(w,0)]+[(w+random.uniform(-.9,.9),h*k/5) for k in range(1,5)]+[(w,h)]+[(w*k/6+random.uniform(-.8,.8),h+random.uniform(-.5,.5)) for k in range(5,0,-1)]+[(0,h)]+[(random.uniform(-.9,.9),h*k/5) for k in range(4,0,-1)]
    p=' '.join(f'{x:.2f},{y:.2f}' for x,y in pts);cid=f'tc{seed}{w}'.replace('.','')
    st=''
    if stripes:  # vector stripes clipped by tape polygon (clipPath stays vector)
        st=f'<clipPath id="{cid}"><polygon points="{p}"/></clipPath><g clip-path="url(#{cid})">'+''.join(f'<rect x="{x}" y="-2" width="2" height="{h+4}" fill="{stripes}" transform="skewX(-30)"/>' for x in range(-4,int(w)+8,4))+'</g>'
    return f'<svg class="tape" style="width:{w}mm;height:{h}mm" viewBox="-1 -1 {w+2} {h+2}"><polygon points="{p}" fill="{col}"/>{st}<polygon points="{p}" fill="none" stroke="rgba(150,130,90,.25)" stroke-width=".15"/></svg>'
_pm=[0]
def postmark(txt,center,col,op=.8,fs=6,waves=True):
    _pm[0]+=1;i=_pm[0]
    wv='<path d="M60 14 q8 -4 16 0 t16 0 M60 24 q8 -4 16 0 t16 0 M60 34 q8 -4 16 0 t16 0 M60 44 q8 -4 16 0 t16 0"/>' if waves else ''
    return f'''<svg viewBox="0 0 100 60" class="pmsvg"><g fill="none" stroke="{col}" stroke-width="1.3" opacity="{op}"><circle cx="30" cy="30" r="26"/><circle cx="30" cy="30" r="17"/>{wv}</g>
<defs><path id="arc{i}" d="M30 30 m-21.5 0 a21.5 21.5 0 1 1 43 0 a21.5 21.5 0 1 1 -43 0"/></defs>
<text font-family="Special Elite" font-size="6.2" fill="{col}" opacity="{op}" letter-spacing="1.1"><textPath href="#arc{i}">{txt}</textPath></text>
<text x="30" y="32.5" text-anchor="middle" font-family="Special Elite" font-size="{fs}" fill="{col}" opacity="{op}">{center}</text></svg>'''
def rectstamp(l1,l2,l3,col,op=.75,w=46,h=24,icon=''):
    return f'''<svg viewBox="0 0 {w} {h}" style="width:{w}mm;height:{h}mm" class="rs"><g fill="none" stroke="{col}" opacity="{op}"><rect x=".8" y=".8" width="{w-1.6}" height="{h-1.6}" rx="2.4" stroke-width=".9"/><rect x="2.4" y="2.4" width="{w-4.8}" height="{h-4.8}" rx="1.4" stroke-width=".35"/></g>
<g fill="{col}" opacity="{op}" font-family="Special Elite" text-anchor="middle"><text x="{w/2}" y="{h*.34}" font-size="3.4" letter-spacing=".6">{l1}</text><text x="{w/2}" y="{h*.62}" font-size="5.6" letter-spacing=".4">{l2}</text><text x="{w/2}" y="{h*.84}" font-size="2.9" letter-spacing=".5">{l3}</text></g>{icon}</svg>'''
PLANE='<path d="M0 0" />'
def plane_icon(x,y,s,col,op):  # simple vector airplane
    return f'<g transform="translate({x},{y}) scale({s})" fill="{col}" opacity="{op}"><path d="M10 0 L11.2 0 L12 7 L19 10 L19 11.6 L12 10.2 L11.6 15 L13.6 16.6 L13.6 17.6 L10.6 17 L7.6 17.6 L7.6 16.6 L9.6 15 L9.2 10.2 L2.2 11.6 L2.2 10 L9.2 7 Z" transform="rotate(90 10.6 9)"/></g>'
def oval_stamp(top,mid,bot,col,op=.75):
    return f'''<svg viewBox="0 0 60 36" class="os"><g fill="none" stroke="{col}" opacity="{op}"><ellipse cx="30" cy="18" rx="28.5" ry="16.5" stroke-width=".9"/><ellipse cx="30" cy="18" rx="25.5" ry="13.8" stroke-width=".35"/><line x1="9" y1="21.5" x2="51" y2="21.5" stroke-width=".35"/><line x1="9" y1="13" x2="51" y2="13" stroke-width=".35"/></g>
<g fill="{col}" opacity="{op}" font-family="Special Elite" text-anchor="middle"><text x="30" y="11.2" font-size="4.4" letter-spacing=".4">{top}</text><text x="30" y="20" font-size="6">{mid}</text><text x="30" y="28.4" font-size="4.4" letter-spacing=".4">{bot}</text></g></svg>'''
FONTS=(ff('Bodoni D','BodoniModa-Display500.ttf',500)+ff('Bodoni D','BodoniModa-DisplayItalic.ttf',400,'italic')+ff('Bodoni T','BodoniModa-Text600.ttf',600)
 +ff('Jost','Jost-400.ttf',400)+ff('Jost','Jost-500.ttf',500)+ff('Gowun','GowunBatang-Regular.ttf',400)+ff('Gowun','GowunBatang-Bold.ttf',700)
 +ff('Caveat','Caveat-500.ttf',500)+ff('Caveat','Caveat-700.ttf',700)+ff('Pen','NanumPenScript-Regular.ttf')+ff('Special Elite','SpecialElite-Regular.ttf'))
CSS=FONTS+"""
@page{size:A4;margin:0}*{box-sizing:border-box;margin:0;padding:0}html,body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Jost','Gowun';color:#1f1b17}img{display:block}.pr,.ko,.lab{word-break:keep-all}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;break-after:page}
.ko,.pr{font-family:'Gowun'}
/* ===== backbone: opener ===== */
.op .ph{position:absolute;inset:0;width:210mm;height:297mm;object-fit:cover}
.op .grad{position:absolute;left:0;right:0;bottom:0;height:128mm;background:linear-gradient(rgba(18,12,7,0),rgba(18,12,7,.55) 45%,rgba(18,12,7,.86))}
.op .gradt{position:absolute;left:0;right:0;top:0;height:36mm;background:linear-gradient(rgba(18,12,7,.55),rgba(18,12,7,0))}
.op .top{position:absolute;top:11mm;left:14mm;right:14mm;color:#fff;font:500 7.5pt 'Jost';letter-spacing:.28em;text-transform:uppercase}
.op .badge{position:absolute;right:9mm;top:6mm}
.op .tb{position:absolute;left:14mm;right:14mm;bottom:15mm;color:#fff}
.op .kick{font:500 8pt 'Jost';letter-spacing:.3em;text-transform:uppercase;opacity:.92}
.op h1{font:400 italic 88pt/0.95 'Bodoni D';margin:3mm 0 0 -1.5mm}
.op .sub{font:400 italic 15pt 'Bodoni D';margin-top:2mm}.op .sub .ko{font-style:normal;font-size:13pt}
.op .hand{font:500 17pt 'Caveat';margin-top:2.5mm;transform:rotate(-1.5deg);transform-origin:left}
.op .rule{height:.3mm;background:rgba(255,255,255,.7);margin:5mm 0 3.2mm}
.op .cap{display:flex;justify-content:space-between;font:400 8pt/1.45 'Jost';letter-spacing:.04em}
.op .cap b{font-weight:500;letter-spacing:.2em;text-transform:uppercase}
.op .chip{display:inline-block;margin-left:2mm;padding:.3mm 1.6mm;border-radius:.6mm;font:500 7pt 'Jost';letter-spacing:.14em;vertical-align:1px}
.op .cred{position:absolute;right:4mm;top:150mm;transform:rotate(90deg);transform-origin:right top;color:rgba(255,255,255,.92);font:400 7pt 'Jost';letter-spacing:.06em;white-space:nowrap}
/* ===== backbone: word page ===== */
.paper{position:absolute;inset:0;width:210mm;height:297mm}
.hd{position:absolute;left:15mm;top:14mm;width:98mm}
.kick2{font:500 7.5pt 'Jost';letter-spacing:.3em;text-transform:uppercase;color:#6b5e50}
h2{font:400 italic 46pt/1 'Bodoni D';margin:3mm 0 1.5mm -0.8mm;color:#1f1b17}
.sub2{font:400 italic 12.5pt 'Bodoni D'}.sub2 .ko{font-style:normal;font-size:11pt}
.legend{margin-top:3.5mm;font:400 7.5pt/1.5 'Jost';color:#5a4f44}.legend b{font-family:'Gowun';font-weight:700;color:#1f1b17}
.hand{font-family:'Caveat','Pen'}.pen{font-family:'Pen'}
.abs{position:absolute}
.tape{position:absolute;overflow:visible}
.print{position:absolute;background:#fdfbf6;padding:2.6mm;box-shadow:.5mm .7mm 0 rgba(60,40,20,.14)}
.pol{position:absolute;background:#fdfcf8;padding:2.4mm 2.4mm 0;box-shadow:.5mm .7mm 0 rgba(60,40,20,.14)}
.pol .c{height:8mm;display:flex;align-items:center;justify-content:center;font:500 11pt 'Caveat';color:#3a2a22}
.pmsvg{width:100%;height:100%}
.card{position:absolute;background:#fdfaf3;box-shadow:.4mm .6mm 0 rgba(60,40,20,.13)}
.hero{padding:3mm 3mm 2.2mm;width:44mm}
.tag{padding:2.4mm 2mm 1.8mm;width:29mm}
.im{display:flex;align-items:center;justify-content:center;position:relative}
.hero .im{height:31mm}.tag .im{height:19mm}
.im img.ph{width:100%;height:100%;object-fit:cover}
.im img.pp{height:100%;width:auto}
.card>.tape{left:50%;top:-3mm;margin-left:-9mm}
.card .n{position:absolute;left:2.2mm;top:1.1mm;font:700 11pt 'Caveat';color:var(--acc);z-index:3}
.tag .n{font-size:10pt;left:1.8mm;top:.5mm}
.card .note{position:absolute;right:1.6mm;top:1.4mm;font:500 10.5pt/.95 'Caveat';color:var(--note);transform:rotate(3deg);text-align:right;width:22mm;z-index:3}
.tag .note{width:14mm;font-size:9.5pt;right:1mm;top:4.5mm}
.ph-note .note{background:rgba(253,250,243,.88);padding:.6mm 1mm;border-radius:.6mm;width:auto;max-width:24mm}
.lab{margin-top:1.8mm;line-height:1.25}
.lab .w{font:600 10.5pt 'Bodoni T','Gowun'}.tag .lab .w{font-size:8.6pt}
.lab .g{font:500 7.5pt 'Jost';margin-left:1.4mm;letter-spacing:.03em}.lab .gf{color:#a4533a}.lab .gm{color:#3e5a86}
.lab .pr{font-size:7.5pt;color:#4a4038}.lab .pr b{font-weight:700;color:#1f1b17}
.lab .l2{font:400 7.5pt 'Jost';color:#3b342d}.lab .l2 .ko{color:#1f1b17}
.tag .lab{margin-top:1.2mm;line-height:1.2}.tag .lab .pr,.tag .lab .l2{font-size:7pt}
.folio{position:absolute;left:15mm;right:15mm;bottom:5mm;display:flex;justify-content:space-between;font:400 7pt 'Jost';letter-spacing:.2em;text-transform:uppercase;color:#6b5e50}
.folio .sk{color:var(--acc)}
/* ===== skin: museo / alhambra (ch01) ===== */
.s-museo .hero{padding-bottom:2.2mm;padding-top:3.4mm}.s-museo .hero .im{height:30.5mm}.s-museo .hero .n{display:none}
.s-museo .im img.cut{max-width:100%;max-height:100%;object-fit:contain}
.s-museo .im img.rot{max-width:none;max-height:none;position:absolute;left:50%;top:50%}
.s-museo .mus{display:flex;align-items:center;gap:1.6mm;margin-top:1.4mm;font:500 7pt 'Jost';letter-spacing:.22em;color:var(--acc)}
.s-museo .mus .ln{flex:1;height:.2mm;background:rgba(120,80,50,.35)}
.s-museo .tag{background:#f1e6cc;border-radius:0 0 1mm 1mm}
.s-museo .tag .hole{position:absolute;left:50%;top:1.6mm;width:2.2mm;height:2.2mm;margin-left:-1.1mm;border-radius:50%;background:#e6dcc4;border:.25mm solid #b9a57e}
.s-museo .tag .im{height:17.5mm}.s-museo .tag.nt .im{justify-content:flex-start}.s-museo .tag.nt .im img{max-width:62%}
.wall{position:absolute;background:#fbfaf6;padding:2.4mm 3mm;box-shadow:.3mm .5mm 0 rgba(60,40,20,.12);font:400 7pt/1.45 'Jost';color:#3b342d;width:52mm}
.wall b{font-weight:500;letter-spacing:.2em;color:var(--acc);display:block;font-size:7pt}
.wall i{font-family:'Bodoni D';font-size:9pt;color:#1f1b17}
/* ===== skin: mercado (ch02) ===== */
.s-mercado .hero{background:#fffdf8}
.s-mercado .tag{background:#f3e4c3;border-radius:1.2mm;border:.25mm dashed rgba(150,90,40,.45)}
.s-mercado .tag .hole{position:absolute;left:2.6mm;top:2.4mm;width:2.4mm;height:2.4mm;border-radius:50%;background:#e7d7b4;border:.3mm solid #a98450;z-index:3}
.s-mercado .tag .n{left:6mm;top:.9mm;font:400 8pt 'Special Elite';color:var(--acc)}
.s-mercado .tag .str{position:absolute;left:-6mm;top:-1.5mm;width:10mm;height:6mm;z-index:3}
.s-mercado .hero .n{font:400 9pt 'Special Elite';top:1.3mm}
.chalk{position:absolute;background:#2b3430;border:2.2mm solid #8a5a33;border-radius:1.4mm;box-shadow:.5mm .8mm 0 rgba(60,40,20,.2);color:#f4f1e8;padding:3mm 4mm}
.chalk .t{font:700 15pt/1 'Caveat';color:#f6e6a8}
.chalk .r{font:500 11.5pt/1.25 'Caveat';color:#f1efe6}
.chalk .k{font:400 10.5pt/1.2 'Pen';color:#cfe3d2}
/* ===== skin: pasaporte + cartel retro (ch11) ===== */
.s-pasaporte .hero{background:#fbfaf5;border:.25mm solid rgba(31,58,95,.35);outline:.2mm solid rgba(31,58,95,.18);outline-offset:-1.2mm}
.s-pasaporte .hero .n{font:400 9pt 'Special Elite';color:var(--acc);top:1.6mm;left:2.6mm}
.s-pasaporte .tag{background:#efe2c4;border-radius:3.2mm 3.2mm 1mm 1mm;padding-top:4.2mm}
.s-pasaporte .tag .hole{position:absolute;left:50%;top:1.3mm;width:3mm;height:3mm;margin-left:-1.5mm;border-radius:50%;background:#f8f3e6;border:.55mm solid #b08a3e}
.s-pasaporte .tag .n{font:400 8pt 'Special Elite';color:var(--acc);left:2.2mm;top:1.2mm}
.s-pasaporte .tag .str{position:absolute;left:50%;top:-6mm;width:8mm;height:8mm;margin-left:-4mm}
.poster{position:absolute;overflow:hidden;box-shadow:.5mm .8mm 0 rgba(60,40,20,.18)}
.rs,.os{position:absolute}
"""
def card(k,es,g,p,en,ko,n,pos,hero,img,note,ph=True,extra=''):
    x,y,r=pos;cls='hero' if hero else 'tag'
    nt=' nt' if (note and not hero) else ''
    notes=f'<div class="note">{note}</div>' if note else ''
    return (f'<div class="card {cls}{nt}{" ph-note" if (note and ph) else ""}" style="left:{x}mm;top:{y}mm;transform:rotate({r}deg)">{extra}'
            f'<span class="n">{n:02d}</span>{notes}<div class="im">{img}</div>{lab(es,g,p,en,ko)}</div>')
HPOS=[(14,72,-1.8),(60,69,1.2),(106,73,-.9),(152,71,2.0),(15,133,1.3),(61,136,-1.6),(107,133,2.1),(152,136,-1.0)]
TPOS=[(13,196,-2.2),(44,198,1.6),(75,195,-1.0),(106,199,2.4),(137,196,-1.8),(168,199,1.1),
      (14,240,1.4),(45,242,-2.0),(76,239,1.0),(107,242,-1.3),(138,239,2.2),(168,242,-1.6)]
def shuffle_rot(L,seed):
    random.seed(seed);rs=[r for *_,r in L];random.shuffle(rs);return [(a,b,r) for (a,b,_),r in zip(L,rs)]
def opener(ch):
    return f'''<section class="page op" style="--acc:{ch["acc"]}"><img class="ph" src="{ch["dir"]}/img/{ch.get("opimg","opener.jpg")}" style="object-position:{ch.get("opos","50% 50%")}"><div class="gradt"></div><div class="grad"></div>
<div class="top">Vocabulario visual · Español</div><div class="badge">{ch["badge"]}</div>
<div class="cred">{ch["opcred"]}</div>
<div class="tb"><div class="kick">Tema {ch["n"]:02d} · {ch["part"]}</div><h1>{ch["title"]}</h1><div class="sub">{ch["en"]} · <span class="ko">{ch["ko"]}</span></div>
<div class="hand" style="color:{ch["handcol"]}">{ch["hand"]}</div>
<div class="rule"></div><div class="cap"><div><b>{ch["stop"]}</b><span class="chip" style="background:{ch["acc"]};color:#fff">{ch["skin"]}</span><br>{ch["place"]}</div><div style="text-align:right"><b>20 palabras</b><br>20 words · <span class="ko">20개 단어</span></div></div></div></section>'''
def wordpage(ch,cards,props,pg):
    return f'''<section class="page wp {ch["cls"]}" style="--acc:{ch["acc"]};--note:{ch["note"]}"><img class="paper" src="shared/paper.jpg">
<div class="hd"><div class="kick2">Tema {ch["n"]:02d} — {ch["part"]}</div><h2>{ch["title"]}</h2><div class="sub2">{ch["en"]} · <span class="ko">{ch["ko"]}</span></div>
<div class="legend">f femenino · m masculino · pl plural &nbsp;—&nbsp; <span class="ko">[ ] 한글 발음, <b>굵은 글자</b> = 강세 · 01–08 핵심</span></div></div>
{props}{cards}
<div class="folio"><span>{ch["n"]:02d} — {ch["title"]} · <span class="sk">{ch["skin"]}</span></span><span>fotos · Wikimedia Commons</span><span>Vocabulario visual · {pg}</span></div></section>'''
# ---------------- ch01 ----------------
NOTE1={'shower':'Latam: la regadera','toilet':'también: el váter','toothpaste':'= el dentífrico','hairdryer':'o: el secador','scissors':'¡siempre plural!'}
ROT={'toothbrush':(-30,46),'toothpaste':(-24,42),'shower':(-22,40)}  # deg, width mm
def ch01():
    ch=dict(n=1,dir='ch01',title='El baño',en='The bathroom',ko='욕실',part='En casa',acc='#a4533a',note='#2f4d84',cls='s-museo',skin='Museo · Alhambra',
            stop='Parada 01 · Granada',place='La Alhambra, baños del Palacio de Comares',hand='primero, el baño — 20 palabras para el viaje',handcol='#f3e3c4',
            opcred='Foto: Daniel Villafruela · CC BY-SA 3.0 · Wikimedia Commons',opos='50% 40%',opimg='opener_comares.jpg',
            badge=f'<div style="width:46mm;height:27.6mm;transform:rotate(-8deg)">{postmark("Nº 01 · EL BAÑO · ESPAÑA · ","GRANADA","#ffffff",.85,6)}</div>')
    star=[i for i in V3 if i['star']];rest=[i for i in V3 if not i['star']]
    hp=HPOS;hp=[(x,y-3 if i<4 else y+2,r) for i,(x,y,r) in enumerate(hp)]
    cs=''
    for n,i in enumerate(star):
        k=i['k']
        if k in ROT:
            d,w=ROT[k];img=f'<img class="rot" src="ch01/img/t_{i["img"]}" style="width:{w}mm;transform:translate(-50%,-50%) rotate({d}deg)">'
        else: img=f'<img class="cut" src="ch01/img/t_{i["img"]}">'
        mus=f'<div class="mus"><span>Nº {n+1:02d}</span><span class="ln"></span><span>Granada</span></div>'
        c=card(k,i['es'],i['g'],i['p'],i['en'],i['ko'],n+1,hp[n],1,img,NOTE1.get(k),ph=False,extra=tape(18,5.5,n))
        c=c.replace('<div class="lab">',mus+'<div class="lab">',1);cs+=c
    for n,i in enumerate(rest):
        k=i['k'];img=f'<img class="cut" src="ch01/img/t_{i["img"]}">'
        cs+=card(k,i['es'],i['g'],i['p'],i['en'],i['ko'],n+9,TPOS[n],0,img,NOTE1.get(k),ph=False,extra='<span class="hole"></span>')
    props=f'''<div class="print" style="left:117mm;top:13mm;width:55.2mm;height:41.2mm;transform:rotate(-2.4deg)"><img src="ch01/img/print_bench.jpg" style="width:50mm;height:36mm;object-fit:cover"></div>
<div class="abs" style="left:112mm;top:12mm;transform:rotate(-38deg)">{tape(20,6,91)}</div>
<div class="pol" style="left:163mm;top:24mm;width:36.8mm;transform:rotate(4deg)"><img src="ch01/img/pol_stars.jpg" style="width:32mm;height:32mm;object-fit:cover"><div class="c">estrellas de luz</div></div>
<div class="abs" style="left:172mm;top:21mm;transform:rotate(-6deg)">{tape(18,5.5,92)}</div>
<div class="wall" style="left:118mm;top:55mm;width:42mm;padding:1.4mm 2.4mm;transform:rotate(-1deg)"><b>CAT. 01–02 · AZULEJOS Y ESTRELLAS</b>Baño de Comares, la Alhambra</div>
<div class="abs" style="left:73mm;top:17mm;width:40mm;height:24mm;transform:rotate(-12deg)">{postmark('CORREO · GRANADA · ','ESPAÑA','#2f4d84',.55,6.4)}</div>'''
    return ch,opener(ch)+wordpage(ch,cs,props,2)
# ---------------- photo-card chapters ----------------
def photo_cards(ch,L,NOTE,skin_extra_hero,skin_extra_tag,seed):
    star=[x for x in L if x[6]];rest=[x for x in L if not x[6]]
    hp=shuffle_rot(HPOS,seed);tp=shuffle_rot(TPOS,seed+1);cs=''
    for n,(k,es,g,p,en,ko,s,o) in enumerate(star):
        cls='pp' if o=='p' else 'ph'
        cs+=card(k,es,g,p,en,ko,n+1,hp[n],1,f'<img class="{cls}" src="{ch["dir"]}/img/{k}.jpg">',NOTE.get(k),extra=skin_extra_hero(n))
    for n,(k,es,g,p,en,ko,s,o) in enumerate(rest):
        cls='pp' if o=='p' else 'ph'
        cs+=card(k,es,g,p,en,ko,n+9,tp[n],0,f'<img class="{cls}" src="{ch["dir"]}/img/{k}.jpg">',NOTE.get(k),extra=skin_extra_tag(n))
    return cs
STRING='<svg class="str" viewBox="0 0 10 6"><path d="M9 4.6 C6 6 3 1 .2 .6" fill="none" stroke="#9b7b4f" stroke-width=".35"/></svg>'
def ch02():
    ch=dict(n=2,dir='ch02',title='La cocina',en='The kitchen',ko='부엌',part='En casa',acc='#b8402e',note='#2f6b45',cls='s-mercado',skin='Mercado',
            stop='Parada 02 · València',place='Mercado Central de València',hand='al mercado, y luego a la cocina',handcol='#f6e6a8',
            opcred='Foto: Diego Delso · CC BY-SA 3.0 · Wikimedia Commons',
            badge='''<svg viewBox="0 0 44 26" style="width:44mm;height:26mm;transform:rotate(-6deg)"><path d="M8 1 H42 a1.5 1.5 0 0 1 1.5 1.5 V23.5 a1.5 1.5 0 0 1 -1.5 1.5 H8 L1 13 Z" fill="none" stroke="#fff" stroke-width=".7" opacity=".9"/><circle cx="8" cy="13" r="1.6" fill="none" stroke="#fff" stroke-width=".6" opacity=".9"/>
<text x="26" y="10" text-anchor="middle" font-family="Special Elite" font-size="3" fill="#fff" letter-spacing=".5" opacity=".92">MERCADO · Nº 02</text><text x="26" y="19" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="8.4" fill="#fff" opacity=".95">la cocina</text></svg>''')
    hx=lambda n: tape(18,5.5,n+20,col='rgba(250,246,238,.92)',stripes='rgba(184,64,46,.75)')
    tx=lambda n: '<span class="hole"></span>'+STRING
    cs=photo_cards(ch,CH02,NOTE02,hx,tx,7)
    props=f'''<div class="chalk" style="left:116mm;top:12mm;width:50mm;height:44mm;transform:rotate(1.2deg)"><div class="t">Hoy en la cocina</div>
<div class="r" style="margin-top:1.6mm">la olla · la sartén<br>la paellera · el mortero</div><div class="k" style="margin-top:1.2mm">냄비, 프라이팬, 파에야 팬</div>
<svg viewBox="0 0 40 6" style="width:40mm;height:4mm;margin-top:1.4mm"><path d="M1 3 q5 -3 10 0 t10 0 t10 0 t8 0" fill="none" stroke="#f6e6a8" stroke-width=".5" opacity=".8"/></svg><div class="r" style="font-size:10.5pt">¡20 palabras!</div></div>
<div class="pol" style="left:170mm;top:15mm;width:30.8mm;transform:rotate(5deg)"><img src="ch02/img/pol1.jpg" style="width:26mm;height:26mm;object-fit:cover"><div class="c" style="font-size:10pt">Mercat Central</div></div>
<div class="abs" style="left:176mm;top:12mm;transform:rotate(-4deg)">{tape(18,5.5,93,col='rgba(250,246,238,.92)',stripes='rgba(184,64,46,.75)')}</div>
<div class="hand abs" style="left:168mm;top:52mm;font-size:11.5pt;color:#7a3b22;transform:rotate(-3deg)">fruta, pescado y más</div>'''
    return ch,opener(ch)+wordpage(ch,cs,props,4)
def poster():
    # vector "cartel retro": flat sun, sky bands, converging rails, Jost caps (no real logos)
    rays=''.join(f'<path d="M60 64 L{60+120*__import__("math").cos(a/57.3):.1f} {64-120*__import__("math").sin(a/57.3):.1f} L{60+120*__import__("math").cos((a+6)/57.3):.1f} {64-120*__import__("math").sin((a+6)/57.3):.1f} Z" fill="#e8b33a" opacity=".55"/>' for a in range(0,180,12))
    return f'''<svg viewBox="0 0 60 80" style="width:100%;height:100%"><defs><clipPath id="pc"><rect width="60" height="80"/></clipPath></defs><g clip-path="url(#pc)">
<rect width="60" height="80" fill="#f3d58a"/><g transform="scale(.5)">{rays}</g><circle cx="30" cy="32" r="10" fill="#c8432f"/>
<rect y="40" width="60" height="40" fill="#1f3a5f"/><path d="M0 40 L60 40 L60 44 L0 44Z" fill="#2c5282"/>
<path d="M26 80 L29.2 41 L30.8 41 L34 80Z" fill="#d9a21b"/><path d="M14 80 L29 41 M46 80 L31 41" stroke="#f3d58a" stroke-width=".8"/>
{''.join(f'<rect x="{30-1.2-(y-41)*0.42:.2f}" y="{y}" width="{2.4+(y-41)*0.84:.2f}" height="{0.4+(y-41)*0.03:.2f}" fill="#f3d58a" opacity=".8"/>' for y in [44,48,53,59,66,74])}
<text x="30" y="11" text-anchor="middle" font-family="Jost" font-weight="500" font-size="8.6" letter-spacing="1.6" fill="#1f3a5f">MADRID</text>
<text x="30" y="19" text-anchor="middle" font-family="Jost" font-weight="500" font-size="4.2" letter-spacing=".5" fill="#1f3a5f">EN TREN · A PIE</text>
<rect x="17" y="72.2" width="26" height="6.4" fill="#1f3a5f"/><text x="30" y="77.2" text-anchor="middle" font-family="Jost" font-weight="500" font-size="4.2" letter-spacing="1" fill="#f3d58a">KM 0</text></g></svg>'''
def ch11():
    ch=dict(n=11,dir='ch11',title='El transporte',en='Getting around',ko='교통',part='La ciudad y el viaje',acc='#1f3a5f',note='#b8332b',cls='s-pasaporte',skin='Pasaporte · Cartel retro',
            stop='Parada 11 · Madrid',place='Estación de Atocha, el jardín tropical',hand='¿a dónde vamos hoy? — en tren, en metro, a pie',handcol='#f3d58a',
            opcred='Foto: Nan Palmero · CC BY 2.0 · Wikimedia Commons',
            badge=f'<div style="width:46mm;height:24mm;transform:rotate(7deg)">{rectstamp("ENTRADA · ENTRY","MADRID","ESPAÑA · Nº 11","#ffffff",.9,46,24)}</div>')
    hx=lambda n:''
    tx=lambda n:'<span class="hole"></span><svg class="str" viewBox="0 0 8 8"><path d="M4 7 C1 4 6 2 3 0" fill="none" stroke="#9b7b4f" stroke-width=".4"/></svg>'
    cs=photo_cards(ch,CH11,NOTE11,hx,tx,11)
    props=f'''<div class="poster" style="left:118mm;top:11mm;width:36mm;height:48mm;transform:rotate(-2.5deg)">{poster()}</div>
<div class="abs" style="left:126mm;top:9mm;transform:rotate(-8deg)">{tape(18,5.5,94)}</div>
<div class="pol" style="left:160mm;top:18mm;width:36.8mm;transform:rotate(4.5deg)"><img src="ch11/img/pol1.jpg" style="width:32mm;height:32mm;object-fit:cover"><div class="c">km 0, Puerta del Sol</div></div>
<div class="abs" style="left:169mm;top:15mm;transform:rotate(3deg)">{tape(18,5.5,95)}</div>
<div class="abs" style="left:170mm;top:37mm;width:34mm;height:20.4mm;transform:rotate(-14deg)">{oval_stamp("AEROPUERTO","LLEGADA","MADRID · ES","#b8332b",.7)}</div>
<div class="abs" style="left:86mm;top:55.5mm;transform:rotate(-5deg)">{rectstamp("SALIDA · DEPARTURE","ATOCHA","EN TREN · Nº 11","#1f3a5f",.62,32,14)}</div>
<div class="hand abs" style="left:160mm;top:61mm;font-size:11.5pt;color:#7a3b22;transform:rotate(-3deg)">sellos de mi viaje</div>'''
    return ch,opener(ch)+wordpage(ch,cs,props,6)

"""ch09 Café y panadería — 인쇄용 PDF 6쪽 (오프너·단어·어순 3쪽·크레딧).
v6 CSS·카드 규칙을 그대로 쓰고, 한글은 Pretendard, 범례 줄 겹침은 측정해서 보정해요.
실행: python build_ch09.py <프로젝트 폴더>
"""
import asyncio, json, random, re, sys, html
import yaml
from playwright.async_api import async_playwright

P = sys.argv[1]; C = f'{P}/claude_design/ch09'
V6 = open(f'{P}/design/build/v6/index_v6.html', encoding='utf-8').read()
CSS = re.search(r'<style>(.*?)</style>', V6, re.S).group(1)
CSS = CSS.replace('fonts/GowunBatang-Regular.ttf', 'fonts/Pretendard-Regular.ttf').replace('fonts/GowunBatang-Bold.ttf', 'fonts/Pretendard-Bold.ttf')
D = yaml.safe_load(open(f'{P}/es/ch09/text/ch09_text.yaml', encoding='utf-8'))
CR = json.load(open(f'{C}/credits.json', encoding='utf-8'))
PROPS = {}
for _p in D['props']: PROPS.setdefault(_p['kind'], _p['lines'])
W = {w['key']: w for w in D['words']}
CH = D['chapter']; NUM = CH['num']; PG0 = 48          # 책 쪽번호: ch09 = 48–53
ACC, NOTE = '#b8402e', '#2f6b45'
RED, GREEN = 'rgba(184,64,46,.75)', 'rgba(47,107,69,.78)'
SKIN = 'Mercado'; PART = 'Comer y beber'
E = html.escape

CSS += """
/* ===== claude ch09 additions (Mercado · Salamanca) ===== */
.kraft{position:absolute;background:#f3e4c3;border:.25mm dashed rgba(150,90,40,.45);border-radius:1.4mm;padding:3mm 4mm 3mm 7mm;box-shadow:.4mm .6mm 0 rgba(60,40,20,.13)}
.kraft .hole{position:absolute;left:2.2mm;top:50%;width:2.6mm;height:2.6mm;margin-top:-1.3mm;border-radius:50%;background:#e7d7b4;border:.3mm solid #a98450}
.kraft .h{font:500 7pt 'Jost';letter-spacing:.2em;text-transform:uppercase;color:var(--acc)}
.kraft .h2k{font:400 12pt/1.2 'Pen';color:#3a2a22;margin:.6mm 0 1.6mm}
.kr{display:flex;align-items:baseline;justify-content:space-between;gap:2mm;padding:1.2mm 0;border-bottom:.2mm dotted rgba(120,80,50,.45)}
.kr:last-child{border-bottom:0}
.kr .es{font:600 9.8pt 'Bodoni T';white-space:nowrap}.kr .es i{font-style:normal;color:var(--acc)}
.kr .en{font:400 7pt 'Jost';color:#5a4f44;white-space:nowrap}
.kr .ko{font:400 7.6pt 'Gowun';color:#2e2822}
.chalk2{position:absolute;background:#2b3430;border:2.2mm solid #8a5a33;border-radius:1.4mm;box-shadow:.5mm .8mm 0 rgba(60,40,20,.2);color:#f4f1e8;padding:3.4mm 4.4mm}
.chalk2 .t{font:700 14pt/1 'Caveat';color:#f6e6a8;margin-bottom:2mm}
.chalk2 .lb{font:400 7pt 'Gowun';color:#bfc9c2;margin-top:2.2mm}
.chalk2 .es{font:500 13pt/1.15 'Caveat';color:#f1efe6}.chalk2 .es i{font-style:normal;color:#f2a58f}
.chalk2 .k{font:400 10pt/1.15 'Pen';color:#cfe3d2}
.gram{position:absolute;background:#7a3a24;color:#f6ead8;padding:3.4mm 4mm;box-shadow:.5mm .8mm 0 rgba(60,40,20,.2);outline:.25mm solid rgba(246,234,216,.55);outline-offset:-1.6mm}
.gram .h{font:500 7pt 'Jost';letter-spacing:.2em;color:#f1c58b;margin-bottom:1.4mm}.gram .h span{font-family:'Gowun';letter-spacing:.05em}
.gram ul{margin:0;padding-left:3.4mm}.gram li{font:400 7.5pt/1.5 'Gowun';margin-bottom:.8mm}
.scn{position:absolute;background:#fdfcf8;padding:2.4mm 2.4mm 0;box-shadow:.5mm .8mm 0 rgba(60,40,20,.16)}
.scn .frame{position:relative;overflow:hidden}.scn .frame img{width:100%;height:100%;object-fit:cover;display:block}
.scn .cap{display:flex;justify-content:space-between;align-items:center;height:7mm;font:400 7pt 'Jost';color:#5a4f44}
.scn .cap b{font-weight:500;letter-spacing:.2em;color:var(--acc);margin-right:2mm}
.lbl{position:absolute;background:#f3e4c3;border:.25mm solid rgba(150,90,40,.5);border-radius:1mm;padding:1mm 2mm 1mm 4mm;box-shadow:.3mm .5mm 0 rgba(40,25,10,.25);white-space:nowrap}
.lbl:before{content:'';position:absolute;left:1.2mm;top:50%;width:1.6mm;height:1.6mm;margin-top:-.8mm;border-radius:50%;border:.25mm solid #9b7b4f;background:#fdfaf3}
.lbl .es{font:700 10.5pt/1.05 'Caveat';color:#2f6b45}.lbl .es i{font-style:normal;color:var(--acc)}
.lbl .ko{font:400 7pt 'Gowun';color:#3b342d;margin-top:.3mm}
.lead2{position:absolute;left:15mm;width:180mm;font:400 8.6pt/1.55 'Gowun';color:#2e2822}.lead2 b{color:var(--acc)}
.chip2{display:inline-flex;align-items:center;gap:1.2mm;margin-right:4mm;font:400 7.4pt 'Gowun';color:#3b342d}
.chip2 i{display:inline-block;width:3mm;height:3mm;border-radius:.6mm;border:.25mm solid rgba(60,40,20,.3)}
.ex8{display:flex;gap:2.4mm;align-items:flex-start;height:16.4mm}
.ex8 .th{width:14mm;height:14mm;flex:none;background:#fdfcf8;padding:.8mm;box-shadow:.3mm .5mm 0 rgba(60,40,20,.14)}.ex8 .th img{width:100%;height:100%;object-fit:cover}
.ex8 .wd{font:500 7pt 'Jost';letter-spacing:.16em;text-transform:uppercase;color:var(--acc)}.ex8 .wd .n{font-family:'Special Elite';letter-spacing:0;margin-right:1mm}
.ex8 .es{font:600 10pt/1.2 'Bodoni T';margin-top:.4mm}
.ex8 .tr{font:400 7.4pt/1.35 'Gowun';color:#2e2822;margin-top:.4mm}.ex8 .tr .en{font-family:'Jost';color:#6b5e50;font-size:7pt}
.cg{position:absolute;background:#fdfaf3;padding:2.2mm 2.4mm 2.4mm;box-shadow:.4mm .6mm 0 rgba(60,40,20,.13);border-top:1.4mm solid var(--acc)}
.cg .im{height:18mm}.cg .im img{width:100%;height:100%;object-fit:cover}
.cg .es{font:600 10pt 'Bodoni T';margin-top:1.6mm}.cg .en{font:400 7pt 'Jost';color:#5a4f44;margin-top:.2mm}
.cg .ko{font:400 7.4pt/1.45 'Gowun';color:#2e2822;margin-top:.8mm}
.tkt{position:absolute;background:#fbf8f0;padding:3mm 3.6mm 3.4mm;font:400 7.4pt/1.55 'Special Elite','Gowun';color:#2e2822;box-shadow:.4mm .6mm 0 rgba(60,40,20,.15)}
.tkt:after{content:'';position:absolute;left:0;right:0;bottom:-1.4mm;height:1.4mm;background:radial-gradient(circle at 1mm 0,#fbf8f0 .9mm,transparent .95mm) 0 0/2mm 1.4mm repeat-x}
.tkt .hr{border-top:.25mm dashed #8a7a68;margin:1.2mm 0}.tkt .dec{font:400 8pt 'Caveat';color:#7a3b22;text-align:right;margin-top:.6mm}
.rnd{position:absolute;border-radius:50%;overflow:hidden;border:1.6mm solid #fdfcf8;box-shadow:.4mm .7mm 0 rgba(60,40,20,.18)}.rnd img{width:100%;height:100%;object-fit:cover}
.band{position:absolute;background:#fdfcf8;padding:2mm;box-shadow:.4mm .7mm 0 rgba(60,40,20,.16)}
.band .frame{position:relative;overflow:hidden}.band img{width:100%;height:100%;object-fit:cover;display:block}
.band .cr{position:absolute;right:2mm;bottom:1.2mm;font:400 6.5pt 'Jost';color:#fff;text-shadow:0 0 1mm rgba(0,0,0,.8)}
.tl{display:inline-flex;align-items:center;padding:.9mm 2.2mm;margin-right:1.6mm;background:#fdfaf3;border:.25mm solid rgba(60,40,20,.22);border-radius:.8mm;box-shadow:.2mm .4mm 0 rgba(60,40,20,.12);font:600 9.8pt 'Bodoni T'}
"""

# ---------- v6 helpers (base_v6 그대로) ----------
GL = {'f': 'f', 'm': 'm', 'fpl': 'f pl', 'mpl': 'm pl'}
STRING = '<svg class="str" viewBox="0 0 10 6"><path d="M9 4.6 C6 6 3 1 .2 .6" fill="none" stroke="#9b7b4f" stroke-width=".35"/></svg>'
HPOS = [(14,72,-1.8),(60,69,1.2),(106,73,-.9),(152,71,2.0),(15,133,1.3),(61,136,-1.6),(107,133,2.1),(152,136,-1.0)]
TPOS = [(13,196,-2.2),(44,198,1.6),(75,195,-1.0),(106,199,2.4),(137,196,-1.8),(168,199,1.1),
        (14,240,1.4),(45,242,-2.0),(76,239,1.0),(107,242,-1.3),(138,239,2.2),(168,242,-1.6)]

def tape(w=30, h=9, seed=0, col='rgba(226,214,180,.74)', stripes=None):
    random.seed(seed*31+w)
    pts=[(0,0)]+[(w*k/6+random.uniform(-.8,.8),random.uniform(-.5,.5)) for k in range(1,6)]+[(w,0)]+[(w+random.uniform(-.9,.9),h*k/5) for k in range(1,5)]+[(w,h)]+[(w*k/6+random.uniform(-.8,.8),h+random.uniform(-.5,.5)) for k in range(5,0,-1)]+[(0,h)]+[(random.uniform(-.9,.9),h*k/5) for k in range(4,0,-1)]
    p=' '.join(f'{x:.2f},{y:.2f}' for x,y in pts); cid=f'tc{seed}{w}'.replace('.','')
    st=''
    if stripes:
        st=f'<clipPath id="{cid}"><polygon points="{p}"/></clipPath><g clip-path="url(#{cid})">'+''.join(f'<rect x="{x}" y="-2" width="2" height="{h+4}" fill="{stripes}" transform="skewX(-30)"/>' for x in range(-4,int(w)+8,4))+'</g>'
    return f'<svg class="tape" style="width:{w}mm;height:{h}mm" viewBox="-1 -1 {w+2} {h+2}"><polygon points="{p}" fill="{col}"/>{st}<polygon points="{p}" fill="none" stroke="rgba(150,130,90,.25)" stroke-width=".15"/></svg>'

_pm = [0]
def postmark(txt, center, col, op=.8, fs=6):
    _pm[0] += 1; i = _pm[0]
    return f'''<svg viewBox="0 0 100 60" class="pmsvg"><g fill="none" stroke="{col}" stroke-width="1.3" opacity="{op}"><circle cx="30" cy="30" r="26"/><circle cx="30" cy="30" r="17"/><path d="M60 14 q8 -4 16 0 t16 0 M60 24 q8 -4 16 0 t16 0 M60 34 q8 -4 16 0 t16 0 M60 44 q8 -4 16 0 t16 0"/></g>
<defs><path id="arc{i}" d="M30 30 m-21.5 0 a21.5 21.5 0 1 1 43 0 a21.5 21.5 0 1 1 -43 0"/></defs>
<text font-family="Special Elite" font-size="6.2" fill="{col}" opacity="{op}" letter-spacing="1.1"><textPath href="#arc{i}">{txt}</textPath></text>
<text x="30" y="32.5" text-anchor="middle" font-family="Special Elite" font-size="{fs}" fill="{col}" opacity="{op}">{center}</text></svg>'''

def shuffle_rot(L, seed):
    random.seed(seed); rs=[r for *_,r in L]; random.shuffle(rs); return [(a,b,r) for (a,b,_),r in zip(L,rs)]
def pron(s): return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
def lab(w):
    return (f'<div class="lab"><div class="l1"><span class="w">{w["es"]}</span><span class="g g{w["gender"][0]}">{GL[w["gender"]]}</span></div>'
            f'<div class="lp"><span class="pr">[{pron(w["pron"])}]</span></div><div class="l2"><span class="en">{w["en"]}</span> · <span class="ko">{w["ko"]}</span></div></div>')
def credit_short(k):
    c = CR[k]; a = re.sub(r'\s+', ' ', c['artist']).strip() or 'autor desconocido'
    return f'{a} · {c["lic"]}'

def price_tag(l1, l2, w=31):
    h = w * 24 / 50
    return f'''<svg viewBox="-7 0 57 24" style="width:{w*57/50:.1f}mm;height:{h:.1f}mm"><path d="M9 1 H48 a1.5 1.5 0 0 1 1.5 1.5 V21.5 a1.5 1.5 0 0 1 -1.5 1.5 H9 L1 12 Z" fill="#d8b98a" stroke="#9b7b4f" stroke-width=".35"/>
<path d="M9.6 2.6 H47 V21.4 H9.6 L2.8 12 Z" fill="none" stroke="#b08d5c" stroke-width=".2" stroke-dasharray=".8 .6"/>
<circle cx="8.5" cy="12" r="1.7" fill="#f1e6cc" stroke="#9b7b4f" stroke-width=".35"/><path d="M8.5 12 C4 9 0 15 -6.5 10" fill="none" stroke="#7a5a33" stroke-width=".4"/>
<text x="29" y="10" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="6.6" fill="#3a2a22">{l1}</text>
<text x="29" y="18.8" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="7.8" fill="#b8402e">{l2}</text></svg>'''

def arches(w=180, h=12, n=20):
    """살라망카 마요르 광장 아케이드를 단순화한 벡터 띠 (사진 아님)."""
    aw = w / n; s = f'<svg viewBox="0 0 {w} {h}" style="width:{w}mm;height:{h}mm;display:block"><rect width="{w}" height="{h}" fill="#c9a46a"/><rect width="{w}" height="1.6" fill="#b48c52"/><rect y="2.2" width="{w}" height=".35" fill="#8f6d3c"/>'
    for i in range(n):
        x = i * aw + aw * .18; ww = aw * .64
        s += f'<path d="M{x:.2f} {h} V{h*.55:.2f} A{ww/2:.2f} {ww/2:.2f} 0 0 1 {x+ww:.2f} {h*.55:.2f} V{h}" fill="#f4ead6"/>'
        s += f'<circle cx="{i*aw+aw/2:.2f}" cy="3.9" r=".55" fill="#8f6d3c"/>'
    return s + '</svg>'

def folio(pg, mid='gramática visual'):
    return f'<div class="folio"><span>{NUM:02d} — {CH["es"]} · <span class="sk">{SKIN}</span></span><span>{mid}</span><span>Vocabulario visual · {pg}</span></div></section>'
def sec_head(no, t, k): return f'<div class="sh"><span class="no">{no}</span><span class="t">{t}</span><span class="k">{k}</span></div>'

# ---------- p48 opener ----------
def opener():
    st = PROPS['stamp']
    badge = f'''<svg viewBox="0 0 44 26" style="width:44mm;height:26mm;transform:rotate(-6deg)"><path d="M8 1 H42 a1.5 1.5 0 0 1 1.5 1.5 V23.5 a1.5 1.5 0 0 1 -1.5 1.5 H8 L1 13 Z" fill="none" stroke="#fff" stroke-width=".7" opacity=".9"/><circle cx="8" cy="13" r="1.6" fill="none" stroke="#fff" stroke-width=".6" opacity=".9"/>
<text x="26" y="10" text-anchor="middle" font-family="Special Elite" font-size="3" fill="#fff" letter-spacing=".5" opacity=".92">{st[1]}</text><text x="26" y="19" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="7.6" fill="#fff" opacity=".95">{st[0].title()}</text></svg>'''
    o = D['opener']; stop = o['parada']
    return f'''<section class="page op" style="--acc:{ACC}"><img class="ph" src="img/opener.jpg" style="object-position:50% 40%"><div class="gradt"></div><div class="grad"></div>
<div class="top">Vocabulario visual · Español</div><div class="badge">{badge}</div>
<div class="cred">Foto: {E(credit_short("opener"))} · Wikimedia Commons</div>
<div class="tb"><div class="kick">Tema {NUM:02d} · {PART}</div><h1 style="font-size:78pt">{CH["es"]}</h1><div class="sub">{CH["en"]} · <span class="ko">{CH["ko"]}</span></div>
<div class="hand" style="color:#f6e6a8">{o["hand"]}</div>
<div class="rule"></div><div class="cap"><div><b>{stop}</b><span class="chip" style="background:{ACC};color:#fff">{SKIN}</span><br>{o["place"]}</div><div style="text-align:right"><b>20 palabras</b><br>20 words · <span class="ko">20개 단어</span></div></div></div></section>'''

# ---------- p49 palabras ----------
def palabras(dh, dt):
    star = [w for w in D['words'] if w['core']]; rest = [w for w in D['words'] if not w['core']]
    hp = shuffle_rot(HPOS, 9); tp = shuffle_rot(TPOS, 10); cs = ''
    for grp, pos, off, hero in ((star, hp, 1, 1), (rest, tp, 9, 0)):
        for n, w in enumerate(grp):
            x, y, r = pos[n]; note = w.get('note') or ''
            cls = ('hero' if hero else 'tag') + (' nt' if note and not hero else '') + (' ph-note' if note else '')
            ex = tape(18,5.5,n+90,col='rgba(250,246,238,.92)',stripes=RED if n%2==0 else GREEN) if hero else '<span class="hole"></span>'+STRING
            dy = dh[n//4] if hero else dt[n//6]
            cs += (f'<div class="card {cls}" data-row="{"h" if hero else "t"}" style="left:{x}mm;top:{y+dy:.2f}mm;transform:rotate({r}deg)">{ex}'
                   f'<span class="n">{n+off:02d}</span>{f"<div class=note>{note}</div>" if note else ""}<div class="im"><img class="ph" src="img/{w["key"]}.jpg"></div>{lab(w)}</div>')
    ck = PROPS['chalk']; pr = PROPS['price']
    rows = ''.join(f'<div class="r" style="font-size:11pt;display:flex;justify-content:space-between"><span>{a}</span><span style="color:#f6e6a8">{b}</span></div>' for a, b in (l.split(' · ') for l in ck[1:]))
    props = f'''<div class="chalk chk" data-n="chalk" style="left:116mm;top:12mm;width:50mm;height:41mm;transform:rotate(1.2deg)"><div class="t" style="font-size:13pt;letter-spacing:.04em">{ck[0].capitalize()}</div>
<div style="margin-top:2mm">{rows}</div>
<svg viewBox="0 0 40 6" style="width:40mm;height:4mm;margin-top:1mm"><path d="M1 3 q5 -3 10 0 t10 0 t10 0 t8 0" fill="none" stroke="#f6e6a8" stroke-width=".5" opacity=".8"/></svg><div class="r" style="font-size:10.5pt">16 de mayo</div></div>
<div class="pol chk" data-n="polaroid" style="left:170mm;top:15mm;width:30.8mm;transform:rotate(5deg)"><img src="img/polaroid.jpg" style="width:26mm;height:26mm;object-fit:cover"><div class="c" style="font-size:9.5pt">{PROPS["polaroid"][0]}</div></div>
<div class="abs" style="left:176mm;top:12mm;transform:rotate(-4deg)">{tape(18,5.5,93,col='rgba(250,246,238,.92)',stripes=GREEN)}</div>
<div class="abs chk" data-n="price" style="left:122mm;top:55.2mm;transform:rotate(-3deg)">{price_tag(pr[0], pr[1], 30)}</div>
<div class="hand abs chk" data-n="hand" style="left:160mm;top:58.5mm;font-size:11pt;color:#7a3b22;transform:rotate(-3deg)">un café y un cruasán</div>'''
    return f'''<section class="page wp s-mercado" style="--acc:{ACC};--note:{NOTE}"><img class="paper" src="shared/paper.jpg">
<div class="hd chk" data-n="header"><div class="kick2">Tema {NUM:02d} — {PART}</div><h2>{CH["es"]}</h2><div class="sub2">{CH["en"]} · <span class="ko">{CH["ko"]}</span></div>
<div class="legend">f femenino · m masculino · pl plural &nbsp;—&nbsp; <span class="ko">[ ] 한글 발음, <b>굵은 글자</b> = 강세 · 01–08 핵심</span></div></div>
{props}{cs}
<div class="folio"><span>{NUM:02d} — {CH["es"]} · <span class="sk">{SKIN}</span></span><span>fotos · Wikimedia Commons</span><span>Vocabulario visual · {PG0+1}</span></div></section>'''

def gp_head(kick, title, sub):
    return f'''<section class="page wp gp s-mercado" style="--acc:{ACC};--note:{NOTE}"><img class="paper" src="shared/paper.jpg">
<div class="hd"><div class="kick2">{kick}</div><h2>{title}</h2><div class="sub2 chk" data-n="header">{sub}</div></div>'''

def hi_es(s):
    """lo/la/los/las(직접목적 대명사)를 강조색으로."""
    return re.sub(r'(?<![\w¿])(Lo|La|Los|Las|lo|la|los|las)(?= (quiero|tomo|pago))', r'<i>\1</i>', s)

# ---------- p50 word order 1/3 ----------
def gram1():
    wo = D['word_order']
    h = gp_head(f'Tema {NUM:02d} — El orden de las palabras · 1/3', wo['tema'], f'Object pronoun · verb · <span class="ko">{wo["tema_sub_ko"]}</span>')
    lead = wo['lead_ko'].replace('lo나 la', '<b>lo</b>나 <b>la</b>').replace('동사 바로 앞', '<b>동사 바로 앞</b>')
    h += f'<div class="lead2 chk" data-n="lead" style="top:42mm">{lead}</div>'
    # scene photo 180 x 92, labels (컵 로고 위에 el chocolate 라벨을 얹어 가림)
    s0, s2 = wo['sentences'][0], wo['sentences'][2]
    labels = [
        (25.5, 23.2, '<i>el</i> chocolate', W['chocolate']['ko'] + ' · ' + W['chocolate']['pron'].replace('**', '')),
        (52, 33.2, 'la taza', W['cup']['ko'] + ' · ' + W['cup']['pron'].replace('**', '')),
        (96, 4, hi_es(s2['es']), s2['ko']),
        (60, 3, 'la cucharilla', W['teaspoon']['ko']),
        (118, 62, hi_es(s0['es']), s0['ko']),
    ]
    lb = ''.join(f'<div class="lbl" style="left:{x}mm;top:{y}mm;padding-bottom:1.6mm"><div class="es">{es}</div><div class="ko">{ko}</div></div>' for x, y, es, ko in labels)
    h += f'''<div class="scn chk" data-n="scene" style="left:15mm;top:53mm;width:180mm;transform:rotate(-.4deg)"><div class="frame" style="height:80mm"><img src="img/scene.jpg" style="object-position:50% 55%">{lb}</div>
<div class="cap"><span><b>CHURRERÍA</b>chocolate con churros en la barra (logotipo tapado)</span><span>foto: {E(credit_short("scene"))}</span></div></div>
<div class="abs" style="left:24mm;top:50mm;transform:rotate(-6deg)">{tape(20,6,301,col='rgba(250,246,238,.92)',stripes=RED)}</div>
<div class="abs" style="left:168mm;top:50mm;transform:rotate(5deg)">{tape(20,6,302,col='rgba(250,246,238,.92)',stripes=GREEN)}</div>'''
    # §1 blocks
    s = f'<div class="sec chk" data-n="s1" style="left:15mm;top:145mm;width:180mm">{sec_head("§1","Bloques de palabras","단어 블록 + 한국어 직역 · 색칸 = 어순 포인트")}'
    s += '<div style="margin:-.4mm 0 2.2mm"><span class="chip2"><i style="background:#f4e0d6;border-color:#a4533a"></i>lo · la · los · las = 그것(들)을</span><span class="chip2"><i style="background:#fbf7ee"></i>나머지 블록</span></div>'
    for j, t in enumerate(wo['sentences']):
        bl = ''.join(f'<span class="blk{" hi" if i in t["highlight"] else ""}"><span class="e">{E(k["es"])}</span><span class="g">{k["gloss_ko"]}</span></span>' for i, k in enumerate(t['tokens']))
        s += f'<div class="sr" style="margin-bottom:2mm"><span class="nn">{j+1}</span><div style="width:96mm;flex:none">{bl}</div><div><div class="tr">{t["ko"]} <span class="en">· {E(t["en"])}</span></div><div class="nt">{t["note_ko"]}</div></div></div>'
    s += '</div>'
    nota = ''.join(f'<p style="margin-top:{.8 if i else 0}mm">{n}</p>' for i, n in enumerate(wo['extra_notes_ko']))
    s += f'<div class="box chk" data-n="nota" style="left:15mm;top:229mm;width:180mm;font:400 7.8pt/1.55 \'Gowun\';color:#2e2822"><b class="h">NOTA · 정리</b>{nota}</div>'
    s += f'<div class="abs chk" data-n="band" style="left:15mm;top:264mm">{arches()}</div>'
    return h + s + folio(PG0+2)

# ---------- p51 word order 2/3 ----------
def gram2():
    wo = D['word_order']; p0, p1 = wo['patterns']; ct = wo['contrast']
    h = gp_head(f'Tema {NUM:02d} — El orden de las palabras · 2/3', 'Lo, la, los, las', f'Object pronouns · <span class="ko">물건에 맞춰 고르고, 동사 앞에</span>')
    TAGC = {'m': '#3e5a86', 'f': '#a4533a', 'm pl': '#3e5a86', 'f pl': '#a4533a'}
    r0 = ''.join(f'<div class="kr"><span class="es">{E(it["es"].split(" → ")[0])} → <i>{it["es"].split(" → ")[1].split(" ")[0]}</i> {" ".join(it["es"].split(" → ")[1].split(" ")[1:])}</span><span class="gtag" style="background:{TAGC[it["tag"]]}">{it["tag"]}</span></div><div class="ko" style="font:400 7.4pt \'Gowun\';color:#4a4038;margin:-.4mm 0 .6mm">{it["ko"]}</div>' for it in p0['items'])
    h += f'<div class="kraft chk" data-n="n1" style="left:15mm;top:44mm;width:86mm;transform:rotate(-.6deg)"><span class="hole"></span><div class="h">Nº 1 · el, la, los, las → lo, la, los, las</div><div class="h2k">{p0["title_ko"]}</div>{r0}</div>'
    r1 = ''.join(f'<div class="kr" style="display:block"><div style="display:flex;justify-content:space-between;align-items:baseline"><span class="es">{E(it["es"]).replace(" con ", " <i>con</i> ").replace(" de ", " <i>de</i> ")}</span><span class="en">{it["en"]}</span></div><div class="ko">{it["ko"]} <span class="en" style="margin-left:1mm">{it["lit"]}</span></div></div>' for it in p1['items'])
    h += f'<div class="kraft chk" data-n="n2" style="left:108mm;top:44mm;width:87mm;transform:rotate(.6deg)"><span class="hole"></span><div class="h">Nº 2 · con · de</div><div class="h2k">{p1["title_ko"]}</div>{r1}</div>'
    cs = ''.join(f'<div class="lb">{it["label_ko"]}</div><div class="es">{hi_es(E(it["es"])).replace("tomarlo", "tomar<i>lo</i>")}</div><div class="k">{it["ko"]}</div>' for it in ct['items'])
    h += f'<div class="chalk2 chk" data-n="contrast" style="left:16mm;top:112.5mm;width:84mm;transform:rotate(-1deg)"><div class="t">¿Antes o después? <span style="font:400 10pt \'Pen\';color:#cfe3d2">{ct["title_ko"]}</span></div>{cs}</div>'
    tk = PROPS['ticket']
    h += f'''<div class="tkt chk" data-n="ticket" style="left:110mm;top:112.5mm;width:56mm;transform:rotate(2deg)"><div style="text-align:center;letter-spacing:.08em">{tk[0]}</div><div class="hr"></div><div>{tk[1].replace(" · ", "<br>")}</div><div class="hr"></div><div style="text-align:right">{tk[2].split(" · ")[0]}</div><div style="text-align:center;margin-top:.6mm">{tk[2].split(" · ")[1]}</div><div class="dec">decorativo</div></div>
<div class="rnd chk" data-n="cortado" style="left:169mm;top:115.5mm;width:27mm;height:27mm"><img src="img/cortado.jpg"></div>'''
    gr = ''.join(f'<li>{g}</li>' for g in D['extras']['grammar_ko'])
    h += f'<div class="gram chk" data-n="gram" style="left:108mm;top:155.6mm;width:87mm;transform:rotate(-.5deg)"><div class="h">GRAMÁTICA · <span>카페에서 쓰는 말</span></div><ul>{gr}</ul></div>'
    # §3 core examples
    core = [w for w in D['words'] if w['core']]
    rows = ''
    for i, w in enumerate(core):
        ex = w['example']
        rows += f'<div class="ex8"><div class="th"><img src="img/{w["key"]}.jpg"></div><div><div class="wd"><span class="n">{i+1:02d}</span>{w["es"]}</div><div class="es">{E(ex["es"])}</div><div class="tr">{ex["ko"]} <span class="en">· {E(ex["en"])}</span></div></div></div>'
    h += f'<div class="sec chk" data-n="s3" style="left:15mm;top:206mm;width:180mm">{sec_head("§3","Frases del cuaderno","핵심 단어 01–08 예문")}<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:6mm;grid-auto-flow:column;grid-template-rows:repeat(4,auto)">{rows}</div></div>'
    return h + folio(PG0+3)

# ---------- p52 word order 3/3 ----------
def gram3():
    h = gp_head(f'Tema {NUM:02d} — El orden de las palabras · 3/3', 'En la cafetería', f'Practice · scenes · <span class="ko">연습 · 장면 · 이야깃거리</span>')
    s = f'<div class="sec chk" data-n="s4" style="left:15mm;top:43mm;width:180mm">{sec_head("§4","Ordena las palabras","순서대로 다시 써 보세요")}'
    for j, pr in enumerate(D['practice']):
        tiles = ''.join(f'<span class="tl" style="transform:rotate({[-2,1.5,-1,2,-1.5][(j+i)%5]}deg)">{E(t)}</span>' for i, t in enumerate(pr['tiles']))
        s += f'<div class="sr" style="margin-bottom:1.6mm;align-items:center"><span class="nn" style="padding-top:0">{j+1}</span><div style="width:92mm;flex:none">{tiles}</div><span class="mini ko" style="width:36mm;flex:none">{pr["ko"]}</span><span class="line" style="width:42mm"></span></div>'
    s += '</div>'
    sc = ''.join(f'<div class="sr" style="margin-bottom:1.5mm"><span class="nn">{j+1}</span><div><div style="font:600 9.8pt \'Bodoni T\'">{E(x["es"])}</div><div class="tr" style="margin-top:.3mm">{x["ko"]} <span class="en">· {E(x["en"])}</span></div></div></div>' for j, x in enumerate(D['scenes']))
    s += f'<div class="sec chk" data-n="s5" style="left:15mm;top:103mm;width:86mm">{sec_head("§5","Escenas","카페·빵집에서 바로 쓰는 말")}{sc}</div>'
    vr = ''.join(f'<div style="display:flex;gap:2mm;margin-bottom:1.6mm;align-items:baseline"><span style="font:600 9.4pt \'Bodoni T\';width:27mm;flex:none">{v["es"]}</span><span class="mini ko">{v["alt"]}</span></div>' for v in D['variants'])
    s += f'<div class="sec chk" data-n="s6" style="left:108mm;top:103mm;width:87mm">{sec_head("§6","Variantes","지역마다 다른 말")}{vr}<div class="mini ko" style="margin-top:1mm;color:#6b5e50">이 책의 기본 표기는 스페인 표준어예요.</div></div>'
    s += f'<div class="abs chk" data-n="stamp" style="left:163mm;top:146.5mm;width:32mm;height:19.2mm;transform:rotate(-8deg)">{postmark("SALAMANCA · 16 MAY · Nº 09 · ", "CAFÉ", ACC, .55, 6.4)}</div>'
    IMG = {'el café': 'coffee', 'el té': 'tea', 'el azúcar': 'sugar', 'el chocolate': 'chocolate'}
    cg = ''.join(f'<div class="cg chk" data-n="cg" style="left:{15+j*45.6:.1f}mm;top:183mm;width:42mm;transform:rotate({[-1.2,.8,-.6,1.1][j]}deg)"><div class="im"><img src="img/{IMG[c["es"]]}.jpg"></div><div class="es">{c["es"]}</div><div class="en">≈ {c["en"]}</div><div class="ko">{c["note_ko"]}</div></div>' for j, c in enumerate(D['extras']['cognates']))
    s += f'<div class="sec chk" data-n="s7" style="left:15mm;top:171mm;width:180mm">{sec_head("§7","Palabras hermanas","영어와 뿌리가 같은 말")}</div>{cg}'
    ff = D['extras']['false_friend']
    s += f'''<div class="box chk" data-n="ff" style="left:15mm;top:229mm;width:86mm;transform:rotate(-.6deg)"><b class="h">FALSO AMIGO · 헷갈리는 말</b><div style="font:600 11pt 'Bodoni T'">{ff["es"]} <span class="mini" style="font-weight:400">≠ {ff["en"]}</span></div><div class="mini ko" style="margin-top:.8mm;line-height:1.5">{ff["note_ko"]}</div></div>
<div class="box chk" data-n="fun" style="left:108mm;top:229mm;width:60mm;transform:rotate(.6deg)"><b class="h">CURIOSIDAD · ESPAÑA</b><div class="mini ko" style="line-height:1.5">{D["extras"]["fun_fact_ko"]}</div><div class="hand" style="font-size:11pt;color:#7a3b22;margin-top:.8mm">un café cortado, por favor</div></div>
<div class="rnd chk" data-n="funimg" style="left:170mm;top:224mm;width:26mm;height:26mm"><img src="img/fun.jpg"></div>'''
    s += f'<div class="band chk" data-n="band" style="left:15mm;top:257mm;width:180mm;transform:rotate(.3deg)"><div class="frame" style="height:15mm"><img src="img/band.jpg" style="object-position:50% 55%"><div class="cr">masa de pan antes del horno · {E(credit_short("band"))}</div></div></div>'
    ans = ' · '.join(f'{j+1} {E(p["answer"])}' for j, p in enumerate(D['practice']))
    s += f'<div class="ans chk" data-n="ans" style="left:15mm;top:280.5mm;width:180mm;text-align:right">Soluciones · 정답 — {ans}</div>'
    return h + s + folio(PG0+4)

# ---------- p53 créditos ----------
USE = {'cup': f'p.{PG0+1} la taza · p.{PG0+2} etiqueta', 'opener': f'p.{PG0} portada', 'polaroid': f'p.{PG0+1} polaroid «la Plaza Mayor al sol»', 'scene': f'p.{PG0+2} escena (logotipo tapado con etiqueta)',
       'cortado': f'p.{PG0+1} el cortado · p.{PG0+3} foto redonda', 'fun': f'p.{PG0+4} curiosidad', 'band': f'p.{PG0+4} franja'}
def creditos():
    ps = ''
    for k, c in CR.items():
        where = USE.get(k) or f'p.{PG0+1} {W[k]["es"]}' if k in W else USE.get(k, k)
        if k in W and k not in USE: where = f'p.{PG0+1} {W[k]["es"]}' + (f' · p.{PG0+3} miniatura' if W[k]['core'] else '') + (' · p.%d §7' % (PG0+4) if k in ('coffee','tea','sugar','chocolate') else '')
        a = re.sub(r'\s+', ' ', c['artist']).strip() or 'autor desconocido'
        ps += f'<p><b>{E(where)}</b> — {E(c["title"][5:])}. {E(a)} · {E(c["lic"])} · {E(c["page"])} · recortado</p>'
    return f'''<section class="page wp cr s-mercado" style="--acc:{ACC};--note:{NOTE}"><img class="paper" src="shared/paper.jpg">
<div class="hd"><div class="kick2">Vocabulario visual · Español — {NUM:02d} {CH["es"]}</div><h2>Créditos</h2><div class="sub2">Photo credits · <span class="ko">사진 출처와 라이선스</span></div>
<div class="legend">모든 사진은 Wikimedia Commons의 실제 사진이에요(생성 이미지 없음). CC0·퍼블릭 도메인은 자유 이용, CC BY / CC BY-SA는 저작자 표시, BY-SA는 변경본도 같은 조건. 칠판·가격표·영수증·소인·아케이드 띠는 벡터로 그렸어요(사진 아님).</div></div>
<div class="cols" style="top:62mm">{ps}</div>{folio(PG0+5, "Wikimedia Commons")}'''

MEASURE = r'''() => { const mm=v=>v*25.4/96; const out=[];
 document.querySelectorAll('section.page').forEach((pg,pi)=>{ if(!pg.querySelector('.folio')){out.push({page:pi});return;} const pr=pg.getBoundingClientRect();
  const R=e=>{const r=e.getBoundingClientRect();return {l:mm(r.left-pr.left),t:mm(r.top-pr.top),r:mm(r.right-pr.left),b:mm(r.bottom-pr.top)}};
  const els=[...pg.querySelectorAll('.chk,.card')].map(e=>{const rs=[R(e),...[...e.querySelectorAll('.tape,.str,.note')].map(R)];
     return {n:e.dataset.n||('card'+(e.querySelector('.n')||{}).textContent), row:e.dataset.row, l:Math.min(...rs.map(r=>r.l)),t:Math.min(...rs.map(r=>r.t)),r:Math.max(...rs.map(r=>r.r)),b:Math.max(...rs.map(r=>r.b))}});
  const hits=[]; for(let i=0;i<els.length;i++) for(let j=i+1;j<els.length;j++){const a=els[i],b=els[j];
     if(a.n.startsWith('card')&&b.n.startsWith('card')) continue;
     if(a.l<b.r-.2&&b.l<a.r-.2&&a.t<b.b-.2&&b.t<a.b-.2) hits.push(a.n+' x '+b.n);}
  const fol=R(pg.querySelector('.folio')); const low=els.filter(e=>e.b>fol.t-1.5).map(e=>e.n+':'+e.b.toFixed(1));
  const out_of_page=els.filter(e=>e.l<4||e.r>206||e.t<3).map(e=>e.n);
  const ovf=[...pg.querySelectorAll('.lab .w,.lab .l2,.lab .pr,.blk,.tl,.kr .es')].filter(e=>e.scrollWidth>e.clientWidth+1).length;
  const leg=pg.querySelector('.legend'); const heroTop=Math.min(...els.filter(e=>e.row=='h').map(e=>e.t));
  out.push({page:pi, boxes: els.filter(e=>!e.n.startsWith('card')).map(e=>e.n+' '+e.l.toFixed(0)+'-'+e.r.toFixed(0)+' x '+e.t.toFixed(1)+'-'+e.b.toFixed(1)), hits, low, out_of_page, ovf, legend_b: leg?R(leg).b:null, heroTop: isFinite(heroTop)?heroTop:null,
     tagBottom: Math.max(...els.filter(e=>e.row=='t').map(e=>e.b),0), folioTop: fol.t});});
 return out; }'''

def doc(dh, dt):
    body = opener() + palabras(dh, dt) + gram1() + gram2() + gram3() + creditos()
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome'); pg = await b.new_page()
        dh, dt = [0, 0], [0, 0]
        for it in range(3):
            open(f'{C}/ch09.html', 'w', encoding='utf-8').write(doc(dh, dt))
            await pg.goto(f'file://{C}/ch09.html'); await pg.wait_for_timeout(1500)
            m = await pg.evaluate(MEASURE); w = m[1]
            need = w['legend_b'] + 3.0 - w['heroTop']
            if need <= .05: break
            room = w['folioTop'] - 3.0 - w['tagBottom']; s = min(need, max(room, 0))
            dh = [dh[0]+need, dh[1]+need-(need-s)/2]; dt = [dt[0]+s-(need-s)/2*0, dt[1]+s]
            if s < need: dt[0] -= (need - s) / 2
        for x in m: print(json.dumps({k: (round(v, 1) if isinstance(v, float) else v) for k, v in x.items()}, ensure_ascii=False))
        await pg.pdf(path=f'{C}/vocabulario_visual_ch09_cafe_print.pdf', prefer_css_page_size=True, print_background=True)
        await b.close()
asyncio.run(main())

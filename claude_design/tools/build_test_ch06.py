"""ch06 단어 쪽 시험 빌드: v6 CSS·카드 규칙 그대로, 한글 Pretendard, 범례 줄 겹침 자동 보정."""
import asyncio, json, random, re, sys
import yaml
from playwright.async_api import async_playwright

P = sys.argv[1]; T = f'{P}/claude_design/test_ch06'
V6 = open(f'{P}/design/build/v6/index_v6.html', encoding='utf-8').read()
CSS = re.search(r'<style>(.*?)</style>', V6, re.S).group(1)
CSS = CSS.replace('fonts/GowunBatang-Regular.ttf', 'fonts/Pretendard-Regular.ttf').replace('fonts/GowunBatang-Bold.ttf', 'fonts/Pretendard-Bold.ttf')
D = yaml.safe_load(open(f'{P}/es/ch06/text/ch06_text.yaml', encoding='utf-8'))
PROPS = {}
for _p in D['props']: PROPS.setdefault(_p['kind'], _p['lines'])  # 같은 종류가 여럿이면 첫 번째(단어 쪽용)

GL = {'f': 'f', 'm': 'm', 'fpl': 'f pl', 'mpl': 'm pl'}
STRING = '<svg class="str" viewBox="0 0 10 6"><path d="M9 4.6 C6 6 3 1 .2 .6" fill="none" stroke="#9b7b4f" stroke-width=".35"/></svg>'
HPOS = [(14,72,-1.8),(60,69,1.2),(106,73,-.9),(152,71,2.0),(15,133,1.3),(61,136,-1.6),(107,133,2.1),(152,136,-1.0)]
TPOS = [(13,196,-2.2),(44,198,1.6),(75,195,-1.0),(106,199,2.4),(137,196,-1.8),(168,199,1.1),
        (14,240,1.4),(45,242,-2.0),(76,239,1.0),(107,242,-1.3),(138,239,2.2),(168,242,-1.6)]
RED, GREEN = 'rgba(184,64,46,.75)', 'rgba(47,107,69,.78)'

def tape(w=30, h=9, seed=0, col='rgba(226,214,180,.74)', stripes=None):  # v6 base_v6.tape 그대로
    random.seed(seed*31+w)
    pts=[(0,0)]+[(w*k/6+random.uniform(-.8,.8),random.uniform(-.5,.5)) for k in range(1,6)]+[(w,0)]+[(w+random.uniform(-.9,.9),h*k/5) for k in range(1,5)]+[(w,h)]+[(w*k/6+random.uniform(-.8,.8),h+random.uniform(-.5,.5)) for k in range(5,0,-1)]+[(0,h)]+[(random.uniform(-.9,.9),h*k/5) for k in range(4,0,-1)]
    p=' '.join(f'{x:.2f},{y:.2f}' for x,y in pts); cid=f'tc{seed}{w}'.replace('.','')
    st=''
    if stripes:
        st=f'<clipPath id="{cid}"><polygon points="{p}"/></clipPath><g clip-path="url(#{cid})">'+''.join(f'<rect x="{x}" y="-2" width="2" height="{h+4}" fill="{stripes}" transform="skewX(-30)"/>' for x in range(-4,int(w)+8,4))+'</g>'
    return f'<svg class="tape" style="width:{w}mm;height:{h}mm" viewBox="-1 -1 {w+2} {h+2}"><polygon points="{p}" fill="{col}"/>{st}<polygon points="{p}" fill="none" stroke="rgba(150,130,90,.25)" stroke-width=".15"/></svg>'

def shuffle_rot(L, seed):
    random.seed(seed); rs=[r for *_,r in L]; random.shuffle(rs); return [(a,b,r) for (a,b,_),r in zip(L,rs)]

def pron(s): return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)

def card(w, n, pos, hero, extra, dy):
    x, y, r = pos; cls = 'hero' if hero else 'tag'; note = w.get('note') or ''
    nt = ' nt' if (note and not hero) else ''
    cls += nt + (' ph-note' if note else '')
    lab = (f'<div class="lab"><div class="l1"><span class="w">{w["es"]}</span><span class="g g{w["gender"][0]}">{GL[w["gender"]]}</span></div>'
           f'<div class="lp"><span class="pr">[{pron(w["pron"])}]</span></div><div class="l2"><span class="en">{w["en"]}</span> · <span class="ko">{w["ko"]}</span></div></div>')
    return (f'<div class="card {cls}" data-row="{"h" if hero else "t"}" style="left:{x}mm;top:{y+dy}mm;transform:rotate({r}deg)">{extra}'
            f'<span class="n">{n:02d}</span>{f"<div class=note>{note}</div>" if note else ""}<div class="im"><img class="ph" src="img/{w["key"]}.jpg"></div>{lab}</div>')

def price_tag(l1, l2):
    return f'''<svg viewBox="0 0 50 24" style="width:31mm;height:14.9mm"><path d="M9 1 H48 a1.5 1.5 0 0 1 1.5 1.5 V21.5 a1.5 1.5 0 0 1 -1.5 1.5 H9 L1 12 Z" fill="#d8b98a" stroke="#9b7b4f" stroke-width=".35"/>
<circle cx="8.5" cy="12" r="1.7" fill="#f1e6cc" stroke="#9b7b4f" stroke-width=".35"/><path d="M8.5 12 C3 8 -2 14 -6 9" fill="none" stroke="#9b7b4f" stroke-width=".35"/>
<text x="29" y="10" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="6.2" fill="#3a2a22">{l1}</text>
<text x="29" y="18.6" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="7.6" fill="#b8402e">{l2}</text></svg>'''

def page(dh, dt):
    ch = D['chapter']; words = D['words']
    star = [w for w in words if w['core']]; rest = [w for w in words if not w['core']]
    hp = shuffle_rot(HPOS, 6); tp = shuffle_rot(TPOS, 7); cs = ''
    for n, w in enumerate(star):
        cs += card(w, n+1, hp[n], 1, tape(18,5.5,n+60,col='rgba(250,246,238,.92)',stripes=RED if n%2==0 else GREEN), dh[n//4])
    for n, w in enumerate(rest):
        cs += card(w, n+9, tp[n], 0, '<span class="hole"></span>'+STRING, dt[n//6])
    ck = PROPS['chalk']
    props = f'''<div class="chalk" style="left:116mm;top:12mm;width:50mm;height:42mm;transform:rotate(1.2deg)"><div class="t">{ck[0]}</div>
<div class="r" style="margin-top:1.6mm">{ck[1]}</div><div class="k" style="margin-top:1.2mm">{ck[2]}</div>
<svg viewBox="0 0 40 6" style="width:40mm;height:4mm;margin-top:1.4mm"><path d="M1 3 q5 -3 10 0 t10 0 t10 0 t8 0" fill="none" stroke="#f6e6a8" stroke-width=".5" opacity=".8"/></svg><div class="r" style="font-size:10.5pt">{ck[3]}</div></div>
<div class="pol" style="left:170mm;top:15mm;width:30.8mm;transform:rotate(5deg)"><img src="img/boqueria.jpg" style="width:26mm;height:26mm;object-fit:cover"><div class="c" style="font-size:10pt">{PROPS["polaroid"][0]}</div></div>
<div class="abs" style="left:176mm;top:12mm;transform:rotate(-4deg)">{tape(18,5.5,93,col='rgba(250,246,238,.92)',stripes=GREEN)}</div>
<div class="abs prop-price" style="left:119mm;top:56.3mm;transform:rotate(-3deg)">{price_tag(*PROPS["price"])}</div>
<div class="hand abs" style="left:154mm;top:59mm;font-size:11pt;color:#7a3b22;transform:rotate(-3deg)">{PROPS["hand"][0]}</div>'''
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<section class="page wp s-mercado" style="--acc:#b8402e;--note:#2f6b45"><img class="paper" src="shared/paper.jpg">
<div class="hd"><div class="kick2">Tema {ch["num"]:02d} — Comer y beber</div><h2>{ch["es"]}</h2><div class="sub2">{ch["en"]} · <span class="ko">{ch["ko"]}</span></div>
<div class="legend">f femenino · m masculino · pl plural &nbsp;—&nbsp; <span class="ko">[ ] 한글 발음, <b>굵은 글자</b> = 강세 · 01–08 핵심</span></div></div>
{props}{cs}
<div class="folio"><span>{ch["num"]:02d} — {ch["es"]} · <span class="sk">Mercado</span></span><span>fotos · Wikimedia Commons</span><span>Vocabulario visual · 31</span></div></section></body></html>'''

MEASURE = '''() => { const mm = v => v*25.4/96; const R = e => e.getBoundingClientRect();
 const leg = R(document.querySelector('.legend')); const hd = R(document.querySelector('.hd'));
 const box = el => { const rs=[R(el), ...[...el.querySelectorAll('.tape,.str,.note')].map(R)];
   return {top:Math.min(...rs.map(r=>r.top)), bottom:Math.max(...rs.map(r=>r.bottom)), left:Math.min(...rs.map(r=>r.left)), right:Math.max(...rs.map(r=>r.right))}; };
 const cards=[...document.querySelectorAll('.card')].map(el=>({row:el.dataset.row, ...box(el)}));
 const props=[...document.querySelectorAll('.chalk,.pol,.prop-price,.hand.abs')].map(el=>({cls:el.className, ...box(el)}));
 const folio=R(document.querySelector('.folio'));
 const over = (a,b) => a.left<b.right && b.left<a.right && a.top<b.bottom && b.top<a.bottom;
 const hits=[]; const all=[{cls:'header',top:hd.top,bottom:leg.bottom,left:hd.left,right:hd.right}, ...props];
 for (const c of cards) for (const p of all) if (over(c,p)) hits.push(p.cls+' x card');
 for (let i=0;i<all.length;i++) for (let j=i+1;j<all.length;j++) if (over(all[i],all[j])) hits.push(all[i].cls+' x '+all[j].cls);
 const over_text=[...document.querySelectorAll('.lab .w,.lab .l2,.lab .pr')].filter(e=>e.scrollWidth>e.parentElement.parentElement.clientWidth+1).length;
 return {legend_bottom:mm(leg.bottom), hero_top:mm(Math.min(...cards.filter(c=>c.row=='h').map(c=>c.top))),
   hero1_bottom:mm(Math.max(...cards.filter((c,i)=>c.row=='h'&&i<4).map(c=>c.bottom))), hero2_top:mm(Math.min(...cards.filter((c,i)=>c.row=='h'&&i>=4).map(c=>c.top))),
   hero_bottom:mm(Math.max(...cards.filter(c=>c.row=='h').map(c=>c.bottom))), tag_top:mm(Math.min(...cards.filter(c=>c.row=='t').map(c=>c.top))),
   tag_bottom:mm(Math.max(...cards.filter(c=>c.row=='t').map(c=>c.bottom))), folio_top:mm(folio.top), hits, over_text}; }'''

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome'); pg = await b.new_page()
        dh, dt = [0, 0], [0, 0]
        for it in range(4):
            open(f'{T}/ch06_palabras.html', 'w', encoding='utf-8').write(page(dh, dt))
            await pg.goto(f'file://{T}/ch06_palabras.html'); await pg.wait_for_timeout(1200)
            m = await pg.evaluate(MEASURE); print(it, dh, dt, json.dumps({k:(round(v,1) if isinstance(v,float) else v) for k,v in m.items()}, ensure_ascii=False))
            need = m['legend_bottom'] + 3.0 - m['hero_top']          # 범례 아래 3mm 띄우기
            if need <= 0.05: break
            room = m['folio_top'] - 3.0 - m['tag_bottom']           # 아래쪽 남는 공간
            d = max(need, 0); s = min(d, max(room, 0))
            dh = [dh[0]+d, dh[1]+d]; dt = [dt[0]+s, dt[1]+s]
            if s < d:  # 아래 여유가 모자라면 단어 줄 사이 간격을 줄여서 메움
                dh[1] -= (d - s) / 2; dt[0] -= (d - s) / 2
        await pg.pdf(path=f'{T}/ch06_palabras_claude.pdf', prefer_css_page_size=True, print_background=True)
        await b.close()
asyncio.run(main())

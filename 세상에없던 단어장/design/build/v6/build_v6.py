import json,sys,os
sys.path.insert(0,'/workspace/trilingual/es/v6/_build')
from base_v6 import *
import base_v6 as B
from toc_v6 import CH as PLAN,PARTS,SKINS,GR,ROMAN
D3=json.load(open('/workspace/trilingual/es/ch01_bathroom_v3/data.json'));O=D3['order'];TF=D3['textfix']
IT={i['k']:i for i in V3}
CSS6=CSS+"""
/* ===== v6: billete prop ===== */
.bil{position:absolute;background:#f6efdc;border:.25mm solid rgba(31,58,95,.45);border-radius:1mm;box-shadow:.4mm .6mm 0 rgba(60,40,20,.14);font-family:'Special Elite';color:#1f3a5f;overflow:hidden}
.bil .st{position:absolute;left:0;top:0;bottom:0;width:6mm;background:repeating-linear-gradient(0deg,#1f3a5f 0 .5mm,transparent .5mm 1.6mm);opacity:.85}
.bil .r1{position:absolute;left:8mm;top:1.6mm;font-size:7pt;letter-spacing:.12em}
.bil .r2{position:absolute;left:8mm;top:4.8mm;font-size:8.6pt;letter-spacing:.04em;white-space:nowrap}
.bil .r3{position:absolute;left:8mm;top:9.4mm;font-size:7pt;letter-spacing:.06em;white-space:nowrap}
.bil .dec{position:absolute;right:1.6mm;bottom:1mm;font:400 7pt 'Caveat';color:#7a3b22}
.bil .perf{position:absolute;right:11mm;top:1mm;bottom:1mm;border-left:.3mm dashed rgba(31,58,95,.4)}
.s-pasaporte .im img.cut{max-width:100%;max-height:100%;object-fit:contain}
.s-pasaporte .hero.cutc .im,.s-pasaporte .tag.cutc .im{background:transparent}
/* ===== v6: grammar pages (museo skin) ===== */
.gp .hd{width:180mm}.gp h2{font-size:34pt}
.lead{position:absolute;left:15mm;width:180mm;font:400 8.6pt/1.55 'Gowun';color:#2e2822}.lead b{font-weight:700}.lead u{text-decoration:none;border-bottom:.45mm solid #a4533a}
.sec{position:absolute}
.sh{display:flex;align-items:baseline;gap:2mm;margin-bottom:2.2mm;border-bottom:.2mm solid rgba(120,80,50,.35);padding-bottom:1mm}
.sh .no{font:400 9pt 'Special Elite';color:var(--acc)}.sh .t{font:400 italic 14pt 'Bodoni D'}.sh .k{font:400 8.4pt 'Gowun';color:#4a4038}
.row{display:flex;align-items:center;gap:2mm;margin-bottom:1.6mm}
.ic{width:11mm;height:11mm;display:flex;align-items:center;justify-content:center;flex:none}.ic img{max-width:100%;max-height:100%}
.ch{display:inline-block;padding:.5mm 1.6mm;border-radius:.8mm;font:600 9.6pt 'Bodoni T';border:.25mm solid rgba(60,40,20,.25);background:#fbf7ee;white-space:nowrap}
.ch.n{background:#f4e0d6;border-color:#c98a72}.ch.a{background:#dbe9e5;border-color:#7fa9a1}
.ko .ch,.ch.k{font:400 8.4pt 'Gowun'}
.mini{font:400 7.5pt/1.4 'Jost';color:#4a4038}.mini.ko{font-family:'Gowun';font-size:7.8pt}
.end{color:#a4533a;font-weight:700}
.gtag{font:500 7pt 'Jost';letter-spacing:.04em;padding:.2mm 1.2mm;border-radius:.6mm;color:#fff}
.dc{position:absolute;background:#fbfaf6;padding:2mm 2.4mm;box-shadow:.3mm .5mm 0 rgba(60,40,20,.12);width:42mm}
.dc .im2{height:13mm;display:flex;align-items:center;justify-content:center}.dc .im2 img{max-height:100%;max-width:100%}
.dc .es{font:600 9.6pt 'Bodoni T';margin-top:1.4mm}.dc .es i{font-style:normal;color:#a4533a}
.dc .lit{font:400 7.2pt 'Jost';color:#4a4038;margin-top:.6mm}.dc .kl{font:400 7.6pt 'Gowun';margin-top:.4mm}
.blk{display:inline-flex;flex-direction:column;align-items:center;padding:.8mm 1.8mm .7mm;margin-right:1.2mm;border-radius:.8mm;background:#fbf7ee;border:.25mm solid rgba(60,40,20,.22)}
.blk .e{font:600 10pt 'Bodoni T';white-space:nowrap}.blk .g{font:400 7pt 'Gowun';color:#4a4038;white-space:nowrap;margin-top:.3mm}
.blk.hi{background:#f4e0d6;border-color:#a4533a}.blk.hi .e{color:#7a2f1c}
.sr{display:flex;align-items:flex-start;gap:2.4mm;margin-bottom:2.4mm}
.sr .nn{font:400 9pt 'Special Elite';color:var(--acc);width:5mm;padding-top:1.2mm;flex:none}
.sr .tr{font:400 7.8pt/1.4 'Gowun';margin-top:1mm}.sr .tr .en{font-family:'Jost';color:#5a4f44;font-size:7.4pt}
.sr .nt{font:400 7.4pt/1.35 'Gowun';color:#2f4d84;margin-top:.4mm}
.box{position:absolute;background:#fbfaf6;padding:2.6mm 3mm;box-shadow:.3mm .5mm 0 rgba(60,40,20,.12)}
.box b.h{display:block;font:500 7pt 'Jost';letter-spacing:.2em;color:var(--acc);margin-bottom:1mm}
.line{display:inline-block;border-bottom:.25mm dotted #8a7a68;width:62mm;height:5mm;vertical-align:bottom;margin-left:2mm}
.ans{position:absolute;transform:rotate(180deg);font:400 7pt 'Jost';color:#6b5e50}
.keyl{position:absolute;left:15mm;width:180mm;font:400 7.4pt/1.45 'Gowun';color:#3b342d;border-top:.2mm solid rgba(120,80,50,.35);padding-top:1.4mm}
/* ===== Índice ===== */
.toc .hd{width:180mm}
.part{position:absolute;left:15mm;width:180mm;display:flex;align-items:baseline;gap:2.4mm;border-bottom:.3mm solid #1f1b17;padding-bottom:.6mm}
.part .pn{font:400 9pt 'Special Elite';color:#a4533a}.part .pt{font:500 7.5pt 'Jost';letter-spacing:.24em;text-transform:uppercase}.part .pk{font:400 8pt 'Gowun';color:#4a4038}
.tr6{position:absolute;left:15mm;width:180mm;height:7.8mm;box-sizing:border-box;padding-top:.5mm;display:grid;grid-template-columns:9mm 52mm 92mm 27mm;align-items:start;border-bottom:.15mm solid rgba(120,80,50,.25)}
.tr6 .n{font:400 10.5pt/1 'Special Elite';padding-top:.3mm}
.tr6 .es{font:400 italic 10.5pt/1.02 'Bodoni D','Gowun';white-space:nowrap}.tr6 .ko2{font:400 7pt/1.2 'Gowun';color:#4a4038;margin-top:.3mm}
.tr6 .gr{font:400 7.2pt/1.2 'Gowun';color:#1f1b17;white-space:nowrap;overflow:hidden;text-overflow:clip}.tr6 .ex{font:400 italic 8pt/1.15 'Bodoni D','Gowun';color:#5a4f44;margin-top:.3mm;white-space:nowrap}
.tr6 .ci{font:500 7pt/1.2 'Jost';letter-spacing:.16em;text-transform:uppercase;text-align:right;padding-top:.3mm}.tr6 .sk{font:400 7pt/1.2 'Jost';text-align:right;margin-top:.5mm}
.tr6.here{background:linear-gradient(90deg,rgba(164,83,58,.10),rgba(164,83,58,0) 70%)}
.here-chip{font:500 7pt 'Jost';letter-spacing:.1em;color:#fff;background:#a4533a;border-radius:.6mm;padding:.1mm 1mm;margin-left:1.4mm;vertical-align:1px;font-style:normal}
/* ===== Créditos ===== */
.cr .hd{width:180mm}.cr .legend{white-space:normal;width:180mm}.cols{position:absolute;left:15mm;top:58mm;width:180mm;height:222mm;column-count:2;column-gap:7mm;column-fill:auto;font:400 7pt/1.32 'Jost';color:#2e2822}
.cols h4{font:500 7pt 'Jost';letter-spacing:.2em;text-transform:uppercase;color:#a4533a;margin:1.6mm 0 .8mm;break-after:avoid}
.cols p{margin-bottom:1mm;break-inside:avoid;overflow-wrap:anywhere}.cols p b{font-weight:500}
"""
B.CSS=CSS6
# ---------- shared ----------
def wp(ch,cards,props,pg,cls_extra=''):
    return wordpage(ch,cards,props,pg).replace(f'class="page wp {ch["cls"]}"',f'class="page wp {ch["cls"]}{cls_extra}"',1)
# ---------- ch01 ----------
def ch01():
    ch=dict(n=1,dir='ch01',title='El baño',en='The bathroom',ko='욕실',part='En casa',acc='#a4533a',note='#2f4d84',cls='s-museo',skin='Museo · Alhambra',
            stop='Parada 01 · Granada',place='La Alhambra, baños del Palacio de Comares',hand='primero, el baño — 20 palabras para el viaje',handcol='#f3e3c4',
            opcred='Foto: Daderot · CC0 · Wikimedia Commons',opos='50% 50%',opimg='opener_v6.jpg',
            badge=f'<div style="width:46mm;height:27.6mm;transform:rotate(-8deg)">{postmark("Nº 01 · EL BAÑO · 3 MAY · ","GRANADA","#ffffff",.85,6)}</div>')
    star=[i for i in V3 if i['star']];rest=[i for i in V3 if not i['star']]
    hp=[(x,y-3 if i<4 else y+2,r) for i,(x,y,r) in enumerate(HPOS)];cs=''
    for n,i in enumerate(star):
        k=i['k']
        if k in ROT: d,w=ROT[k];img=f'<img class="rot" src="ch01/img/t_{i["img"]}" style="width:{w}mm;transform:translate(-50%,-50%) rotate({d}deg)">'
        else: img=f'<img class="cut" src="ch01/img/t_{i["img"]}">'
        mus=f'<div class="mus"><span>Nº {n+1:02d}</span><span class="ln"></span><span>Granada</span></div>'
        c=card(k,i['es'],i['g'],i['p'],i['en'],i['ko'],n+1,hp[n],1,img,NOTE1.get(k),ph=False,extra=tape(18,5.5,n));cs+=c.replace('<div class="lab">',mus+'<div class="lab">',1)
    for n,i in enumerate(rest):
        cs+=card(i['k'],i['es'],i['g'],i['p'],i['en'],i['ko'],n+9,TPOS[n],0,f'<img class="cut" src="ch01/img/t_{i["img"]}">',NOTE1.get(i['k']),ph=False,extra='<span class="hole"></span>')
    props=f'''<div class="print" style="left:117mm;top:13mm;width:55.2mm;height:41.2mm;transform:rotate(-2.4deg)"><img src="ch01/img/print_bench.jpg" style="width:50mm;height:36mm;object-fit:cover"></div>
<div class="abs" style="left:112mm;top:12mm;transform:rotate(-38deg)">{tape(20,6,91)}</div>
<div class="pol" style="left:163mm;top:24mm;width:36.8mm;transform:rotate(4deg)"><img src="ch01/img/pol_stars.jpg" style="width:32mm;height:32mm;object-fit:cover"><div class="c">estrellas de luz</div></div>
<div class="abs" style="left:172mm;top:21mm;transform:rotate(-6deg)">{tape(18,5.5,92)}</div>
<div class="wall" style="left:118mm;top:55mm;width:42mm;padding:1.4mm 2.4mm;transform:rotate(-1deg)"><b>CAT. 01–02 · AZULEJOS Y ESTRELLAS</b>Baño de Comares, la Alhambra</div>
<div class="abs" style="left:73mm;top:17mm;width:40mm;height:24mm;transform:rotate(-12deg)">{postmark('CORREO · GRANADA · 3 MAY · ','ESPAÑA','#2f4d84',.55,6.4)}</div>'''
    return ch,opener(ch)+wordpage(ch,cs,props,3)+gram1(ch)+gram2(ch)
def ic(k,h=11): return f'<span class="ic" style="width:{h}mm;height:{h}mm"><img src="ch01/img/t_{IT[k]["img"]}"></span>'
def gp_head(ch,kick,title,sub):
    return f'''<section class="page wp gp {ch["cls"]}" style="--acc:{ch["acc"]};--note:{ch["note"]}"><img class="paper" src="shared/paper.jpg">
<div class="hd"><div class="kick2">{kick}</div><h2>{title}</h2><div class="sub2">{sub}</div></div>'''
def folio(ch,pg,mid='gramática visual'):
    return f'<div class="folio"><span>{ch["n"]:02d} — {ch["title"]} · <span class="sk">{ch["skin"]}</span></span><span>{mid}</span><span>Vocabulario visual · {pg}</span></div></section>'
def gram1(ch):
    h=gp_head(ch,'Tema 01 — El orden de las palabras · 1/2','El orden de las palabras','Word order · <span class="ko">어순 — 명사가 먼저, 꾸밈은 뒤에</span>')
    h+=f'<div class="lead" style="top:41mm">{TF["lead_c"].replace("적갈색 밑줄","적갈색 칸")}</div>'
    # §1 noun + adjective
    ADJ_IC={'la toalla':'towel','el jabón':'soap','las toallas':'towel'}
    s='<div class="sec" style="left:15mm;top:53mm;width:86mm"><div class="sh"><span class="no">§1</span><span class="t">Nombre + adjetivo</span><span class="k">명사 + 형용사</span></div>'
    for (n,a),en,ko in O['adj']:
        kn,ka=ko.split(' ',1)[::-1] if False else (ko.split(' ')[-1],' '.join(ko.split(' ')[:-1]))
        s+=f'<div class="row">{ic(ADJ_IC[n])}<div><div><span class="ch n">{n}</span> <span class="ch a">{a}</span></div><div style="margin-top:.8mm"><span class="ch k a">{ka}</span> <span class="ch k n">{kn}</span> <span class="mini" style="margin-left:1mm">{en}</span></div></div></div>'
    s+='<div class="mini ko" style="margin-top:.6mm">같은 색끼리 짝이에요. 스페인어는 <b>명사</b> → <b>형용사</b>, 한국어·영어는 그 반대.</div></div>'
    # §2 agreement
    AG_IC={'el espejo limpio':'mirror','la toalla limpia':'towel','los peines limpios':'comb','las tijeras limpias':'scissors'}
    GC={'m':'#3e5a86','f':'#a4533a','m pl':'#3e5a86','f pl':'#a4533a'}
    s+='<div class="sec" style="left:108mm;top:53mm;width:87mm"><div class="sh"><span class="no">§2</span><span class="t">Concordancia</span><span class="k">성·수 일치</span></div>'
    for es,g,ko in O['agree']:
        w=es.split(' ');art,nn,adj=w[0],w[1],w[2]
        def endh(x,suf): return x[:-len(suf)]+f'<span class="end">{suf}</span>'
        suf={'m':'o','f':'a','m pl':'os','f pl':'as'}[g]; asuf={'m':'o','f':'a','m pl':'os','f pl':'as'}[g]
        nsuf=suf if nn.endswith(suf) else ('es' if nn.endswith('es') else nn[-1])
        s+=f'<div class="row">{ic(AG_IC[es],10)}<div style="flex:1"><span class="ch" style="font-weight:600">{endh(art, art[-1] if g!="m" else "l") if False else art} {endh(nn,nsuf) if nn.endswith(suf) else nn} {endh(adj,asuf)}</span> <span class="gtag" style="background:{GC[g]}">{g}</span><div class="mini ko" style="margin-top:.5mm">{ko}</div></div></div>'
    s+='<div class="mini ko" style="margin-top:.4mm">형용사 끝이 명사를 따라 <b>-o / -a / -os / -as</b>로 바뀌어요.</div></div>'
    # §3 de-compounds
    DE_IC={'el cepillo':'toothbrush','la pasta':'toothpaste','el secador':'hairdryer','el papel':'toiletpaper'}
    KL={'el cepillo':'솔 · ~의 · 이 = 칫솔','la pasta':'반죽 · ~의 · 이 = 치약','el secador':'말리는 것 · ~의 · 머리 = 드라이어','el papel':'종이 · 위생의 = 화장지'}
    s+='<div class="sec" style="left:15mm;top:122mm;width:180mm"><div class="sh"><span class="no">§3</span><span class="t">Palabras con «de»</span><span class="k">de로 잇는 말 · 뒤에서 꾸미기</span></div></div>'
    for j,(a,b,lit,en,ko) in enumerate(O['de']):
        s+=f'<div class="dc" style="left:{15+j*45.6}mm;top:131mm;transform:rotate({[-1.2,.8,-.6,1.1][j]}deg)"><div class="im2"><img src="ch01/img/t_{IT[DE_IC[a]]["img"]}"></div><div class="es">{a} <i>{b}</i></div><div class="lit">{lit} · {en}</div><div class="kl">{KL[a]}</div></div>'
    # §4 word blocks
    GL={'o1':{3:'이(치아)들'},'o3':{0:'(나는) 필요하다'}}
    s+='<div class="sec" style="left:15mm;top:171mm;width:180mm"><div class="sh"><span class="no">§4</span><span class="t">Bloques de palabras</span><span class="k">단어 블록 + 한국어 직역 · 색칸 = 영어와 자리가 다른 곳</span></div>'
    for t in O['sent']:
        bl=''.join(f'<span class="blk{" hi" if i in t["hi"] else ""}"><span class="e">{e}</span><span class="g">{GL.get(t["id"],{}).get(i,g)}</span></span>' for i,(e,g) in enumerate(t['b']))
        s+=f'<div class="sr"><span class="nn">{t["id"][1]}</span><div style="width:92mm;flex:none">{bl}</div><div><div class="tr">{t["ko"]} <span class="en">· {t["en"]}</span></div><div class="nt">{t["note"]}</div></div></div>'
    s+='</div>'
    s+=f'<div class="keyl" style="top:271mm">{TF["key"]}</div>'
    return h+s+folio(ch,4)
def gram2(ch):
    h=gp_head(ch,'Tema 01 — El orden de las palabras · 2/2','Pronombres y sujeto','Pronouns &amp; subject · <span class="ko">me의 자리, 생략되는 주어</span>')
    s='<div class="sec" style="left:15mm;top:42mm;width:180mm"><div class="sh"><span class="no">§5</span><span class="t">¿Dónde va «me»?</span><span class="k">대명사 me의 자리</span></div>'
    for es,where,ko in O['clitic']:
        w=es.rstrip('.').split(' ');bl=''
        for x in w:
            hi='me' in x.lower() and x.lower()!='dientes'
            if x.endswith('me') and len(x)>2: bl+=f'<span class="blk"><span class="e">{x[:-2]}<span class="end">me</span></span><span class="g">&nbsp;</span></span>'
            else: bl+=f'<span class="blk{" hi" if x=="Me" else ""}"><span class="e">{x}</span><span class="g">&nbsp;</span></span>'
        bl=bl.replace('<span class="g">&nbsp;</span>','')
        s+=f'<div class="sr" style="margin-bottom:1.6mm"><div style="width:96mm;flex:none">{bl}</div><div><div class="tr" style="margin-top:.6mm"><b style="color:#a4533a">{where}</b> · {ko}</div></div></div>'
    s+=f'<div class="mini ko" style="width:180mm;margin-top:.6mm;line-height:1.5">{TF["small5"]}</div></div>'
    # §6 subject drop (left)
    s+='<div class="sec" style="left:15mm;top:93mm;width:86mm"><div class="sh"><span class="no">§6</span><span class="t">Sin sujeto</span><span class="k">주어 생략</span></div>'
    for es,ko in O['subj']:
        p,rest=es.split(') ');p=p+')';v=rest.rstrip('.').split(' ')
        verb=v[1];stem={'ducho':('duch','o'),'duchas':('duch','as'),'ducha':('duch','a')}[verb]
        s+=f'<div class="row"><span class="ch" style="color:#9a8f82;font-weight:400">{p}</span><span class="ch">{v[0]} {stem[0]}<span class="end">{stem[1]}</span>.</span><span class="mini ko">{ko}</span></div>'
    s+=f'<div class="mini ko" style="line-height:1.5;margin-top:.8mm">{TF["small6"]}</div></div>'
    # §8 variants (right)
    s+='<div class="sec" style="left:108mm;top:93mm;width:87mm"><div class="sh"><span class="no">§7</span><span class="t">Variantes</span><span class="k">지역마다 다른 말</span></div>'
    for es,v in O['variants']:
        s+=f'<div style="display:flex;gap:2mm;margin-bottom:1.3mm;align-items:baseline"><span style="font:600 9pt \'Bodoni T\';width:30mm;flex:none">{es}</span><span class="mini ko">{v.replace("(같은 뜻)","· 같은 뜻").replace(" (",", ").replace(")","")}</span></div>'
    s+='<div class="mini ko" style="margin-top:1mm;color:#6b5e50">이 책의 기본 표기는 스페인 표준어예요.</div></div>'
    # §8 practice
    s+='<div class="sec" style="left:15mm;top:152mm;width:180mm"><div class="sh"><span class="no">§8</span><span class="t">Ordena las palabras</span><span class="k">순서대로 다시 써 보세요</span></div>'
    for j,(sc,ans,ko) in enumerate(O['practice']):
        tiles=''.join(f'<span class="blk" style="transform:rotate({[-2,1.5,-1,2,-1.5][(j+i)%5]}deg)"><span class="e">{w}</span></span>' for i,w in enumerate(sc))
        s+=f'<div class="sr" style="margin-bottom:2mm;align-items:center"><span class="nn" style="padding-top:0">{j+1}</span><div style="width:70mm;flex:none">{tiles}</div><span class="mini ko" style="width:34mm;flex:none">{ko}</span><span class="line"></span></div>'
    s+='</div>'
    ff=D3['falsefriend']
    s+=f'''<div class="box" style="left:15mm;top:222mm;width:86mm;transform:rotate(-.8deg)"><b class="h">FALSO AMIGO · 헷갈리는 말</b><div style="font:600 11pt 'Bodoni T'">{ff[0]} <span class="mini" style="font-weight:400">≠ {ff[1]}</span></div><div class="mini ko" style="margin-top:.8mm;line-height:1.5">{ff[2]}</div></div>
<div class="wall" style="left:108mm;top:222mm;width:58mm;transform:rotate(.8deg)"><b>CAT. 01 · CURIOSIDAD</b><span class="ko" style="font-size:7.6pt;line-height:1.5">{D3["funfact"]}</span></div>
<div class="abs" style="left:158mm;top:232mm;width:40mm;height:24mm;transform:rotate(-10deg)">{postmark('CORREO · GRANADA · 3 MAY · ','ESPAÑA','#2f4d84',.5,6.4)}</div>'''
    ans=' · '.join(f'{j+1} {a}' for j,(_,a,_) in enumerate(O['practice']))
    s+=f'<div class="ans" style="left:15mm;top:262mm;width:180mm;text-align:right">Soluciones · 정답 — {ans}</div>'
    return h+s+folio(ch,5)
# ---------- ch02 ----------
def ch02():
    ch=dict(n=2,dir='ch02',title='La cocina',en='The kitchen',ko='부엌',part='En casa',acc='#b8402e',note='#2f6b45',cls='s-mercado',skin='Mercado',
            stop='Parada 02 · València',place='Mercado Central de València, la fachada',hand='al mercado, y luego a la cocina',handcol='#f6e6a8',
            opcred='Foto: Bene Riobó · CC BY-SA 4.0 · Wikimedia Commons',opimg='opener_v6.jpg',
            badge='''<svg viewBox="0 0 44 26" style="width:44mm;height:26mm;transform:rotate(-6deg)"><path d="M8 1 H42 a1.5 1.5 0 0 1 1.5 1.5 V23.5 a1.5 1.5 0 0 1 -1.5 1.5 H8 L1 13 Z" fill="none" stroke="#fff" stroke-width=".7" opacity=".9"/><circle cx="8" cy="13" r="1.6" fill="none" stroke="#fff" stroke-width=".6" opacity=".9"/>
<text x="26" y="10" text-anchor="middle" font-family="Special Elite" font-size="3" fill="#fff" letter-spacing=".5" opacity=".92">MERCADO · 5 MAY</text><text x="26" y="19" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="8.4" fill="#fff" opacity=".95">la cocina</text></svg>''')
    hx=lambda n: tape(18,5.5,n+20,col='rgba(250,246,238,.92)',stripes='rgba(184,64,46,.75)')
    tx=lambda n: '<span class="hole"></span>'+STRING
    cs=photo_cards(ch,CH02,NOTE02,hx,tx,7)
    props=f'''<div class="chalk" style="left:116mm;top:12mm;width:50mm;height:44mm;transform:rotate(1.2deg)"><div class="t">Hoy en la cocina</div>
<div class="r" style="margin-top:1.6mm">la olla · la sartén<br>la paellera · el mortero</div><div class="k" style="margin-top:1.2mm">냄비, 프라이팬, 파에야 팬</div>
<svg viewBox="0 0 40 6" style="width:40mm;height:4mm;margin-top:1.4mm"><path d="M1 3 q5 -3 10 0 t10 0 t10 0 t8 0" fill="none" stroke="#f6e6a8" stroke-width=".5" opacity=".8"/></svg><div class="r" style="font-size:10.5pt">5 de mayo</div></div>
<div class="pol" style="left:170mm;top:15mm;width:30.8mm;transform:rotate(5deg)"><img src="ch02/img/pol1.jpg" style="width:26mm;height:26mm;object-fit:cover"><div class="c" style="font-size:10pt">Mercat Central</div></div>
<div class="abs" style="left:176mm;top:12mm;transform:rotate(-4deg)">{tape(18,5.5,93,col='rgba(250,246,238,.92)',stripes='rgba(184,64,46,.75)')}</div>
<div class="hand abs" style="left:168mm;top:52mm;font-size:11.5pt;color:#7a3b22;transform:rotate(-3deg)">fruta, pescado y más</div>'''
    return ch,opener(ch)+wordpage(ch,cs,props,7)
# ---------- ch11 ----------
CUT11={'bus','taxi','ticket','suitcase','plane','bike','car','moto','lights','backpack','helmet'}
def photo_cards6(ch,L,NOTE,hx,tx,seed):
    star=[x for x in L if x[6]];rest=[x for x in L if not x[6]]
    hp=shuffle_rot(HPOS,seed);tp=shuffle_rot(TPOS,seed+1);cs=''
    for grp,pos,off,hero,ex in ((star,hp,1,1,hx),(rest,tp,9,0,tx)):
        for n,(k,es,g,p,en,ko,s,o) in enumerate(grp):
            if k in CUT11: img=f'<img class="cut" src="{ch["dir"]}/img/c_{k}.png">'
            else: img=f'<img class="{"pp" if o=="p" else "ph"}" src="{ch["dir"]}/img/{k}.jpg">'
            c=card(k,es,g,p,en,ko,n+off,pos[n],hero,img,NOTE.get(k),ph=(k not in CUT11),extra=ex(n))
            if k in CUT11: c=c.replace('class="card ','class="card cutc ',1)
            cs+=c
    return cs
def billete():
    arrow='<svg viewBox="0 0 8 3" style="width:5mm;height:2mm;vertical-align:.2mm"><path d="M0 1.5 H7 M5.4 .2 L7.3 1.5 L5.4 2.8" fill="none" stroke="#1f3a5f" stroke-width=".45"/></svg>'
    return f'''<div class="bil" style="left:16mm;top:53.6mm;width:62mm;height:15mm;transform:rotate(-1.5deg)"><div class="st"></div>
<div class="r1">BILLETE · TICKET · 승차권</div><div class="r2">MADRID-ATOCHA {arrow} TOLEDO</div><div class="r3">14 MAY · 09:20 · COCHE 4 · PLAZA 07A</div><div class="dec">decorativo</div></div>'''
def ch11():
    ch=dict(n=11,dir='ch11',title='El transporte',en='Getting around',ko='교통',part='La ciudad y el viaje',acc='#1f3a5f',note='#b8332b',cls='s-pasaporte',skin='Pasaporte · Cartel retro',
            stop='Parada 11 · Madrid',place='Estación de Atocha, el jardín tropical',hand='¿a dónde vamos hoy? — en tren, en metro, a pie',handcol='#f3d58a',
            opcred='Foto: Nan Palmero · CC BY 2.0 · Wikimedia Commons',
            badge=f'<div style="width:46mm;height:24mm;transform:rotate(7deg)">{rectstamp("ENTRADA · ENTRY","MADRID","12 MAY · Nº 11","#ffffff",.9,46,24)}</div>')
    hx=lambda n:''
    tx=lambda n:'<span class="hole"></span><svg class="str" viewBox="0 0 8 8"><path d="M4 7 C1 4 6 2 3 0" fill="none" stroke="#9b7b4f" stroke-width=".4"/></svg>'
    cs=photo_cards6(ch,CH11,NOTE11,hx,tx,11)
    props=f'''<div class="poster" style="left:117mm;top:8mm;width:36mm;height:48mm;transform:rotate(-2.5deg)">{poster()}</div>
<div class="abs" style="left:125mm;top:7mm;transform:rotate(-8deg)">{tape(18,5.5,94)}</div>
<div class="pol" style="left:160mm;top:14mm;width:36.8mm;transform:rotate(4.5deg)"><img src="ch11/img/pol1.jpg" style="width:32mm;height:32mm;object-fit:cover"><div class="c">km 0, Puerta del Sol</div></div>
<div class="abs" style="left:169mm;top:11mm;transform:rotate(3deg)">{tape(18,5.5,95)}</div>
{billete()}
'''
    return ch,opener(ch)+wordpage(ch,cs,props,9)
# ---------- Índice ----------
def indice():
    h='''<section class="page wp toc s-museo" style="--acc:#a4533a"><img class="paper" src="shared/paper.jpg">
<div class="hd"><div class="kick2">Vocabulario visual · Español — 24 temas · 480 palabras</div><h2>Índice</h2><div class="sub2">Contents · <span class="ko">목차 — 단어는 장소에서, 어순은 한 걸음씩</span></div>
<div class="legend"><span class="ko">각 장: 사진 오프너 · 단어 20개 · <b>어순 포인트</b>(앞 장에 쌓아 올리는 순서) · 도시 · 디자인 스킨</span></div></div>'''
    y=52;cur=-1
    for (part,n,es,ko,city,skin,op,sig,acc) in PLAN:
        if part!=cur:
            cur=part;pt=PARTS[part].split(" · ");y+=1.2
            h+=f'<div class="part" style="top:{y:.1f}mm"><span class="pn">{ROMAN[part]}</span><span class="pt">{pt[0][3:]}</span><span class="pk">{pt[1]}</span></div>';y+=5.4
        g,ex,exk=GR[n];here=n in (1,2,11)
        chip='<span class="here-chip">en este PDF</span>' if here else ''
        h+=f'''<div class="tr6{' here' if here else ''}" style="top:{y:.1f}mm"><div class="n" style="color:{acc}">{n:02d}</div><div><div class="es">{es}{chip}</div><div class="ko2">{ko} · 20 palabras</div></div>
<div><div class="gr">{g}</div><div class="ex">{ex}</div></div><div><div class="ci">{city}</div><div class="sk" style="color:{acc}">{SKINS[skin][0]}</div></div></div>'''
        y+=7.8
    h+=f'<div class="folio"><span>Índice · <span class="sk">Plan de 24 temas</span></span><span>ch01 · ch02 · ch11 en este PDF</span><span>Vocabulario visual · 1</span></div></section>'
    return h,y
# ---------- Créditos ----------
def creditos():
    C=json.load(open('/workspace/trilingual/es/v6/_build/credits_v6.json'))
    body='';cur=None
    for c in C:
        if c['sec']!=cur: cur=c['sec'];body+=f'<h4>{cur}</h4>'
        body+=f'<p><b>{c["what"]}</b> — {c["title"]}. {c["author"]} · {c["lic"]} · {__import__('urllib.parse').parse.unquote(c["url"])}{(" · "+c["mod"]) if c.get("mod") else ""}</p>'
    pages=[]
    head='''<section class="page wp cr s-museo" style="--acc:#a4533a"><img class="paper" src="shared/paper.jpg">
<div class="hd"><div class="kick2">Vocabulario visual · Español</div><h2>Créditos</h2><div class="sub2">Photo credits · <span class="ko">사진 출처와 라이선스</span></div>
<div class="legend"><span class="ko">모든 사진은 Wikimedia Commons의 실제 사진이에요(생성 이미지 없음). CC BY / CC BY-SA는 저작자 표시, BY-SA는 변경본도 같은 조건. 로고·광고·브랜드 글자는 리터칭으로 지웠어요.</span></div></div>'''
    return head,body

c0,y=indice();c1,h1=ch01();c2,h2=ch02();c3,h3=ch11()
head,body=creditos()
cr=head+f'<div class="cols" id="cr1">{body}</div><div class="folio"><span>Créditos</span><span>Wikimedia Commons</span><span>Vocabulario visual · 10</span></div></section>'
cr+=head.replace('<h2>Créditos</h2>','<h2>Créditos <span style="font-size:20pt">(cont.)</span></h2>')+'<div class="cols" id="cr2"></div><div class="folio"><span>Créditos</span><span>Wikimedia Commons</span><span>Vocabulario visual · 11</span></div></section>'
# overflow of cr1 is moved into cr2 at render time by flow.js (DOM split, before PDF)
FLOW="""<script>window.flowCredits=()=>{const a=document.getElementById('cr1'),b=document.getElementById('cr2');
const fits=()=>a.scrollWidth<=a.clientWidth+2;while(!fits()&&a.lastElementChild){b.prepend(a.lastElementChild)}
const h=a.lastElementChild;if(h&&h.tagName=='H4'){b.prepend(h)}return [a.children.length,b.children.length,b.scrollWidth<=b.clientWidth+2]}</script>"""
import re as _re
def _fb(css):
    out=[]
    for blk in _re.split(r'(@font-face\{[^}]*\})',css):
        if not blk.startswith('@font-face'):
            blk=blk.replace("'Special Elite'","'Special Elite','Gowun'").replace("'Jost';","'Jost','Gowun';").replace("'Jost'}","'Jost','Gowun'}")
        out.append(blk)
    return ''.join(out)
CSSX=_fb(CSS6)
open(f'{R}/index.html','w').write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSSX}</style>{FLOW}</head><body>{c0}{h1}{h2}{h3}{cr}</body></html>')
print('built, toc end y',round(y,1))

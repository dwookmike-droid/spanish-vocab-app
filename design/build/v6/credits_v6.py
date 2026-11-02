import json,re,sys;sys.path.insert(0,'/workspace/trilingual/es/v6/_build')
from data_v6 import CH02,CH11
P=json.load(open('photos.json'));N=json.load(open('photos_v6new.json'))
def t(x): return x['title'].replace('File:','')
out=[]
def add(sec,what,m,mod):
    out.append(dict(sec=sec,what=what,title=t(m),author=re.sub(r'\s+',' ',m['artist']).strip(),lic=m['lic'],licurl=m.get('licurl',''),url=m['page'],mod=mod))
# ch01
S='01 · El baño (Granada)'
add(S,'p.2 opener',N['ch01_OP'],'recortado, enfoque suave, degradado y texto encima')
ab=open('/workspace/trilingual/es/v6/ch01/CREDITS.md').read()
for f,what in (('print_bench.jpg','p.3 foto pegada'),('pol_stars.jpg','p.3 polaroid')):
    line=[l for l in ab.split('\n') if f'img/{f}' in l][0]
    seg=line.split('). ')[1] if False else line
    m=re.search(r'File:(.+?) — (.+?) — (.+?) \((.+?)\) — (\S+)\.',line)
    out.append(dict(sec=S,what=what,title=m.group(1),author=m.group(2),lic=m.group(3),licurl=m.group(4),url=m.group(5),mod='recortado'))
C=json.load(open('/workspace/trilingual/es/v6/ch01/img/credits.json'))
for c in C:
    if c['key'].startswith('__'): continue
    mod='recorte de fondo (rembg), sombra, ajuste de tono'+('; marca y texto eliminados' if c['key'] in('toothpaste','toilet') else '')
    out.append(dict(sec=S,what=f"p.3–5 {c['object']}",title=c['source'].replace('File:',''),author=c['author'],lic=c['license'],licurl=c['license_url'],url=c['source_url'],mod=mod))
S='02 · La cocina (València)'
add(S,'p.6 opener',N['ch02_OP'],'recortado, degradado y texto encima')
add(S,'p.7 polaroid',P['ch02_POL1'],'recortado')
for x in CH02:
    k=x[0]
    if k=='fridge': add(S,'p.7 la nevera',P['ch02_fridge'],'logotipo eliminado, recorte apaisado')
    else: add(S,f'p.7 {x[1]}',P[f'ch02_{k}'],{'knife':'grabado y logotipo eliminados, recortado','microwave':'logotipo, modelo y etiqueta eliminados, recortado'}.get(k,'recortado'))
S='11 · El transporte (Madrid)'
add(S,'p.8 opener',P['ch11_OP'],'recortado, degradado y texto encima')
add(S,'p.9 polaroid',P['ch11_POL1'],'recortado')
MOD={'bus':'recorte de fondo; logotipos, anuncios, matrícula y rótulo eliminados','train':'logotipos del morro eliminados, recortado','stop':'cartel publicitario tapado (panel liso), recortado',
     'helmet':'logotipo eliminado, recorte de fondo','plane':'recorte de fondo','ticket':'recorte de fondo, girado','lights':'recorte de fondo, solo el semáforo peatonal'}
for x in CH11:
    k=x[0];m=N.get(f'ch11_{k}',P[f'ch11_{k}'])
    cut=k in {'bus','taxi','ticket','suitcase','plane','bike','car','moto','lights','backpack','helmet'}
    add(S,f'p.9 {x[1]}',m,MOD.get(k,'recorte de fondo (rembg), sombra, ajuste de tono' if cut else 'recortado'))
json.dump(out,open('credits_v6.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(out),Counter(o['lic'] for o in out))

import asyncio,subprocess,os,sys
from playwright.async_api import async_playwright
R='/workspace/trilingual/es/v6';PDF=f'{R}/vocabulario_visual_v6_indice_ch01_ch02_ch11_creditos.pdf'
CHECK="""()=>{let o=[];document.querySelectorAll('.page').forEach((p,pi)=>{const pr=p.getBoundingClientRect();
 p.querySelectorAll('.lab').forEach((e,i)=>{const r=e.getBoundingClientRect(),par=e.parentElement.getBoundingClientRect();if(r.right>par.right+1)o.push(`p${pi+1} lab${i} wider ${(r.right-par.right).toFixed(1)}`)});
 p.querySelectorAll('.card,.sec,.box,.wall,.dc,.tr6,.keyl,.ans,.bil,.lead').forEach((e,i)=>{const r=e.getBoundingClientRect();if(r.bottom>pr.bottom-26)o.push(`p${pi+1} ${e.className} ${i} bottom ${((r.bottom-pr.top)/3.7795).toFixed(1)}mm`);if(r.right>pr.right-8)o.push(`p${pi+1} ${e.className} right ${((r.right-pr.left)/3.7795).toFixed(1)}mm`)});
 p.querySelectorAll('.sr,.row,.blk').forEach((e,i)=>{if(e.scrollWidth>e.clientWidth+2)o.push(`p${pi+1} ${e.className} ${i} hscroll`)});
 const cs=[...p.querySelectorAll('.card,.sec,.box,.dc')].map(e=>e.getBoundingClientRect());
 for(let a=0;a<cs.length;a++)for(let b=a+1;b<cs.length;b++){const A=cs[a],B=cs[b];const ox=Math.min(A.right,B.right)-Math.max(A.left,B.left),oy=Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top);if(ox>4&&oy>4)o.push(`p${pi+1} overlap ${a}-${b} ${(ox/3.78).toFixed(1)}x${(oy/3.78).toFixed(1)}mm`)}});
 let mn=99,who='';document.querySelectorAll('body *').forEach(e=>{if(!e.childNodes.length||e.closest('svg'))return;const t=[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim());if(!t)return;const s=parseFloat(getComputedStyle(e).fontSize)*0.75;if(s<mn){mn=s;who=e.className+':'+e.textContent.slice(0,20)}});
 o.push('min html font pt '+mn.toFixed(2)+' '+who);let sm=99,sw='';document.querySelectorAll('svg text,svg textPath').forEach(t=>{const el=t.tagName=='textPath'?t.parentElement:t;const fs=parseFloat(el.getAttribute('font-size')||getComputedStyle(el).fontSize);const m=el.getScreenCTM();const sc=Math.hypot(m.a,m.b);const pt=fs*sc*0.75;if(pt<sm){sm=pt;sw=t.textContent.slice(0,24)}});o.push('min svg font pt '+sm.toFixed(2)+' '+sw);
 o.push('fonts:'+[...document.fonts].filter(f=>f.status!='loaded').map(f=>f.family).join(','));return o}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page()
        await pg.goto(f'file://{R}/index.html');await pg.evaluate('document.fonts.ready');await pg.wait_for_timeout(800)
        print('credits flow',await pg.evaluate('flowCredits()'))
        print('\n'.join(await pg.evaluate(CHECK)))
        await pg.pdf(path=PDF,format='A4',print_background=True,prefer_css_page_size=True);await b.close()
asyncio.run(main())
for f in os.listdir(f'{R}/_shots'):
    if f.startswith('tmp-'): os.remove(f'{R}/_shots/{f}')
subprocess.run(['pdftoppm','-r','110','-png',PDF,f'{R}/_shots/tmp'],check=True)
names=['p01_indice','p02_ch01_opener','p03_ch01_palabras','p04_ch01_orden1','p05_ch01_orden2','p06_ch02_opener','p07_ch02_palabras','p08_ch11_opener','p09_ch11_palabras','p10_creditos','p11_creditos2']
tm=sorted(f for f in os.listdir(f'{R}/_shots') if f.startswith('tmp-'))
print('pages',len(tm))
for f,n in zip(tm,names): os.replace(f'{R}/_shots/{f}',f'{R}/_shots/{n}.png')

cmd=f"pdffonts {PDF}; echo TYPE3: $(pdffonts {PDF} | grep -ci 'type 3'); pdfimages -list {PDF} | awk 'NR>2 && $3!=\"smask\"{{print $1, $13, $4, $5}}' | sort -k2 -n | head -5"
print(subprocess.run(cmd,shell=True,capture_output=True,text=True).stdout)
"""Optimised build: print (>=300ppi, ~320 target) + screen (~150ppi). Run after build_v6.py (needs index.html)."""
import asyncio,subprocess,os,sys,json
sys.path.insert(0,'/workspace/trilingual/es/v6/_build')
import optimize as OP
from playwright.async_api import async_playwright
R='/workspace/trilingual/es/v6';BASE='vocabulario_visual_v6_indice_ch01_ch02_ch11_creditos'
PROFILES={'print':dict(ppi=320,floor=300,q=86,pq=86),'screen':dict(ppi=150,floor=140,q=78,pq=78)}
async def render(page,html,pdf):
    await page.goto(f'file://{R}/{html}');await page.evaluate('document.fonts.ready');await page.wait_for_timeout(600)
    fl=await page.evaluate('window.flowCredits?flowCredits():null')
    await page.pdf(path=pdf,format='A4',print_background=True,prefer_css_page_size=True);return fl
async def main(which):
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page()
        await pg.goto(f'file://{R}/index.html');await pg.evaluate('document.fonts.ready');await pg.wait_for_timeout(600)
        await pg.evaluate('window.flowCredits&&flowCredits()')
        meas=await pg.evaluate(OP.MEASURE_JS)
        html=open(f'{R}/index.html').read()
        for name in which:
            pr=PROFILES[name];out=f'{R}/_opt/{name}'
            mp=OP.make_assets(R,meas,out,ppi=pr['ppi'],floor=pr['floor'],q=pr['q'],log=f'{R}/_opt/{name}_assets.json')
            open(f'{R}/index_{name}.html','w').write(OP.rewrite_html(html,mp))
            raw=f'{R}/_opt/{BASE}_{name}_raw.pdf'
            fl=await render(pg,f'index_{name}.html',raw)
            final=f'{R}/{BASE}_{name}.pdf'
            nc,nd=OP.postprocess(raw,final,q=pr['pq'])
            print(name,'credits flow',fl,'flate->jpeg',nc,'dedup',nd,'size MB',round(os.path.getsize(final)/1e6,2))
        await b.close()
which=sys.argv[1:] or ['print','screen']
asyncio.run(main(which))

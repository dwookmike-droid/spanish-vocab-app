"""One-command chapter build (standing rule: every build is size-optimised).
1) build_v6.py      -> index.html (layout source)
2) render_v6.py     -> master PDF (unoptimised, kept as reference) + page shots
3) render_opt_v6.py -> *_print.pdf (photos 300-320ppi, JPEG q86 4:2:0, alpha as JPEG+SMask, dedupe, no XMP, linearized)
                       *_screen.pdf (~150ppi, q78)
4) web_v6.py        -> web/ (WebP 1x/2x srcset + lazy, speech MP3 mono 24kHz 32kbps)
Usage: python3 _build/build_all.py [--skip-master]
"""
import subprocess,sys,os
B=os.path.dirname(os.path.abspath(__file__));R=os.path.dirname(B)
steps=['build_v6.py']+([] if '--skip-master' in sys.argv else ['render_v6.py'])+['render_opt_v6.py','web_v6.py']
for s in steps:
    print('>>',s,flush=True);subprocess.run([sys.executable,f'{B}/{s}'],cwd=R,check=True)
for f in sorted(os.listdir(R)):
    if f.endswith('.pdf'): print(f'{os.path.getsize(f"{R}/{f}")/1e6:6.2f} MB  {f}')
w=sum(os.path.getsize(os.path.join(d,f)) for d,_,fs in os.walk(f'{R}/web') for f in fs)
print(f'{w/1e6:6.2f} MB  web/')

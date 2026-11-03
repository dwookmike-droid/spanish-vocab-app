"""Gentle Commons candidate fetcher for many chapters (shared IPs get rate-limited hard).

Usage: python3 claude_design/tools/commons_fetch_slow.py 08 10 12 ...   (N candidates per word = 4)
For each chapter reads claude_design/chNN/queries.json and writes cand/<key>_<i>.jpg + cand/meta.json,
saving after every word so it can be stopped and resumed. One request every PACE seconds; on HTTP 429 it waits
(Retry-After or 60 s, growing) and tries again. Thumbnails use a standard Wikimedia width (330 px).
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "VocabularioVisual/1.0 (https://github.com/dwookmike-droid/spanish-vocab-app; educational app)"}
OK = re.compile(r"^(cc0|cc[- ]by(-sa)?[- ]?[1-4]\.0|public domain|pd)", re.I)
PACE, N, THUMB = 6, 4, 330
_last = [0.0]


def get(u):
    wait = 60
    while True:
        dt = time.time() - _last[0]
        if dt < PACE:
            time.sleep(PACE - dt)
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500:
                raise
            ra = e.headers.get("Retry-After")
            pause = max(int(ra) if ra and ra.isdigit() else 0, wait)
            print(f"   {e.code}, waiting {pause}s", flush=True)
            time.sleep(pause)
            wait = min(wait * 2, 300)
        except Exception as e:
            print("   network:", e, flush=True)
            time.sleep(30)


def chapter(nn):
    d = ROOT / f"claude_design/ch{nn}"
    out = d / "cand"
    out.mkdir(parents=True, exist_ok=True)
    Q = json.loads((d / "queries.json").read_text(encoding="utf-8"))
    mp = out / "meta.json"
    meta = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {}
    for key, q in Q.items():
        if meta.get(key):
            continue
        p = {"action": "query", "format": "json", "generator": "search", "gsrsearch": q + " filetype:bitmap", "gsrnamespace": 6,
             "gsrlimit": 25, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": THUMB}
        d_ = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
        pages = sorted(d_.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 99))
        picked = []
        for pg in pages:
            ii = (pg.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {})
            lic = em.get("LicenseShortName", {}).get("value", "")
            if not OK.match(lic) or min(ii.get("width", 0), ii.get("height", 0)) < 700 or "thumburl" not in ii:
                continue
            art = re.sub("<[^>]+>", "", em.get("Artist", {}).get("value", "")).strip()
            picked.append(dict(title=pg["title"], lic=lic, artist=art, w=ii["width"], h=ii["height"], url=ii["url"],
                               thumb=ii["thumburl"], page=ii["descriptionurl"]))
            if len(picked) >= N:
                break
        for i, c in enumerate(picked):
            fn = out / f"{key}_{i}.jpg"
            if not fn.exists() or fn.stat().st_size == 0:
                fn.write_bytes(get(c["thumb"]))
            c["file"] = str(fn)
        meta[key] = picked
        mp.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"ch{nn} {key}: {len(picked)}", flush=True)


if __name__ == "__main__":
    for nn in sys.argv[1:]:
        chapter(nn)
    print("done")

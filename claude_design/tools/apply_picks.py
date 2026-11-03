"""Save the chosen Commons photo for each word: claude_design/chNN/img/<key>.jpg (500 px, a standard Wikimedia thumbnail width) + credits.json.

Usage: python3 claude_design/tools/apply_picks.py claude_design/chNN
Reads cand/meta.json (from commons_cand.py) and picks.json ({"key": index or null}).
credits.json uses the same fields as ch09 (title, lic, artist, w, h, url, thumb, page), which build_data.py reads.
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

UA = {"User-Agent": "VocabularioVisual/1.0 (https://github.com/dwookmike-droid/spanish-vocab-app; educational app)"}


def get(u):
    u = u.replace("://thumb.wikimedia.org/", "://upload.wikimedia.org/")  # thumb host is not on the network allow-list
    err = None
    for i in range(8):
        time.sleep(6)  # shared IPs get rate-limited: stay slow
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as e:  # 429 / network: back off and retry
            err = e
            time.sleep(min(60 * (i + 1), 300))
    raise err


def main(d):
    d = Path(d)
    meta = json.loads((d / "cand/meta.json").read_text(encoding="utf-8"))
    picks = json.loads((d / "picks.json").read_text(encoding="utf-8"))
    (d / "img").mkdir(exist_ok=True)
    credits = {}
    for key, idx in picks.items():
        if idx is None or idx >= len(meta.get(key, [])):
            continue
        c = meta[key][idx]
        dst = d / "img" / f"{key}.jpg"
        if not dst.exists():
            url = re.sub(r"/\d+px-", "/500px-", c["thumb"])
            dst.write_bytes(get(url))
        credits[key] = {k: c[k] for k in ("title", "lic", "artist", "w", "h", "url", "thumb", "page")}
    (d / "credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")
    print(d.name, len(credits), "photos")


if __name__ == "__main__":
    main(sys.argv[1])

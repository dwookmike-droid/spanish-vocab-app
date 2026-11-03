"""Openverse candidate fetcher (CC photos from Flickr, Wikimedia and others through one host: api.openverse.org).

Usage: python3 claude_design/tools/openverse_fetch.py 08 10 12 ...
For each chapter reads claude_design/chNN/queries.json and writes cand/<key>_<i>.jpg (Openverse 600 px thumbnail)
+ cand/meta.json in the same format as commons_fetch_slow.py (plus "src": "openverse"), saving after every word.
Words that already have candidates are skipped, so it resumes. Anonymous limits: search 20/min and 200/day,
thumbnails 1000/day; when the daily search budget is used up it stops cleanly (run again tomorrow).
"""
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "VocabularioVisual/1.0 (https://github.com/dwookmike-droid/spanish-vocab-app; educational app)"}
API = "https://api.openverse.org/v1/images/"
LIC = {"cc0": "CC0", "pdm": "Public Domain", "by": "CC BY", "by-sa": "CC BY-SA"}
PACE = 9  # 9 s between searches: three processes stay under the 20/min burst limit
N = int(os.environ.get("OV_N", 3))  # candidates per word
_last = [0.0]
_lock = threading.Lock()


class OutOfBudget(Exception):
    pass


def get(u, pace=True):
    for attempt in range(6):
        if pace:  # searches are paced; thumbnails (own 1000/day budget) are fetched in parallel
            with _lock:
                dt = time.time() - _last[0]
                if dt < PACE:
                    time.sleep(PACE - dt)
                _last[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                return r.read(), r.headers
        except urllib.error.HTTPError as e:
            if e.code == 429:
                if any(e.headers.get(h) == "0" for h in ("x-ratelimit-available-anon_sustained",
                                                         "x-ratelimit-available-anon_thumbnail")):
                    raise OutOfBudget(u)
                print("   429, waiting 60s", flush=True)
                time.sleep(60)
            elif e.code >= 500:
                time.sleep(20)
            else:
                raise
        except Exception as e:
            print("   network:", e, flush=True)
            time.sleep(20)
    raise RuntimeError("giving up on " + u)


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
        results, hdr = [], {}
        # long queries often return nothing: fall back to the first two words, then the first word
        words = q.split()
        for qq in dict.fromkeys([q, " ".join(words[:2]), words[0]]):
            p = {"q": qq, "license": ",".join(LIC), "page_size": 12, "mature": "false"}
            body, hdr = get(API + "?" + urllib.parse.urlencode(p))
            results = json.loads(body).get("results", [])
            if results:
                break
        cands = []
        for r in results:
            if (r.get("width") or 0) and min(r.get("width") or 0, r.get("height") or 0) < 400:
                continue
            lic = LIC[r["license"]] + (f" {r['license_version']}" if r["license"] not in ("cc0", "pdm") and r.get("license_version") else "")
            cands.append(dict(title=r.get("title") or "", lic=lic, artist=r.get("creator") or "", w=r.get("width"), h=r.get("height"),
                              url=r.get("url"), thumb=r["thumbnail"], page=r.get("foreign_landing_url") or "",
                              src="openverse", provider=r.get("source") or ""))

        def fetch(ic):
            i, c = ic
            fn = out / f"{key}_{i}.jpg"
            try:
                fn.write_bytes(get(c["thumb"], pace=False)[0])
                c["file"] = str(fn)
            except OutOfBudget:
                raise
            except Exception as e:  # 424: the original host is gone; try the next result instead
                print("   thumb failed:", key, i, e, flush=True)

        picked, pos = [], 0
        with ThreadPoolExecutor(N) as ex:
            while len(picked) < N and pos < len(cands):
                batch = list(enumerate(cands[pos:pos + N - len(picked)], start=pos))
                pos += len(batch)
                list(ex.map(fetch, batch))
                picked += [c for _, c in batch if c.get("file")]
        meta[key] = picked
        mp.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"ch{nn} {key}: {len(picked)}  (search left today: {hdr.get('x-ratelimit-available-anon_sustained')})", flush=True)


if __name__ == "__main__":
    try:
        for nn in sys.argv[1:]:
            chapter(nn)
        print("done")
    except OutOfBudget as e:
        print("out of daily Openverse budget; run again tomorrow:", e)

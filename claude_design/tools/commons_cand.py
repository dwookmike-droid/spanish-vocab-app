"""Commons 후보 검색: 키별로 검색어를 돌려 라이선스·해상도가 맞는 파일의 썸네일을 받는다."""
import json, sys, os, re, time, urllib.parse, urllib.request
OUT = sys.argv[1]; Q = json.load(open(sys.argv[2], encoding='utf-8')); N = int(sys.argv[3]) if len(sys.argv) > 3 else 8
UA = {'User-Agent': 'vocab-book-photo-search/1.0 (personal study material)'}
OK = re.compile(r'^(cc0|cc[- ]by(-sa)?[- ]?[1-4]\.0|public domain|pd)', re.I)
def get(u):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r: return r.read()
        except Exception as e:
            time.sleep(5 * (i + 1)); err = e
    raise err
meta = json.load(open(f'{OUT}/meta.json', encoding='utf-8')) if os.path.exists(f'{OUT}/meta.json') else {}
for key, q in Q.items():
    if meta.get(key): continue
    p = {'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': q + ' filetype:bitmap', 'gsrnamespace': 6, 'gsrlimit': 30,
         'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata', 'iiurlwidth': 360}
    for t in range(5):
        d = json.loads(get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(p)))
        if 'query' in d or 'error' not in d: break
        time.sleep(15 * (t + 1))
    pages = sorted(d.get('query', {}).get('pages', {}).values(), key=lambda x: x.get('index', 99))
    picked = []
    for pg in pages:
        ii = pg['imageinfo'][0]; em = ii.get('extmetadata', {})
        lic = em.get('LicenseShortName', {}).get('value', '')
        if not OK.match(lic) or min(ii['width'], ii['height']) < 900: continue
        art = re.sub('<[^>]+>', '', em.get('Artist', {}).get('value', '')).strip()
        picked.append(dict(title=pg['title'], lic=lic, artist=art, w=ii['width'], h=ii['height'], url=ii['url'], thumb=ii['thumburl'], page=ii['descriptionurl']))
        if len(picked) >= N: break
    for i, c in enumerate(picked):
        fn = f'{OUT}/{key}_{i}.jpg'
        if not os.path.exists(fn): open(fn, 'wb').write(get(c['thumb'])); time.sleep(.5)
        c['file'] = fn
    meta[key] = picked; print(key, len(picked)); time.sleep(1)
json.dump(meta, open(f'{OUT}/meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

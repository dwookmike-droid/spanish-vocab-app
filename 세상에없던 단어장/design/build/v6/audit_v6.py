import sys,re,unicodedata;sys.path.insert(0,'.')
from base_v6 import V3
from data_v6 import CH02,CH11
items=[('01',i['es'],i['p']) for i in V3]+[('02',x[1],x[3]) for x in CH02]+[('11',x[1],x[3]) for x in CH11]
def jamo(s):
    out=[]
    for ch in s:
        o=ord(ch)-0xAC00
        if 0<=o<11172: out.append((o//588,(o%588)//28,o%28))
    return out
CHO='ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
JUNG='ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
rows=[];bad=0
for ch,es,p in items:
    w=es.lower();plain=re.sub('<[^>]+>','',p);J=jamo(plain);cho=[CHO[a] for a,b,c in J]
    issues=[]
    if 'ㅌ' in cho or 'ㅋ' in cho: issues.append('ㅌ/ㅋ (p·t·k는 ㄸ·ㄲ)')
    if 'ㅍ' in cho and 'f' not in w: issues.append('ㅍ인데 f 없음')
    if 'f' in w and 'ㅍ' not in cho: issues.append('f인데 ㅍ 없음')
    if re.search(r'p',w) and 'ㅃ' not in cho: issues.append('p인데 ㅃ 없음')
    if re.search(r'z|c[ei]',w) and not ({'ㅅ','ㅆ'}&set(cho)): issues.append('c/z인데 ㅅ 없음')
    if re.search(r'll|y[aeiou]',w):
        ok=any(CHO[a]=='ㅇ' and JUNG[b] in 'ㅑㅕㅛㅠㅖㅒㅣ' for a,b,c in J)
        if not ok: issues.append('ll/y인데 야·요 계열 없음')
    nb=len(re.findall('<b>',p))
    if nb==0: issues.append('굵은 강세 없음')
    rows.append((ch,es,plain,nb,issues));bad+=bool(issues)
print(f'checked {len(rows)} items, flagged {bad}')
for r in rows:
    if r[4]: print(r)
import json;json.dump(rows,open('audit_pron.json','w'),ensure_ascii=False)

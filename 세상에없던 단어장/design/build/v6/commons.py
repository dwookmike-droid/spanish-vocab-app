import json,urllib.request,urllib.parse,sys,re,os
UA={'User-Agent':'StudyBookBot/1.0 (personal study; contact via owner)'}
def api(params):
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({**params,'format':'json'})
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40))
OK=re.compile(r'^(CC0|Public domain|PD|CC BY(-SA)? ?[1-4]\.0|CC BY(-SA)? [1-4]\.0)',re.I)
def search(q,n=20):
    r=api({'action':'query','generator':'search','gsrsearch':q+' filetype:bitmap','gsrnamespace':6,'gsrlimit':n,'prop':'imageinfo','iiprop':'url|size|mime|extmetadata','iiurlwidth':500})
    out=[]
    for p in sorted(r.get('query',{}).get('pages',{}).values(),key=lambda p:p.get('index',0)):
        ii=p['imageinfo'][0];m=ii.get('extmetadata',{})
        lic=m.get('LicenseShortName',{}).get('value','')
        art=re.sub('<[^>]+>','',m.get('Artist',{}).get('value','')).strip()
        if not OK.match(lic) or ii['mime'] not in('image/jpeg','image/png'): continue
        out.append({'title':p['title'],'w':ii['width'],'h':ii['height'],'lic':lic,'licurl':m.get('LicenseUrl',{}).get('value',''),'artist':art[:80],'thumb':ii['thumburl'],'url':ii['url'],'page':ii['descriptionurl']})
    return out
if __name__=='__main__':
    Q=json.load(open(sys.argv[1]));res={}
    for k,qs in Q.items():
        res[k]=[]
        for q in qs:
            try: res[k]+=search(q)
            except Exception as e: print(k,q,'ERR',e)
        seen=set();res[k]=[c for c in res[k] if not(c['title'] in seen or seen.add(c['title']))][:24]
        print(k,len(res[k]))
    json.dump(res,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)

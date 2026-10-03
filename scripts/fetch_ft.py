import json, subprocess, os, sys
from concurrent.futures import ThreadPoolExecutor
D=os.environ.get('FTDIR','../data/fulltext'); os.makedirs(D,exist_ok=True)
src=json.load(open('../data/fulltext_sources.json'))
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
def urls(v):
    u=[]
    if v['oa'] and v['oa'].get('url'): u.append(v['oa']['url'])
    if v['arxiv']: u.append(f"https://arxiv.org/pdf/{v['arxiv']}")
    d=v['doi']
    if d.startswith('10.1145/'): u.append(f"https://dl.acm.org/doi/pdf/{d}")
    if d.startswith('10.3389/'): u.append(f"https://www.frontiersin.org/articles/{d}/pdf")
    if d.startswith('10.2196/'): u.append(f"https://doi.org/{d}")
    if d.startswith('10.3390/'): u.append(f"https://doi.org/{d}")
    if d.startswith('10.1007/'): u.append(f"https://link.springer.com/content/pdf/{d}.pdf")
    if d: u.append(f"https://doi.org/{d}")
    return u
def get(k):
    v=src[k]; out=f"{D}/{k}.pdf"
    if not v: return k,'no-doi'
    if os.path.exists(out) and os.path.getsize(out)>20000: return k,'cached'
    for u in urls(v):
        subprocess.run(['curl','-sL','-m','60','-A',UA,'-o',out,u])
        if os.path.exists(out) and open(out,'rb').read(5)==b'%PDF-' and os.path.getsize(out)>20000: return k,'ok '+u
    if os.path.exists(out): os.remove(out)
    return k,'FAIL'
with ThreadPoolExecutor(8) as ex: res=list(ex.map(get,src))
json.dump(dict(res),open('../data/fulltext_status.json','w'),indent=1)
print(sum(1 for _,s in res if s.startswith(('ok','cached'))),'/',len(res))

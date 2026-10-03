"""Cuarta vía: copias archivadas (Internet Archive) de los PDF de acceso abierto."""
import json, os, subprocess, urllib.parse, urllib.request
D=os.environ['FTDIR']
src=json.load(open('../data/fulltext_sources.json')); st=json.load(open('../data/fulltext_status.json'))
for k,v in src.items():
    if not v or not st[k].startswith('FAIL') or v['doi'].startswith('10.1109/'): continue
    cands=[(v['oa'] or {}).get('url')] if (v['oa'] or {}).get('url') else []
    if v['doi'].startswith('10.1145/'): cands.append(f"https://dl.acm.org/doi/pdf/{v['doi']}")
    for u in cands:
        try:
            a=json.load(urllib.request.urlopen("https://archive.org/wayback/available?url="+urllib.parse.quote(u,safe=''),timeout=40))
            snap=a.get('archived_snapshots',{}).get('closest')
            if not snap: continue
            raw=snap['url'].replace('/http','id_/http',1)
            subprocess.run(['curl','-sL','-m','90','-o',f"{D}/{k}.pdf",raw])
            if open(f"{D}/{k}.pdf",'rb').read(5)==b'%PDF-': st[k]='ok wayback '+raw; break
            os.remove(f"{D}/{k}.pdf")
        except Exception as e: pass
    print(k,st[k])
json.dump(st,open('../data/fulltext_status.json','w'),indent=1)
print(sum(1 for s in st.values() if s.startswith(('ok','cached'))),'/',len(st))

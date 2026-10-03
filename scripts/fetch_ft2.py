"""Segunda vía de recuperación: Europe PMC (XML de texto completo) y arXiv por título."""
import json, os, re, subprocess, urllib.parse, urllib.request, time, difflib
D=os.environ.get('FTDIR','../data/fulltext')
src=json.load(open('../data/fulltext_sources.json')); st=json.load(open('../data/fulltext_status.json'))
def j(u):
    return json.load(urllib.request.urlopen(u,timeout=60))
for k,v in src.items():
    if not st[k].startswith('FAIL') or not v: continue
    # Europe PMC
    try:
        r=j("https://www.ebi.ac.uk/europepmc/webservices/rest/search?"+urllib.parse.urlencode({'query':f'DOI:"{v["doi"]}"','format':'json','resultType':'lite'}))
        hits=[h for h in r['resultList']['result'] if h.get('pmcid')]
        if hits:
            x=urllib.request.urlopen(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{hits[0]['pmcid']}/fullTextXML",timeout=60).read()
            if len(x)>20000:
                open(f"{D}/{k}.xml",'wb').write(x); st[k]='ok europepmc '+hits[0]['pmcid']; print(k,st[k]); continue
    except Exception as e: print(k,'epmc err',e)
    # arXiv por título
    try:
        t=re.sub(r'[^A-Za-z0-9 ]',' ',v['title']); q='ti:"'+' '.join(t.split()[:12])+'"'
        x=urllib.request.urlopen("https://export.arxiv.org/api/query?"+urllib.parse.urlencode({'search_query':q,'max_results':3}),timeout=60).read().decode()
        for ent in re.findall(r'<entry>(.*?)</entry>',x,re.S):
            et=re.sub(r'\s+',' ',re.search(r'<title>(.*?)</title>',ent,re.S).group(1))
            if difflib.SequenceMatcher(None,et.lower(),v['title'].lower()).ratio()>0.85:
                aid=re.search(r'<id>http://arxiv.org/abs/(.*?)</id>',ent).group(1)
                subprocess.run(['curl','-sL','-m','60','-o',f"{D}/{k}.pdf",f"https://arxiv.org/pdf/{aid}"])
                if open(f"{D}/{k}.pdf",'rb').read(5)==b'%PDF-': st[k]='ok arxiv-title '+aid; print(k,st[k]); break
        time.sleep(3)
    except Exception as e: print(k,'arxiv err',e)
json.dump(st,open('../data/fulltext_status.json','w'),indent=1)
print(sum(1 for s in st.values() if s.startswith(('ok','cached'))),'/',len(st))

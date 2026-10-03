import json, re, html
P = r'(social robot|social robotics|socially assistive robot|companion robot|human[- ]robot interaction)'
I = r'(large language model|generative ai|generative artificial intelligence|vision[- ]language model|foundation model|\bgpt|chatgpt|multimodal llm|\bllms?\b)'
def clean(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s or ''))).strip()
def norm(t): return re.sub(r'[^a-z0-9]','',t.lower())
recs=[]
s2=json.load(open('../data/s2_all.json'))
for p in s2['data']:
    t=p.get('publicationTypes') or []
    typ='Journal article' if 'JournalArticle' in t or 'Review' in t else ('Conference paper' if 'Conference' in t else (', '.join(t) or 'Unknown'))
    if 'Review' in t: typ='Review'
    recs.append(dict(db='Semantic Scholar',title=clean(p['title']),authors='; '.join(a['name'] for a in (p.get('authors') or [])),
      year=p.get('year'),source=(p.get('journal') or {}).get('name') or p.get('venue') or '',type=typ,
      doi=((p.get('externalIds') or {}).get('DOI') or '').lower(),arxiv=bool((p.get('externalIds') or {}).get('ArXiv')),abstract=clean(p.get('abstract'))))
cr=json.load(open('../data/cr_all.json')); kept=0
for it in cr['data']:
    title=clean(' '.join(it.get('title') or [])); ab=clean(it.get('abstract'))
    txt=(title+' '+ab).lower()
    if not (re.search(P,txt) and re.search(I,txt)): continue
    y=(it.get('issued',{}).get('date-parts') or [[None]])[0][0]
    if not y or y<2020 or y>2026: continue
    typ={'journal-article':'Journal article','proceedings-article':'Conference paper','posted-content':'Preprint','book-chapter':'Book chapter'}.get(it['type'],it['type'])
    recs.append(dict(db='Crossref',title=title,authors='; '.join((a.get('given','')+' '+a.get('family','')).strip() for a in it.get('author',[])),
      year=y,source=' '.join(it.get('container-title') or []),type=typ,doi=it['DOI'].lower(),arxiv=False,abstract=ab)); kept+=1
print('S2',len(s2['data']),'CR candidates',len(cr['data']),'CR matching equation',kept)
json.dump(recs,open('../data/recs.json','w'))

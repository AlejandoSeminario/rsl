import json, re
recs=json.load(open('../data/recs.json'))
def norm(t): return re.sub(r'[^a-z0-9]','',t.lower())
seen={}; 
for i,r in enumerate(recs):
    r['id']=f"R{i+1:04d}"; r['dup_of']=''
    keys=[k for k in (r['doi'], norm(r['title'])) if k]
    hit=next((seen[k] for k in keys if k in seen),None)
    if hit: r['dup_of']=hit
    else:
        for k in keys: seen[k]=r['id']
uniq=[r for r in recs if not r['dup_of']]
print('total',len(recs),'dups',len(recs)-len(uniq),'unique',len(uniq))
# Filters (CE automatic)
for r in uniq:
    v=''
    if r['type'] not in ('Journal article','Conference paper','Review'):
        v='CE1: tipo de documento no elegible (preprint, libro, capítulo, tesis u otro)'
    elif not r['source'] or re.search(r'arxiv|biorxiv|ssrn|research square|techrxiv',r['source'].lower()):
        v='CE1: preprint sin revisión por pares'
    elif len(r['abstract'])<100:
        v='CE5: registro sin resumen disponible para el cribado'
    r['filter']=v
f=[r for r in uniq if not r['filter']]
print('after filters',len(f))
from collections import Counter; print(Counter(r['filter'] for r in uniq))
SOC=r'(social robot|socially assistive|companion robot|social robotics|human[- ]robot interaction|\bhri\b|humanoid|pepper|nao|furhat|elderly|older adults|children|autism|conversational robot|receptionist|tutor)'
GEN=r'(large language model|\bllms?\b|gpt|chatgpt|generative|vision[- ]language|foundation model|multimodal language)'
OUT=r'(latency|response time|delay|gesture|nonverbal|non-verbal|gaze|facial expression|speech|voice|asr|turn-taking|ethic|trust|anthropomorph|manipulat|safety|deception|user study|participants|experiment|evaluat|theory of mind|emotion|empath)'
NONSOC=r'(manipulation task|grasp|pick-and-place|autonomous driving|surgical|industrial|warehouse|quadruped|drone|uav|navigation benchmark)'
for r in f:
    t=(r['title']+' '+r['abstract']).lower()
    r['c_soc']=bool(re.search(SOC,t)); r['c_gen']=bool(re.search(GEN,t))
    r['n_out']=len(set(re.findall(OUT,t))); r['nonsoc']=bool(re.search(NONSOC,t)) and not re.search(r'social|assistive|companion|elderly|older adults|children',t)
    r['multi']=bool(re.search(r'multimodal|multi-modal|vision|visual|image|video|gesture|speech|voice|gaze|facial',t))
    r['empir']=bool(re.search(r'participants|user study|experiment|we evaluat|evaluation|n ?= ?\d+|pilot|field study|trial',t))
json.dump(recs,open('../data/recs2.json','w'))
cand=[r for r in f if r['c_soc'] and r['c_gen'] and not r['nonsoc'] and r['multi'] and r['empir'] and r['n_out']>=3]
print('auto-candidates',len(cand))

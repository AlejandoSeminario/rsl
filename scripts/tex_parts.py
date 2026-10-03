import json, re
inc = json.load(open('../data/incluidos.json'))
exec(open('../data/extraccion.py').read())
YEAR_FIX = {'R0617': 2026}  # publicado en Frontiers el 15/04/2026
for r in inc: r['year'] = YEAR_FIX.get(r['id'], r['year'])
def esc(s):
    s = s.replace('\\', ' ')
    for a, b in [('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}'), ('~', r'\textasciitilde{}'), ('^', r'\^{}')]:
        s = s.replace(a, b)
    s = s.replace('≈', '$\\approx$').replace('→', '$\\rightarrow$').replace('+', '+\\allowbreak{}').replace('/', '/\\allowbreak{}')
    return s.replace('“', '``').replace('”', "''").replace('’', "'").replace('‐', '-').replace('–', '--').replace('—', '---')
def surname(n):
    p = n.split()
    if len(p) > 2 and p[-2] in ('Ben', 'de', 'van', 'Van', 'von'): return ' '.join(p[-2:])
    return p[-1] if p else n
SUF = {}
def cite(r):
    a = [x.strip() for x in r['authors'].split(';') if x.strip()]
    if not a: return esc(r['title'][:30]) + f", {r['year']}"
    if len(a) == 1: s = surname(a[0])
    elif len(a) == 2: s = f"{surname(a[0])} {'e' if surname(a[1])[:1] in 'IÍ' else 'y'} {surname(a[1])}"
    else: s = f"{surname(a[0])} et al."
    return f"{esc(s)}, {r['year']}{SUF.get(r['id'], '')}"
inc.sort(key=lambda r: (surname(r['authors'].split(';')[0]) if r['authors'] else r['title']).lower())
from collections import Counter
key = lambda r: (cite(r).rsplit(',', 1)[0], r['year'])
dupk = {k for k, v in Counter(map(key, inc)).items() if v > 1}
suf = {}
for k in dupk:
    for i, r in enumerate([r for r in inc if key(r) == k]): suf[r['id']] = 'abcdefgh'[i]
SUF.update(suf)
rows = []
for n, r in enumerate(inc, 1):
    x = X[r['id']]
    rows.append(f"{n} & {cite(r)} & {esc(x['plat'])} & {esc(x['n'])} & {esc(x['modelo'])} & {esc(x['res'])} & {esc(x['dim'])} \\\\")
open('../articulo/tabla_incluidos.tex', 'w').write('\n'.join(rows) + '\n')
def apa(r):
    a = [x.strip() for x in r['authors'].split(';') if x.strip()]
    def fmt(n):
        sn = surname(n); given = n[:len(n) - len(sn)].split()
        return (sn + ', ' + ' '.join(q[0] + '.' for q in given)) if given else n
    f = [fmt(n) for n in a]
    if len(f) > 20: au = ', '.join(f[:19]) + ', \\ldots{} ' + f[-1]
    elif len(f) > 1: au = ', '.join(f[:-1]) + ', y ' + f[-1]
    else: au = f[0] if f else ''
    doi = f" \\url{{https://doi.org/{r['doi']}}}" if r['doi'] else ''
    return f"\\bibitem{{{r['id']}}} {esc(au)} ({r['year']}{SUF.get(r['id'], '')}). {esc(r['title'])}. \\textit{{{esc(r['source'])}}}.{doi}"
open('../articulo/refs_incluidos.tex', 'w').write('\n\n'.join(apa(r) for r in inc) + '\n')

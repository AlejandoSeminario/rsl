import json, re
inc = json.load(open('../data/incluidos.json'))
def esc(s):
    s = s.replace('\\', ' ')
    for a, b in [('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}'), ('~', r'\textasciitilde{}'), ('^', r'\^{}')]:
        s = s.replace(a, b)
    return s.replace('“', '``').replace('”', "''").replace('’', "'").replace('‐', '-').replace('–', '--').replace('—', '---')
def surname(n): return n.split()[-1] if n.split() else n
def cite(r):
    a = [x.strip() for x in r['authors'].split(';') if x.strip()]
    if not a: return esc(r['title'][:30]) + f", {r['year']}"
    if len(a) == 1: s = surname(a[0])
    elif len(a) == 2: s = f"{surname(a[0])} y {surname(a[1])}"
    else: s = f"{surname(a[0])} et al."
    y = "2025b" if s == "Abbo et al." and r["year"] == 2025 else r["year"]
    return f"{esc(s)}, {y}"
inc.sort(key=lambda r: (surname(r['authors'].split(';')[0]) if r['authors'] else r['title']).lower())
rows = []
for n, r in enumerate(inc, 1):
    src = r['source'] if len(r['source']) < 55 else r['source'][:52] + '...'
    rows.append(f"{n} & {cite(r)} & {esc(r['title'])} & {esc(src)} \\\\")
open('../articulo/tabla_incluidos.tex', 'w').write('\n'.join(rows) + '\n')
def apa(r):
    a = [x.strip() for x in r['authors'].split(';') if x.strip()]
    f = [(n.split()[-1] + ', ' + ' '.join(q[0] + '.' for q in n.split()[:-1])) if len(n.split()) > 1 else n for n in a]
    if len(f) > 20: au = ', '.join(f[:19]) + ', \\ldots{} ' + f[-1]
    elif len(f) > 1: au = ', '.join(f[:-1]) + ', y ' + f[-1]
    else: au = f[0] if f else ''
    doi = f" \\url{{https://doi.org/{r['doi']}}}" if r['doi'] else ''
    return f"\\bibitem{{{r['id']}}} {esc(au)} ({r['year']}). {esc(r['title'])}. \\textit{{{esc(r['source'])}}}.{doi}"
open('../articulo/refs_incluidos.tex', 'w').write('\n\n'.join(apa(r) for r in inc) + '\n')

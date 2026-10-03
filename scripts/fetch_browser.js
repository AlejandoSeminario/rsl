// Tercera vía: navegador Chromium para sitios con protección anti-bots (MDPI, ACM, Springer, JMIR).
const { chromium } = require(process.env.PW || 'playwright');
const fs = require('fs');
const D = process.env.FTDIR;
const src = JSON.parse(fs.readFileSync('../data/fulltext_sources.json'));
const st = JSON.parse(fs.readFileSync('../data/fulltext_status.json'));
function urls(v) {
  const u = [];
  if (v.oa && v.oa.url) u.push(v.oa.url);
  const d = v.doi;
  if (d.startsWith('10.1145/')) u.push(`https://dl.acm.org/doi/pdf/${d}`);
  if (d.startsWith('10.1007/')) u.push(`https://link.springer.com/content/pdf/${d}.pdf`);
  u.push(`https://doi.org/${d}`);
  return u;
}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const ctx = await b.newContext({ acceptDownloads: true, userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36' });
  for (const [k, v] of Object.entries(src)) {
    if (!v || !st[k].startsWith('FAIL')) continue;
    if (v.doi.startsWith('10.1109/')) continue; // IEEE Xplore: acceso por suscripción
    for (const u of urls(v)) {
      try {
        const r = await ctx.request.get(u, { timeout: 60000 });
        const body = await r.body();
        if (body.slice(0, 5).toString() === '%PDF-' && body.length > 20000) { fs.writeFileSync(`${D}/${k}.pdf`, body); st[k] = 'ok browser ' + u; break; }
        const p = await ctx.newPage();
        await p.goto(u, { timeout: 60000, waitUntil: 'domcontentloaded' }).catch(() => {});
        await p.waitForTimeout(4000);
        const txt = await p.evaluate(() => document.body ? document.body.innerText : '');
        await p.close();
        if (txt.length > 15000 && /introduction|method/i.test(txt)) { fs.writeFileSync(`${D}/${k}.txt`, txt); st[k] = 'ok browser-html ' + u; break; }
      } catch (e) { }
    }
    console.log(k, st[k]);
  }
  fs.writeFileSync('../data/fulltext_status.json', JSON.stringify(st, null, 1));
  await b.close();
})();

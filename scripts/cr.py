import json, sys, time, urllib.parse, urllib.request, re
P = ["social robot", "social robotics", "socially assistive robot", "companion robot", "human-robot interaction"]
I = ["large language model", "generative AI", "vision-language model", "foundation model", "GPT", "ChatGPT"]
recs = {}
for p in P:
    for i in I:
        q = f"{p} {i}"
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode({
            "query.bibliographic": q, "rows": 100,
            "filter": "from-pub-date:2020-01-01,until-pub-date:2026-12-31",
            "select": "DOI,title,author,container-title,type,issued,abstract"})
        for a in range(5):
            try: d = json.load(urllib.request.urlopen(url, timeout=90)); break
            except Exception as e: print("retry", e, file=sys.stderr); time.sleep(3*(a+1))
        for it in d["message"]["items"]:
            recs[it["DOI"].lower()] = it
        print(q, len(recs), file=sys.stderr)
json.dump({"date": time.strftime("%Y-%m-%d"), "data": list(recs.values())}, open("../data/cr_all.json", "w"))

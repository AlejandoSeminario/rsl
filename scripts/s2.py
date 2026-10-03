import json, sys, time, urllib.parse, urllib.request
Q = ('("social robot" | "social robots" | "social robotics" | "socially assistive robot" | "socially assistive robots" | "companion robot" | "human-robot interaction") + '
     '("large language model" | "large language models" | "generative AI" | "generative artificial intelligence" | "vision-language model" | "foundation model" | "GPT" | "ChatGPT" | "multimodal LLM")')
base = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
params = {"query": Q, "year": "2020-2026", "fields": "title,year,venue,publicationTypes,externalIds,abstract,authors,journal,publicationDate"}
out, token = [], None
while True:
    p = dict(params)
    if token: p["token"] = token
    url = base + "?" + urllib.parse.urlencode(p)
    for a in range(6):
        try:
            d = json.load(urllib.request.urlopen(url, timeout=60)); break
        except Exception as e:
            print("retry", e, file=sys.stderr); time.sleep(3*(a+1))
    out += d["data"]; token = d.get("token")
    print(d.get("total"), len(out), file=sys.stderr)
    if not token: break
json.dump({"query": Q, "date": time.strftime("%Y-%m-%d"), "data": out}, open("../data/s2_all.json", "w"))

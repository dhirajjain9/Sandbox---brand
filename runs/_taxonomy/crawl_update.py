import json,sys
D="/home/user/Sandbox---brand/runs/_taxonomy/"
PRI=["Kitchen & Dining","Kitchen & Home Appliances","Appliances","Home Furnishing","Home & Décor","Indoor Lighting","Home Storage & Organisation","Heating, Cooling & Air Quality","Large Appliances","Furniture","Religious & Spiritual Items","Bath","Home Improvement","Artwork"]
SKIPN=("craft materials","warrant")
resp=json.load(sys.stdin)
fr=json.load(open(D+"frontier.json"))
idx={e["catId"]:e for e in fr}
got=set(); new=[]
seen={json.loads(l)["catId"] for l in open(D+"keepa_in_tree.jsonl")}
dup=[]
out=open(D+"keepa_in_tree.jsonl","a")
for c in resp["categories"]:
    e=idx.get(c["catId"])
    if e is None: print("unknown",c["catId"]); continue
    got.add(c["catId"])
    path=(e["path_prefix"]+" > "+c["name"]) if e["path_prefix"] else e.get("rootName",c["name"])
    kids=c.get("childCategoryIds") or []
    rec=dict(catId=c["catId"],name=c["name"],parent=e["parent"] or c.get("parent"),depth=e["depth"],path=path,
      productCount=c.get("productCount"),brandCount=c.get("brandCount"),isBrowseNode=c.get("isBrowseNode"),
      avgBuyBoxPrice=c.get("avgBuyBoxPrice"),childCategoryIds=kids,childCategoryCount=c.get("childCategoryCount",len(kids)),branch=e["branch"])
    expand = c.get("isBrowseNode") and (c.get("productCount") or 0)>0 and not any(s in c["name"].lower() for s in SKIPN)
    rec["expanded"]=bool(expand and kids)
    out.write(json.dumps(rec,ensure_ascii=False)+"\n")
    if expand:
        for k in kids:
            if k in idx or k in seen or any(n["catId"]==k for n in new): dup.append(k)
            else: new.append({"catId":k,"parent":c["catId"],"depth":e["depth"]+1,"path_prefix":path,"branch":e["branch"]})
missing=[i for i in idx if i in set(json.loads(sys.argv[1])) and i not in got] if len(sys.argv)>1 else []
# requested but not returned: drop to avoid loops, log
for m in missing:
    out.write(json.dumps(dict(catId=m,parent=idx[m]["parent"],depth=idx[m]["depth"],path=idx[m]["path_prefix"]+" > ?",notFound=True,branch=idx[m]["branch"]))+"\n")
    got.add(m)
fr=[e for e in fr if e["catId"] not in got]+new
fr.sort(key=lambda e:(e["depth"],PRI.index(e["branch"])))  # stable
json.dump(fr,open(D+"frontier.json","w"),indent=0,ensure_ascii=False)
print("dups skipped",len(dup));print("recorded",len(got),"frontier",len(fr),"left",resp.get("apiTokens",{}).get("left"))
nxt=[e["catId"] for e in fr if e["depth"]<5][:10]
print("NEXT",json.dumps(nxt))

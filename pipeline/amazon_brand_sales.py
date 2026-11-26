"""Amazon India 30-day sales by brand (Helium 10), for every brand in the quick-commerce table.

    python -m pipeline.amazon_brand_sales extract    # parse Helium 10 batch pulls from session transcripts
    python -m pipeline.amazon_brand_sales build      # join with runs/_qcom/qcom_brand_sales.csv

Pulls are search_products calls (marketplace IN, brand_include = a batch of brands,
child_monthly_sales_from = 1, top 500 listings by revenue). A brand whose own query hit 500 rows
is flagged `capped` (its figure covers its top 500 listings, nearly all of its sales).

Outputs:
- data/raw/helium10/qcom_brands/rows.csv.gz   listing rows (gitignored)
- runs/_qcom/amazon_brand_sales_30d.csv       brand, units, revenue, selling listings, capped
- runs/_qcom/qcom_amazon_by_category.csv      quick-commerce category x brand, Sep/Oct 2026 by platform,
                                              with the brand's Amazon 30-day sales alongside
"""
import glob
import json
import os
import re
import sys

import pandas as pd

TRANSCRIPTS = "/root/.claude/projects/*/**/*.jsonl"
CTX = "Amazon 30-day sales for quick-commerce brands"
RAW = "data/raw/helium10/qcom_brands"


def slug(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def split_brands(s):
    out, cur, q = [], "", False
    for ch in s:
        if ch == '"':
            q = not q
        elif ch == "," and not q:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    return [x for x in out if x]


def load_result(content):
    txt = content if isinstance(content, str) else "".join(x.get("text", "") for x in content or [] if isinstance(x, dict))
    m = re.search(r"Output has been saved to (\S+\.txt)", txt)
    if m and os.path.exists(m.group(1)):
        txt = open(m.group(1)).read()
    t = txt.strip()
    try:
        return json.loads(t[: t.rfind("}") + 1])
    except Exception:
        return None


def extract():
    rows, queries = [], []
    for src in glob.glob(TRANSCRIPTS, recursive=True):
        calls, res = {}, []
        for line in open(src):
            try:
                c = json.loads(line).get("message", {}).get("content")
            except Exception:
                continue
            if not isinstance(c, list):
                continue
            for b in c:
                if b.get("type") == "tool_use" and b.get("name") == "mcp__Helium_10__search_products" \
                        and str(b.get("input", {}).get("context", "")).startswith(CTX):
                    calls[b["id"]] = b["input"]
                elif b.get("type") == "tool_result":
                    res.append((b["tool_use_id"], b.get("content")))
        for tid, content in res:
            if tid not in calls:
                continue
            j = load_result(content)
            if not j or not j.get("data"):
                continue
            brands = split_brands(calls[tid]["filters"]["brand_include"])
            P = j["data"]["products"]
            capped = bool(j["data"]["pagination"].get("has_more"))
            queries.append({"brands": brands, "rows": len(P), "capped": capped})
            for p in P:
                rows.append({"asin": p["amazon_standard_identification_number"], "brand": p.get("brand"),
                             "units": p.get("child_monthly_sales") or 0, "revenue_rs": (p.get("child_monthly_revenue") or 0) / 100})
    if not rows:
        sys.exit("no Helium 10 batch results found")
    d = pd.DataFrame(rows).drop_duplicates("asin")
    os.makedirs(RAW, exist_ok=True)
    d.to_csv(f"{RAW}/rows.csv.gz", index=False)
    json.dump(queries, open(f"{RAW}/queries.json", "w"))
    print(f"{len(queries)} queries, {len(d):,} listings, {d.brand.nunique():,} Amazon brand names")


def build():
    d = pd.read_csv(f"{RAW}/rows.csv.gz")
    queries = json.load(open(f"{RAW}/queries.json"))
    asked = {slug(b) for q in queries for b in q["brands"]}
    capped = {slug(q["brands"][0]) for q in queries if q["capped"] and len(q["brands"]) == 1}
    d["brand_key"] = d.brand.map(slug)
    a = (d.groupby("brand_key").agg(amazon_brand=("brand", lambda s: s.mode().iat[0]), amazon_listings=("asin", "count"),
                                    amazon_units_30d=("units", "sum"), amazon_revenue_30d_rs=("revenue_rs", "sum")).reset_index())
    a["amazon_revenue_30d_lakh"] = (a.amazon_revenue_30d_rs / 1e5).round(2)
    a["capped_top500"] = a.brand_key.isin(capped)
    q = pd.read_csv("runs/_qcom/qcom_brand_sales.csv")
    names = q.groupby("brand_key").brand.first().reset_index()
    a = names.merge(a, on="brand_key", how="left")
    a["amazon_status"] = a.apply(lambda r: "found" if r.amazon_listings == r.amazon_listings and r.amazon_listings > 0
                                 else ("no selling listing" if r.brand_key in asked else "not queried"), axis=1)
    a = a.drop(columns="amazon_revenue_30d_rs")
    a.to_csv("runs/_qcom/amazon_brand_sales_30d.csv", index=False)
    m = q[q.month.isin(["2026-09", "2026-10"])].pivot_table(index=["platform", "category", "brand", "brand_key"], columns="month",
                                                           values=["sales_mrp_lakh", "sales_sp_lakh", "share_mrp_pct", "skus"], aggfunc="sum")
    m.columns = [f"{v}_{c.replace('2026-', '')}" for v, c in m.columns]
    m = m.reset_index().merge(a[["brand_key", "amazon_units_30d", "amazon_revenue_30d_lakh", "amazon_listings", "capped_top500", "amazon_status"]],
                              on="brand_key", how="left")
    m.to_csv("runs/_qcom/qcom_amazon_by_category.csv", index=False)
    f = a.amazon_status.value_counts().to_dict()
    print(f"brands: {f}; Amazon 30-day total Rs {a.amazon_revenue_30d_lakh.sum() / 100:,.1f} Cr; {len(m):,} category rows")


if __name__ == "__main__":
    {"extract": extract, "build": build}[sys.argv[1]]()

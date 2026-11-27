"""Amazon India 30-day sales by brand (Helium 10), for every brand in the quick-commerce table.

    python -m pipeline.amazon_brand_sales extract    # parse Helium 10 batch pulls from session transcripts
    python -m pipeline.amazon_brand_sales import-csv <folder> [--batches runs/_sourcing/amazon_pull/batches.tsv]
                                                     # add Black Box CSV exports (browser run) to the listing rows
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


def num(s):
    return pd.to_numeric(s.astype(str).str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")


def import_csv(folder, batches=None):
    """Black Box CSV exports -> listing rows (same shape as the MCP pulls), plus 12-month units if exported."""
    files = sorted(glob.glob(os.path.join(folder, "*.csv")))
    if not files:
        sys.exit(f"no CSV files in {folder}")
    out = []
    for f in files:
        d = pd.read_csv(f)
        cols = {c.lower().strip(): c for c in d.columns}
        pick = lambda *names: next((cols[n] for n in names if n in cols), None)
        a, b = pick("asin"), pick("brand")
        rev, units, price = pick("asin revenue", "revenue"), pick("asin sales", "sales"), pick("price", "price ₹", "price (₹)")
        # Black Box's "Last Year Sales" is parent-level (repeated on every child), so it is not summed per listing
        year = next((c for c in d.columns if re.search(r"(12[- ]?month|asin year sales|annual)", c, re.I)
                     and not re.search(r"(%|over year|yoy|parent)", c, re.I)), None)
        if not (a and b and rev and units):
            print("skipped (missing ASIN/Brand/Revenue/Sales columns):", f, list(d.columns)[:12]); continue
        x = pd.DataFrame({"asin": d[a], "brand": d[b], "units": num(d[units]).fillna(0), "revenue_rs": num(d[rev]).fillna(0)})
        x["price_rs"] = num(d[price]) if price else None
        x["units_12m"] = num(d[year]) if year else None
        x["source"] = "blackbox_csv:" + os.path.basename(f)
        out.append(x)
        print(f"{os.path.basename(f)}: {len(x)} rows; 12-month column: {year or 'none'}")
    new = pd.concat(out).drop_duplicates("asin")
    old = pd.read_csv(f"{RAW}/rows.csv.gz") if os.path.exists(f"{RAW}/rows.csv.gz") else pd.DataFrame()
    allr = pd.concat([old[~old.asin.isin(new.asin)] if len(old) else old, new], ignore_index=True)
    allr.to_csv(f"{RAW}/rows.csv.gz", index=False)
    if batches:
        q = json.load(open(f"{RAW}/queries.json")) if os.path.exists(f"{RAW}/queries.json") else []
        for line in open(batches).read().splitlines()[1:]:
            q.append({"brands": [s.strip() for s in line.split("\t", 1)[1].split("|")], "rows": None, "capped": False, "source": "blackbox_csv"})
        json.dump(q, open(f"{RAW}/queries.json", "w"))
    print(f"{len(new):,} listings imported; {len(allr):,} in total")


def aliases():
    """Amazon brand slug -> our brand slug, from pipeline/brand_aliases.json ("aliases" only; "verify" is not applied)."""
    f = os.path.join(os.path.dirname(__file__), "brand_aliases.json")
    if not os.path.exists(f):
        return {}
    return {slug(amz): slug(ours) for ours, L in json.load(open(f))["aliases"].items() for amz in L}


HOME_CATS = {"Home & Kitchen", "Home Improvement", "Outdoor Living"}


def asin_categories():
    """ASIN -> Amazon top category, from every Black Box CSV on disk (API pulls carry no category)."""
    m = {}
    for f in sorted(set(glob.glob("data/raw/**/*.csv", recursive=True))):
        try:
            h = pd.read_csv(f, nrows=0).columns
        except Exception:
            continue
        if "ASIN" in h and "Category" in h:
            d = pd.read_csv(f, usecols=["ASIN", "Category"], low_memory=False).dropna()
            m.update(dict(zip(d.ASIN, d.Category)))
    return m


def build():
    d = pd.read_csv(f"{RAW}/rows.csv.gz")
    queries = json.load(open(f"{RAW}/queries.json"))
    al = aliases()
    asked = {al.get(slug(b), slug(b)) for q in queries for b in q["brands"]}
    capped = {slug(q["brands"][0]) for q in queries if q["capped"] and len(q["brands"]) == 1}
    d["brand_key"] = d.brand.map(slug).map(lambda k: al.get(k, k))
    if "units_12m" not in d:
        d["units_12m"] = None
    d["price_rs"] = d.get("price_rs", pd.Series(index=d.index, dtype=float))
    d["rev_12m_rs"] = d.units_12m * d.price_rs.fillna(d.revenue_rs / d.units.where(d.units > 0))
    a = (d.groupby("brand_key").agg(amazon_brand=("brand", lambda s: s.mode().iat[0]), amazon_listings=("asin", "count"),
                                    amazon_units_30d=("units", "sum"), amazon_revenue_30d_rs=("revenue_rs", "sum"),
                                    amazon_revenue_12m_rs=("rev_12m_rs", lambda s: s.sum(min_count=1))).reset_index())
    cat = d.asin.map(asin_categories())
    d["rev_known"] = d.revenue_rs.where(cat.notna(), 0)
    d["rev_home"] = d.revenue_rs.where(cat.isin(HOME_CATS), 0)
    d["top_cat"] = cat
    h = d.groupby("brand_key").agg(rk=("rev_known", "sum"), rh=("rev_home", "sum"), rt=("revenue_rs", "sum"))
    a["amazon_category_known_pct"] = a.brand_key.map((h.rk / h.rt.where(h.rt > 0) * 100).round(0))
    a["amazon_home_pct"] = a.brand_key.map((h.rh / h.rk.where(h.rk > 0) * 100).round(0))
    tc = d[cat.notna()].groupby(["brand_key", "top_cat"]).revenue_rs.sum().reset_index().sort_values("revenue_rs").drop_duplicates("brand_key", keep="last")
    a["amazon_main_category"] = a.brand_key.map(tc.set_index("brand_key").top_cat)
    a["amazon_revenue_12m_cr"] = (a.amazon_revenue_12m_rs / 1e7).round(2)
    a = a.drop(columns="amazon_revenue_12m_rs")
    a["amazon_revenue_30d_lakh"] = (a.amazon_revenue_30d_rs / 1e5).round(2)
    a["capped_top500"] = a.brand_key.isin(capped)
    q = pd.read_csv("runs/_qcom/qcom_brand_sales.csv")
    names = q.groupby("brand_key").brand.first().reset_index()
    if os.path.exists("runs/_target/master_list_with_exclusions.csv"):  # every target-list brand (Master File names too)
        s = pd.read_csv("runs/_target/master_list_with_exclusions.csv")[["key", "brand"]].rename(columns={"key": "brand_key"})
        names = pd.concat([names, s[~s.brand_key.isin(names.brand_key)]], ignore_index=True)
    if os.path.exists("runs/_sourcing/universe.csv"):  # Amazon-only brands from the team's universe
        s = pd.read_csv("runs/_sourcing/universe.csv")[["key", "brand"]].rename(columns={"key": "brand_key"})
        names = pd.concat([names, s[~s.brand_key.isin(names.brand_key)]], ignore_index=True)
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
    if sys.argv[1] == "import-csv":
        bt = sys.argv[sys.argv.index("--batches") + 1] if "--batches" in sys.argv else None
        import_csv(sys.argv[2], bt)
    else:
        {"extract": extract, "build": build}[sys.argv[1]]()

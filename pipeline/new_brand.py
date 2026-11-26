"""Start and track a new brand screen.

    # 1. Register the brand and scaffold its run folder (blank scoring sheet, checklist)
    python -m pipeline.new_brand add --name "TEKAVO" --group "Home & office furniture" \
        --category "Computer tables, desks and office furniture"

    # 1b. A brand house: add sister brands as sub-brands (screened together as one entity)
    python -m pipeline.new_brand subbrand --key tekavo --name FFO --amazon-brand "FFO FURNITURE FACTORY OUTLET"

    # 2. After the Helium 10 brand pull(s) are saved to data/raw/helium10/<key>/ (one per sub-brand):
    #    writes h10_<key>_asins.csv, picks the top 10 hero families, writes both Claude in Chrome
    #    run sheets with the hero ASINs and the brand's main sub-categories filled in
    python -m pipeline.new_brand heroes --key tekavo --pull data/raw/helium10/tekavo/brand_pull_*.json

    # 3. Tick stages as they finish (the dashboard shows progress); "scored" makes it a full brand
    python -m pipeline.new_brand stage --key tekavo --done competition history

    # 4. Rebuild the dashboard
    python -m pipeline.build_dashboard

Stages, in order: brand_pull, competition, history, keepa, chrome, scored.
"""
import argparse
import json
import shutil
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "pipeline" / "brands.json"
TPL = ROOT / "pipeline" / "templates"
STAGES = ["brand_pull", "competition", "history", "keepa", "chrome", "scored"]


def slug(s):
    return "".join(c for c in s.lower() if c.isalnum())


def load_reg():
    return json.loads(REG.read_text())


def save_reg(reg):
    REG.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n")


def fill(text, **kw):
    for k, v in kw.items():
        text = text.replace("{" + k + "}", str(v))
    return text


def add(a):
    reg = load_reg()
    key = a.key or slug(a.name)
    if any(b["key"] == key for b in reg):
        raise SystemExit(f"{key} already registered")
    today = a.date or date.today().isoformat()
    run = f"runs/{today}_{key}"
    (ROOT / run).mkdir(parents=True, exist_ok=True)
    shutil.copy(TPL / "screen_scoring_inputs.csv", ROOT / run / "screen_scoring_inputs.csv")
    (ROOT / run / "RUN_NOTES.md").write_text(f"""# {a.name}: brand screen

Started {today}. Group: {a.group}. Category: {a.category}.

Checklist (tick with `python -m pipeline.new_brand stage --key {key} --done <stage>`):

1. brand_pull: Helium 10 brand pull saved to data/raw/helium10/{key}/, then `new_brand heroes`
2. competition: Helium 10 peers per main sub-category, keyword paid share, seller feedback
3. history: hero rank / price history, copycats, branded search (pipeline.h10_history_metrics)
4. keepa: Claude in Chrome Keepa run (keepa_chrome_runsheet.md), discount vs list price
5. chrome: Claude in Chrome Step B run (claude_in_chrome_stepB_runsheet.md)
6. scored: inputs filled with pipeline.rescore, report written, dashboard rebuilt
""")
    reg.append({"key": key, "name": a.name, "run": run, "asof": today, "group": a.group, "category": a.category,
                "channels": a.channels or "To be checked", "report": a.report or "", "why": "Screening in progress.",
                "match": slug(a.name), "status": "screening", "stages": {s: False for s in STAGES}})
    save_reg(reg)
    print(f"registered {key} -> {run}")


def heroes(a):
    reg = load_reg()
    b = next(x for x in reg if x["key"] == a.key)
    run = ROOT / b["run"]
    P = [p for f in a.pull for p in json.load(open(f))["data"]["products"]]
    rows = []
    for p in P:
        s = (p.get("subcategories") or [{}])[0]
        rows.append({"asin": p["amazon_standard_identification_number"], "brand": p.get("brand"),
                     "parent": p.get("parent_amazon_standard_identification_number") or p["amazon_standard_identification_number"],
                     "title": p.get("title"), "seller": p.get("buy_box_seller"), "subcat": s.get("node_name"),
                     "subcat_node": s.get("node_id"), "subcat_bsr": s.get("subcategory_best_sellers_rank"),
                     "price": (p.get("price") or 0) / 100, "units": p.get("child_monthly_sales") or 0,
                     "rev": (p.get("child_monthly_revenue") or 0) / 100, "reviews": p.get("review_count"),
                     "rating": pd.to_numeric(p.get("reviews_rating"), errors="coerce"),
                     "yoy": p.get("child_sales_year_over_year"), "trend90": p.get("sales_change"), "age": p.get("age_in_months")})
    d = pd.DataFrame(rows).drop_duplicates("asin")
    subs_cfg = b.get("subBrands") or [{"name": b["name"], "amazonBrand": b["name"]}]
    amap = {slug(x["amazonBrand"]): x["name"] for x in subs_cfg}
    d["subbrand"] = d.brand.map(lambda v: amap.get(slug(str(v)), str(v)))
    d.to_csv(run / f"h10_{a.key}_asins.csv", index=False)
    top = (d.sort_values("rev", ascending=False).drop_duplicates("parent").head(a.top))
    hf = run / "h10_heroes.json"
    old = json.load(open(hf)) if hf.exists() else {}
    json.dump({r.asin: old.get(r.asin, {}) for r in top.itertuples()}, open(hf, "w"), indent=1)  # keeps copycat phrases
    sellers = d.groupby("seller").rev.sum().sort_values(ascending=False)
    main = [s for s in sellers.index[:3] if sellers[s] / sellers.sum() >= 0.05]
    seller_line = "Amazon sellers: " + ", ".join(f"**{s}** ({sellers[s] / sellers.sum():.0%} of revenue)" for s in main)
    hero_table = "| # | ASIN | Product |\n|---|---|---|\n" + "\n".join(
        f"| {i} | {r.asin} | {str(r.title)[:70]} |" for i, r in enumerate(top.itertuples(), 1))
    subs = d.groupby(["subcat"]).rev.sum().sort_values(ascending=False)
    subs = subs[subs / subs.sum() >= 0.02].head(5)
    subcat_table = "| # | Sub-category | File name |\n|---|---|---|\n" + "\n".join(
        f"| {i} | {s} | `{a.key}_peers_{slug(s)}_{date.today().isoformat()}.xlsx` |" for i, s in enumerate(subs.index, 1))
    subs_all = b.get("subBrands") or [{"name": b["name"], "amazonBrand": b["name"]}]
    if len(subs_all) > 1:
        brand_line = "A brand house screened as one: " + ", ".join(f"**{x['name']}** (Amazon brand \"{x['amazonBrand']}\")" for x in subs_all) + ". "
        brand_pull_steps = "- Run one search per brand, each with the **Brand** field set to that brand (pick every matching\n  spelling) and no other filters, and export each:\n" + "\n".join(
            f"  - **{x['amazonBrand']}** → `{a.key}_keepa_brand_{slug(x['name'])}_{date.today().isoformat()}.xlsx`" for x in subs_all)
    else:
        brand_line = ""
        brand_pull_steps = (f'- **Brand** field: type "{b["name"]}" and pick every matching option (any spelling or case). No\n  other filters.'
                            f'\n- File: `{a.key}_keepa_brand_{date.today().isoformat()}.xlsx`.')
    kw = dict(brand_line=brand_line, brand_pull_steps=brand_pull_steps, brand_names=", ".join(x["name"] for x in subs_all),
              name=b["name"], key=a.key, category=b["category"], seller_line=seller_line, hero_table=hero_table,
              subcat_table=subcat_table, date=date.today().isoformat())
    (run / "keepa_chrome_runsheet.md").write_text(fill((TPL / "keepa_runsheet.md").read_text(), **kw))
    (run / "claude_in_chrome_stepB_runsheet.md").write_text(fill((TPL / "stepB_runsheet.md").read_text(), **kw))
    tot = d.rev.sum()
    split = d.groupby("subbrand").agg(rev=("rev", "sum"), listings=("asin", "count"), seller=("seller", lambda s: s.mode().iat[0] if len(s.mode()) else ""))
    for x in subs_cfg:
        r = split.loc[x["name"]] if x["name"] in split.index else None
        x.update({"revenueMonthly": round(float(r.rev)) if r is not None else 0, "share": round(float(r.rev / tot * 100), 1) if r is not None else 0,
                  "listings": int(r.listings) if r is not None else 0, "seller": r.seller if r is not None else ""})
    if b.get("subBrands"):
        b["subBrands"] = subs_cfg
        print("sub-brands:", {x["name"]: f'{x["share"]}%' for x in subs_cfg})
    b["stages"]["brand_pull"] = True
    b["mainSeller"] = main[0] if main else None
    save_reg(reg)
    R = d.rev.sum()
    print(f"{len(d)} listings, {d.parent.nunique()} families, Rs {R / 1e7:.2f} crore/month; heroes: {', '.join(top.asin)}")
    print("sub-categories for competition pulls:", {s: int(subs[s] / R * 100) for s in subs.index})


def subbrand(a):
    reg = load_reg()
    b = next(x for x in reg if x["key"] == a.key)
    subs = b.setdefault("subBrands", [{"name": b["name"], "amazonBrand": b["name"]}])
    if not any(x["name"] == a.name for x in subs):
        subs.append({"name": a.name, "amazonBrand": a.amazon_brand or a.name})
    b["match"] = [slug(x["amazonBrand"]) for x in subs]
    save_reg(reg)
    print(a.key, "sub-brands:", [x["name"] for x in subs])


def stage(a):
    reg = load_reg()
    b = next(x for x in reg if x["key"] == a.key)
    for s in a.done:
        if s not in STAGES:
            raise SystemExit(f"unknown stage {s}; use one of {STAGES}")
        b.setdefault("stages", {})[s] = True
    if b["stages"].get("scored"):
        b["status"] = "scored"
    save_reg(reg)
    print(a.key, {s: b["stages"].get(s, False) for s in STAGES})


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("add")
    p.add_argument("--name", required=True)
    p.add_argument("--group", required=True, help="dashboard category, e.g. 'Kitchen appliances'")
    p.add_argument("--category", required=True, help="one-line description of what the brand sells")
    p.add_argument("--key")
    p.add_argument("--date")
    p.add_argument("--channels")
    p.add_argument("--report")
    p = sp.add_parser("heroes")
    p.add_argument("--key", required=True)
    p.add_argument("--pull", required=True, nargs="+")
    p.add_argument("--top", type=int, default=10)
    p = sp.add_parser("subbrand")
    p.add_argument("--key", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--amazon-brand", help="brand name exactly as on Amazon / Helium 10")
    p = sp.add_parser("stage")
    p.add_argument("--key", required=True)
    p.add_argument("--done", nargs="+", required=True)
    a = ap.parse_args()
    {"add": add, "heroes": heroes, "subbrand": subbrand, "stage": stage}[a.cmd](a)


if __name__ == "__main__":
    main()

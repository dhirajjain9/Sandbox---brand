"""Quick-commerce sales by brand, platform, category and month, from the GobbleCube exports.

    python -m pipeline.qcom_brand_sales build             # rebuild runs/_qcom/qcom_brand_sales.csv
    python -m pipeline.qcom_brand_sales brand nestroots   # one brand, platform-wise, every period
    python -m pipeline.qcom_brand_sales brand "aura decor" --by category

Sales = the brand's Est. Category Share (sum over its SKUs; GobbleCube shows it in %) x the
category's estimated size for that month. MRP share x MRP size gives sales at MRP; SP share x SP
size gives sales at selling price. GobbleCube's Offtake / Units columns are blank on our plan.

Sources (data/raw/gobblecube/, gitignored; the output table is committed):
- vetting_qcomm_raw_2026-11-23.xlsx, sheet R_GobbleCube_RCA_JulOct: SKU rows, all brands, Blinkit /
  Zepto / Instamart, home and kitchen categories, Jul-Oct 2026 (cached as rca_JulOct.csv.gz)
- same workbook, sheet R_Category_Size_SepOct: every category's size, MRP and SP, Sep-Oct 2026
- deep_dive/*category_size_blinkit.csv: Blinkit Home Decor, Festive Gifting, Pooja Needs, MRP only,
  Aug 2025 - Nov 2026 (Nov 2026 partial, 22 days)
- deep_dive/*homedecor_top5_brands_blinkit.csv: top 5 brands' share of Blinkit Home Decor, Aug 2025 on

Months with a share but no category size keep the share and leave sales blank. To add a new
GobbleCube export, drop it in data/raw/gobblecube/, extend load_*() below, and rebuild.
"""
import argparse
import glob
import os
import re
import sys

import pandas as pd

RAW = "data/raw/gobblecube"
OUT = "runs/_qcom/qcom_brand_sales.csv"


def slug(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def rca():
    cache = f"{RAW}/rca_JulOct.csv.gz"
    if not os.path.exists(cache):
        import openpyxl
        ws = openpyxl.load_workbook(f"{RAW}/vetting_qcomm_raw_2026-11-23.xlsx", read_only=True)["R_GobbleCube_RCA_JulOct"]
        it = ws.iter_rows(values_only=True)
        pd.DataFrame(it, columns=next(it)).to_csv(cache, index=False)
    d = pd.read_csv(cache)
    d["month"] = d.Date.str[:7]
    return d


def sizes():
    import openpyxl
    ws = openpyxl.load_workbook(f"{RAW}/vetting_qcomm_raw_2026-11-23.xlsx", read_only=True)["R_Category_Size_SepOct"]
    it = ws.iter_rows(values_only=True)
    a = pd.DataFrame(it, columns=next(it))
    a["month"] = pd.to_datetime(a.month, format="%b %Y").dt.strftime("%Y-%m")
    a = a.rename(columns={"size_mrp_cr": "size_mrp_cr", "size_sp_cr": "size_sp_cr"})[["platform", "category", "month", "size_mrp_cr", "size_sp_cr"]]
    a["size_source"] = "R_Category_Size_SepOct"
    b = pd.read_csv(glob.glob(f"{RAW}/deep_dive/*category_size_blinkit.csv")[0])
    b = b.assign(size_mrp_cr=pd.to_numeric(b.size_mrp, errors="coerce"), size_sp_cr=None,
                 size_source=b.days_covered.map(lambda x: "deep_dive (MRP only)" + ("" if x >= 28 else f", {x} days")))
    b = b[["platform", "category", "month", "size_mrp_cr", "size_sp_cr", "size_source"]]
    s = pd.concat([a, b]).drop_duplicates(["platform", "category", "month"], keep="first")
    return s


def build():
    d = rca()
    g = (d.groupby(["Platform", "Category", "month", "Brand"])
         .agg(skus=("Product Name", "nunique"), share_mrp_pct=("Est. Category Share", "sum"),
              share_sp_pct=("Est. Category Share SP", "sum"), osa_pct=("Wt. OSA %", "mean"),
              discount_pct=("Wt. Discount %", "mean")).reset_index()
         .rename(columns={"Platform": "platform", "Category": "category", "Brand": "brand"}))
    g["source"] = "RCA Jul-Oct 2026 (SKU rows)"
    t = pd.read_csv(glob.glob(f"{RAW}/deep_dive/*homedecor_top5_brands_blinkit.csv")[0])
    t = t.rename(columns={"est_cat_share_mrp_pct": "share_mrp_pct", "wt_discount_pct": "discount_pct"})
    t["platform"], t["source"] = "Blinkit", "deep_dive top 5 brands, Home Decor"
    t = t[["platform", "category", "month", "brand", "share_mrp_pct", "discount_pct", "source"]]
    key = ["platform", "category", "month", "brand"]
    t = t[~t.set_index(key).index.isin(g.set_index(key).index)]
    g = pd.concat([g, t], ignore_index=True)
    g = g.merge(sizes(), on=["platform", "category", "month"], how="left")
    g["sales_mrp_lakh"] = (g.share_mrp_pct / 100 * g.size_mrp_cr * 100).round(2)
    g["sales_sp_lakh"] = (g.share_sp_pct / 100 * g.size_sp_cr.astype(float) * 100).round(2)
    g["brand_key"] = g.brand.map(slug)
    for c in ["share_mrp_pct", "share_sp_pct", "osa_pct", "discount_pct"]:
        g[c] = g[c].round(4)
    cols = ["brand", "brand_key", "platform", "category", "month", "skus", "share_mrp_pct", "share_sp_pct",
            "size_mrp_cr", "size_sp_cr", "sales_mrp_lakh", "sales_sp_lakh", "osa_pct", "discount_pct", "source", "size_source"]
    g = g[cols].sort_values(["brand_key", "platform", "category", "month"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    g.to_csv(OUT, index=False)
    print(f"wrote {OUT}: {len(g):,} rows, {g.brand_key.nunique():,} brands, months {g.month.min()} to {g.month.max()}, "
          f"{g.sales_mrp_lakh.notna().mean():.0%} of rows with sales")


def brand(name, by):
    g = pd.read_csv(OUT)
    k = slug(name)
    b = g[g.brand_key == k]
    if b.empty:
        hits = sorted(g.loc[g.brand_key.str.contains(k[:5]), "brand"].unique())[:15]
        sys.exit(f"no rows for '{name}'. Close matches: {hits or 'none'}. Not listed in the exported categories, or spelled differently.")
    idx = ["platform", "category", "month"] if by == "category" else ["platform", "month"]
    agg = dict(skus=("skus", lambda s: s.sum(min_count=1)))
    if by == "category":
        agg["share_mrp_pct"] = ("share_mrp_pct", "sum")
    t = b.groupby(idx).agg(**agg,
                           sales_mrp_lakh=("sales_mrp_lakh", lambda s: s.sum(min_count=1)),
                           sales_sp_lakh=("sales_sp_lakh", lambda s: s.sum(min_count=1)),
                           osa_pct=("osa_pct", "mean")).round(2)
    print(f"{b.brand.iloc[0]}: quick-commerce sales by {' / '.join(idx)} (Rs lakh; blank = no category size for that month)")
    print(t.to_string())
    seen = set(b.platform)
    missing = [p for p in ["Blinkit", "Zepto", "Instamart"] if p not in seen]
    if missing:
        print("not found on:", ", ".join(missing), "(within the exported home and kitchen categories)")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("build")
    p = sp.add_parser("brand")
    p.add_argument("name")
    p.add_argument("--by", choices=["platform", "category"], default="platform")
    a = ap.parse_args()
    build() if a.cmd == "build" else brand(a.name, a.by)


if __name__ == "__main__":
    main()

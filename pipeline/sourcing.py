"""Sourcing universe: the team's brand list (CH dashboard workbook) joined with our own data.

    python -m pipeline.sourcing data/raw/sourcing/ch_dashboard_2026-11-26.xlsx

Base: the workbook's Brand Summary (1,562 brands with ARR > Rs 1 Cr; Amazon from bestseller-list
pulls, quick commerce from GobbleCube, both annualised x12), with status and outreach status. Master
File adds the owner (person to reach out), priority and the standardised skip reason. Financials in the
Master File are not carried over.

Our data joined on brand name (lower case, letters and digits only):
- Amazon full brand pull, 30 days to 26 Nov 2026 (runs/_qcom/amazon_brand_sales_30d.csv), x12.
  Bestseller lists miss a brand's long tail: across 205 brands the full pull is a median 9.6x the
  workbook figure (30x for brands under Rs 0.1 Cr a month). Brands at 3x or more are flagged.
- Quick commerce at selling price, Sep-Oct 2026 average x12 (runs/_qcom/qcom_brand_sales.csv).
- Brand Fit Screen verdict for screened brands (pipeline/brands.json).
Both of our figures cover the festive season (Diwali 8 Nov 2026) and overstate a normal month; the
workbook's quick-commerce figures cover the same Sep-Oct period.

Output: runs/_sourcing/universe.csv (one row per brand).
"""
import json
import os
import re
import sys

import openpyxl
import pandas as pd

TARGET = ["Part of existing list", "New"]


def slug(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def rows(wb, sheet, hdr_row, first_col):
    r = list(wb[sheet].iter_rows(values_only=True))
    h = [str(x).strip() if x is not None else f"_{i}" for i, x in enumerate(r[hdr_row])]
    d = pd.DataFrame(r[hdr_row + 1:], columns=h)
    return d[d[first_col].notna()]


def main(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    bs = rows(wb, "Brand Summary", 11, "Brand")
    bs = bs.rename(columns={"CH Categories": "ch_category", "Secondary Category": "secondary", "Sub - Category": "subcategory",
                            "Website": "website", "Total": "file_total_cr", "Amazon (₹ Cr)": "file_amazon_cr", "Blinkit (₹ Cr)": "file_blinkit_cr",
                            "Instamart (₹ Cr)": "file_instamart_cr", "Zepto (₹ Cr)": "file_zepto_cr", "Source": "file_source",
                            "Comments": "comment", "Status": "status", "Outreach status": "outreach"})
    bs = bs[["Brand", "ch_category", "secondary", "subcategory", "website", "file_total_cr", "file_amazon_cr", "file_blinkit_cr",
             "file_instamart_cr", "file_zepto_cr", "file_source", "comment", "status", "outreach"]].rename(columns={"Brand": "brand"})
    bs["key"] = bs.brand.map(slug)
    mf = rows(wb, "Master File", 8, "Brand Name")
    mf = pd.DataFrame({"key": mf["Brand Name"].map(slug), "owner": mf["Person to reach out"], "mf_status": mf["Status"],
                       "skip_reason": mf["Standardized reason for skipping"], "priority": mf["P0"], "revenue_band": mf["R25P2"]})
    mf = mf.drop_duplicates("key")
    u = bs.merge(mf, on="key", how="left")
    a = pd.read_csv("runs/_qcom/amazon_brand_sales_30d.csv")
    a = a[a.amazon_status != "not queried"].set_index("brand_key")
    u["amz_full_cr"] = u.key.map((a.amazon_revenue_30d_lakh.fillna(0) * 12 / 100).to_dict())
    u["amz_full_status"] = u.key.map(a.amazon_status.to_dict())
    u["amz_capped"] = u.key.map(a.capped_top500.to_dict())
    u["amz_12m_cr"] = u.key.map(a.amazon_revenue_12m_cr.to_dict()) if "amazon_revenue_12m_cr" in a else None
    sv = "data/raw/sourcing/amazon_in_sourcing_brands_summary_v2.csv"  # full-pull coverage per brand (sourcing run, 26 Nov)
    if os.path.exists(sv):
        s = pd.read_csv(sv)
        u["amz_coverage"] = u.key.map(dict(zip(s.our_brand.map(slug), s.coverage)))
    q = pd.read_csv("runs/_qcom/qcom_brand_sales.csv")
    q = q[q.month.isin(["2026-09", "2026-10"])]
    for pf in ["Blinkit", "Instamart", "Zepto"]:
        s = q[q.platform == pf].groupby("brand_key").sales_sp_lakh.sum() / 2 * 12 / 100
        u[f"qc_{pf.lower()}_cr"] = u.key.map(s.to_dict())
    u["qc_total_cr"] = u[["qc_blinkit_cr", "qc_instamart_cr", "qc_zepto_cr"]].sum(axis=1, min_count=1)
    u["amz_ratio"] = (u.amz_full_cr / pd.to_numeric(u.file_amazon_cr, errors="coerce")).where(pd.to_numeric(u.file_amazon_cr, errors="coerce") > 0)
    u["undersized"] = u.amz_ratio >= 3
    reg = json.load(open("pipeline/brands.json"))
    import pipeline.build_dashboard as bd
    tier = {}
    for b in reg:
        t = bd.load(b)["tier"]
        for m in (b["match"] if isinstance(b["match"], list) else [b["match"]]):
            tier[m] = (b["key"], t)
    u["screen_key"] = u.key.map(lambda k: tier.get(k, (None, None))[0])
    u["screen_verdict"] = u.key.map(lambda k: tier.get(k, (None, None))[1])
    u["target"] = u.status.isin(TARGET)
    u["best_total_cr"] = u[["amz_full_cr", "qc_total_cr"]].sum(axis=1, min_count=1)
    num = ["amz_12m_cr", "file_total_cr", "file_amazon_cr", "file_blinkit_cr", "file_instamart_cr", "file_zepto_cr", "amz_full_cr",
           "qc_blinkit_cr", "qc_instamart_cr", "qc_zepto_cr", "qc_total_cr", "amz_ratio", "best_total_cr"]
    for c in num:
        u[c] = pd.to_numeric(u[c], errors="coerce").round(2)
    os.makedirs("runs/_sourcing", exist_ok=True)
    u.to_csv("runs/_sourcing/universe.csv", index=False)
    t = u[u.target]
    print(f"{len(u):,} brands; target (Part of existing list + New) {len(t)}; with our Amazon pull {t.amz_full_cr.notna().sum()}, "
          f"under-sized 3x+ {int(t.undersized.sum())}; with our quick-commerce figures {t.qc_total_cr.notna().sum()}; screened {u.screen_key.notna().sum()}")
    print(u.status.value_counts().to_dict())
    print(u.outreach.value_counts().to_dict())


if __name__ == "__main__":
    main(sys.argv[1])

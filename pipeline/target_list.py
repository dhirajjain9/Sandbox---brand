"""Master target list for data extraction (set 26 Nov 2026): 1,569 brands.

    python -m pipeline.target_list data/raw/sourcing/ch_dashboard_2026-11-26.xlsx

= the team workbook's Master File brands, excluding status "Skipped" and "Skipped (Established)" (336)
+ quick-commerce brands from our GobbleCube exports that are not in the Master File (1,233).

Writes runs/_target/master_list.csv with each brand's extraction coverage:
amazon_status (found / no selling listing / not queried), Amazon 30-day and 12-month revenue, quick-commerce
sales (Sep-Oct 2026 average, selling price), and whether a Brand Fit Screen exists. Re-run after each pull.
"""
import json
import os
import re
import sys

import openpyxl
import pandas as pd

SKIP = ["Skipped", "Skipped (Established)"]


def slug(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def main(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    r = list(wb["Master File"].iter_rows(values_only=True))
    h = [str(x).strip() if x else f"_{i}" for i, x in enumerate(r[8])]
    m = pd.DataFrame(r[9:], columns=h)
    m = m[m["Brand Name"].notna()]
    m = pd.DataFrame({"brand": m["Brand Name"].astype(str).str.strip(), "mf_status": m["Status"], "mf_category": m["Category"],
                      "mf_subcategory": m["Sub-Category"], "owner": m["Person to reach out"]})
    m["key"] = m.brand.map(slug)
    m = m.drop_duplicates("key")
    q = pd.read_csv("runs/_qcom/qcom_brand_sales.csv")
    q = q[q.brand_key.notna() & (q.brand_key != "")]
    qn = q.groupby("brand_key").agg(brand=("brand", "first"), qc_category=("category", lambda s: s.value_counts().index[0]))
    mf = m[~m.mf_status.isin(SKIP)].assign(source="Master File")
    qo = qn[~qn.index.isin(m.key)].reset_index().rename(columns={"brand_key": "key"}).assign(source="Quick commerce only")
    t = pd.concat([mf, qo], ignore_index=True)
    a = pd.read_csv("runs/_qcom/amazon_brand_sales_30d.csv").set_index("brand_key")
    t["amazon_status"] = t.key.map(a.amazon_status.to_dict()).fillna("not queried")
    t["amazon_30d_lakh"] = t.key.map(a.amazon_revenue_30d_lakh.to_dict())
    t["amazon_12m_cr"] = t.key.map(a.amazon_revenue_12m_cr.to_dict()) if "amazon_revenue_12m_cr" in a else None
    s = q[q.month.isin(["2026-09", "2026-10"])]
    for pf in ["Blinkit", "Instamart", "Zepto"]:
        t[f"qc_{pf.lower()}_lakh"] = t.key.map((s[s.platform == pf].groupby("brand_key").sales_sp_lakh.sum() / 2).round(2).to_dict())
    t["qc_month_lakh"] = t[["qc_blinkit_lakh", "qc_instamart_lakh", "qc_zepto_lakh"]].sum(axis=1, min_count=1)
    t["qc_category"] = t.qc_category.fillna(t.key.map(qn.qc_category.to_dict()))
    reg = json.load(open("pipeline/brands.json"))
    sk = {mm: b["key"] for b in reg for mm in (b["match"] if isinstance(b["match"], list) else [b["match"]])}
    t["screened"] = t.key.map(sk)
    from pipeline.target_exclusions import ESTABLISHED, LISTED, NO_FIT, ROLLUP
    u = pd.read_csv("runs/_sourcing/universe.csv")
    wb_est = set(u[u.status.astype(str).str.startswith("Established")].key)
    ro = {slug(b): f"Roll-up: {g}" for g, L in ROLLUP.items() for b in L}
    li = {slug(b): f"Listed: {g}" for g, L in LISTED.items() for b in L}
    es = {slug(b) for b in ESTABLISHED}
    nf = {slug(b) for b in NO_FIT}
    t["exclude_reason"] = t.key.map(lambda x: ro.get(x) or li.get(x) or ("Established (workbook)" if x in wb_est else
                                    ("Established (well-known)" if x in es else "")))
    t.loc[(t.exclude_reason == "") & t.key.isin(nf) & (t.source == "Quick commerce only"), "exclude_reason"] = "No product fit (electronics/gaming)"
    t["in_target"] = t.exclude_reason == ""
    os.makedirs("runs/_target", exist_ok=True)
    t.to_csv("runs/_target/master_list_with_exclusions.csv", index=False)
    t[t.in_target].to_csv("runs/_target/master_list.csv", index=False)
    print(f"{len(t):,} brands before exclusions: {t.source.value_counts().to_dict()}")
    print("excluded:", t[~t.in_target].exclude_reason.str.split(":").str[0].value_counts().to_dict(), "->", int(t.in_target.sum()), "in target")
    print(pd.crosstab(t.source, t.in_target).to_string())
    t = t[t.in_target]
    print("Amazon:", t.amazon_status.value_counts().to_dict(), "| with 12-month:", int(t.amazon_12m_cr.notna().sum()))
    print("Quick commerce figures:", int(t.qc_month_lakh.notna().sum()), "| screened:", int(t.screened.notna().sum()))


if __name__ == "__main__":
    main(sys.argv[1])

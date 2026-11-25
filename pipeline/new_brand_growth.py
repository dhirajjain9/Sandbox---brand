"""Growth inputs for young brands whose listings have no year-on-year data.

Usage:
    python -m pipeline.new_brand_growth runs/<run> --brand cadlec [--heroes-top 10]

Reads runs/<run>/peers_*.csv (one row per ASIN per sub-category, from Helium 10 product research,
with columns brand, units, revenue, yoy, sales_change_90d, and optionally parent) and prints the
fallback values for three inputs. Use them only when listings with a year-ago figure cover less
than half of the brand's revenue (Helium 10 reports a missing year-on-year figure as 0).

Season adjustment: a 90-day window is seasonal (Diwali, summer for fans, winter for heaters), so
each figure compares the brand's 90-day growth with its own sub-category's 90-day growth over the
same window (other brands only). Growth is the implied ratio sum(current) / sum(current / (1 + g)).

- 2b (hero growth count): product families with >= 300 units a month whose 90-day growth beats
  their sub-category's by >= 50% (relative).
- 3a (order growth of heroes): median season-adjusted 90-day growth of the top hero families.
- 4c (growth vs category): brand revenue now vs what it would be had every sub-category position
  grown at its category's 90-day rate, minus 1 (mix-weighted, so the biggest families dominate).
"""
import argparse
import glob
import statistics as st

import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--heroes-top", type=int, default=10)
    ap.add_argument("--families", help="CSV with asin,parent to group variation families")
    a = ap.parse_args()
    fmap = pd.read_csv(a.families).set_index("asin")["parent"].to_dict() if a.families else {}
    rows, cur, prior, exp_prior = [], 0.0, 0.0, 0.0
    yoy_cov_num = yoy_cov_den = 0.0
    for f in sorted(glob.glob(f"{a.run}/peers_*.csv")):
        p = pd.read_csv(f)
        is_b = p.brand.fillna("").str.casefold().str.replace(" ", "") == a.brand.casefold()
        b = p[is_b]
        yoy_cov_num += b.loc[b.yoy.fillna(0) != 0, "revenue"].sum()
        yoy_cov_den += b.revenue.sum()
        p = p[p.sales_change_90d.notna() & (p.sales_change_90d > -100)]
        b, o = p[is_b.loc[p.index]], p[~is_b.loc[p.index]]
        if b.empty or o.empty:
            continue
        k = o.revenue.sum() / (o.revenue / (1 + o.sales_change_90d / 100)).sum() - 1
        pc = (b.revenue / (1 + b.sales_change_90d / 100)).sum()
        cur, prior, exp_prior = cur + b.revenue.sum(), prior + pc, exp_prior + pc * (1 + k)
        fam = b.asin.map(lambda x: fmap.get(x, x))
        g = b.assign(fam=fam).groupby("fam").agg(units=("units", "sum"), revenue=("revenue", "sum"),
                                                 g90=("sales_change_90d", "first"))
        for fid, r in g.iterrows():
            rows.append((fid, f.split("peers_")[-1][:-4], r.units, r.revenue, r.g90, k * 100,
                         ((1 + r.g90 / 100) / (1 + k) - 1) * 100))
    h = pd.DataFrame(rows, columns=["family", "subcat", "units", "revenue", "brand_90d_pct",
                                    "category_90d_pct", "relative_pct"]).sort_values("revenue", ascending=False)
    print(f"Revenue with a year-ago figure: {yoy_cov_num / yoy_cov_den:.0%} (use the fallback if under 50%)")
    print(h.head(a.heroes_top).round(0).to_string(index=False))
    n2b = int(((h.units >= 300) & (h.relative_pct >= 50)).sum())
    top = h.head(a.heroes_top)
    print(f"2b = {n2b}  (families >= 300 units beating category 90-day growth by >= 50%)")
    print(f"3a = {st.median(top.relative_pct) / 100:.2f}  (median season-adjusted 90-day growth, top {len(top)} families)")
    print(f"4c = {cur / exp_prior - 1:.2f}  (brand 90-day growth {cur / prior - 1:+.0%} vs category mix {exp_prior / prior - 1:+.0%})")


if __name__ == "__main__":
    main()

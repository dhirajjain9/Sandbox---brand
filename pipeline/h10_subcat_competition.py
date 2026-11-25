"""Brand-level competition table from a Helium 10 Black Box sub-category export.

Usage:
    python -m pipeline.h10_subcat_competition <blackbox.csv> --brand AuraDecor --out <out.csv>

Black Box exports one row per ASIN. This rolls them up to brand level:
units, revenue, share, average price, rating (weighted by review count),
year-on-year growth (implied from each ASIN's YoY %, weighted by units) and
dependence on the brand's top ASIN.

Note: review counts are pooled across variation families on Amazon, so the
'reviews' total double counts siblings. Use it for weighting, not as a count.
"""
import argparse

import numpy as np
import pandas as pd

NUMERIC = [
    "ASIN Sales", "ASIN Revenue", "Price", "Review Count", "Reviews Rating",
    "Sales Year Over Year (%)", "Sales Trend (90 days) (%)", "Listing Age (Months)",
    "Number of Active Sellers",
]


def split_brand(df: pd.DataFrame, brand: str, seller: str, label_seller: str, label_other: str) -> pd.DataFrame:
    """Split one brand name into two brands by seller.

    Example: "Milton" sold by HYDRO VALVES. is Milton Home Appliances; every other
    "Milton" listing is the original Milton (Hamilton Housewares) line.
    """
    is_brand = df["Brand"].str.casefold() == brand.casefold()
    by_seller = df["Seller"].fillna("").str.strip().str.casefold() == seller.strip().casefold()
    df.loc[is_brand & by_seller, "Brand"] = label_seller
    df.loc[is_brand & ~by_seller, "Brand"] = label_other
    return df


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for c in NUMERIC:
        if c in df:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ""), errors="coerce")
    df["Brand"] = df["Brand"].fillna("(blank)").str.strip()
    # Merge case variants ("Milton" / "MILTON") under the most common spelling.
    key = df["Brand"].str.casefold()
    canon = df.groupby(key)["Brand"].agg(lambda s: s.value_counts().index[0])
    df["Brand"] = key.map(canon)
    return df


def implied_growth(g: pd.DataFrame, col: str) -> float:
    t = g.dropna(subset=[col])
    t = t[t[col] > -100]
    if t.empty:
        return np.nan
    prior = (t["ASIN Sales"] / (1 + t[col] / 100)).sum()
    return (t["ASIN Sales"].sum() / prior - 1) * 100 if prior else np.nan


def brand_table(df: pd.DataFrame) -> pd.DataFrame:
    units_total = df["ASIN Sales"].sum()
    rev_total = df["ASIN Revenue"].sum()

    def agg(g: pd.DataFrame) -> pd.Series:
        units = g["ASIN Sales"].sum()
        rev = g["ASIN Revenue"].sum()
        rc = g["Review Count"].fillna(0)
        return pd.Series({
            "asins": len(g),
            "units": units,
            "rev_lakh": rev / 1e5,
            "avg_price": rev / units if units else np.nan,
            "wtd_rating": (g["Reviews Rating"] * rc).sum() / rc.sum() if rc.sum() else np.nan,
            "yoy_pct": implied_growth(g, "Sales Year Over Year (%)"),
            "trend90_pct": implied_growth(g, "Sales Trend (90 days) (%)"),
            "top_asin_share": g["ASIN Sales"].max() / units if units else np.nan,
            "med_age_months": g["Listing Age (Months)"].median(),
        })

    b = df.groupby("Brand").apply(agg, include_groups=False).sort_values("units", ascending=False)
    b["unit_share_pct"] = b["units"] / units_total * 100
    b["rev_share_pct"] = b["rev_lakh"] * 1e5 / rev_total * 100
    b.insert(0, "rank", range(1, len(b) + 1))
    return b


def summary(df: pd.DataFrame, b: pd.DataFrame, brand: str | None) -> str:
    u, r = df["ASIN Sales"].sum(), df["ASIN Revenue"].sum()
    lines = [
        f"Sub-categories: {df['Subcategory'].value_counts().to_dict()}",
        f"Rows {len(df)} | min ASIN sales {df['ASIN Sales'].min():.0f} | brands {len(b)}",
        f"Units {u:,.0f} | revenue Rs {r/1e5:,.1f} lakh | ASP Rs {r/u:,.0f}",
        f"Top-5 brand unit share {b['unit_share_pct'].head(5).sum():.1f}%",
        f"Category YoY (implied) {implied_growth(df, 'Sales Year Over Year (%)'):.1f}%",
    ]
    if brand:
        key = brand.lower().replace(" ", "")
        hit = b[b.index.str.lower().str.replace(" ", "") == key]
        lines.append(f"{brand}: " + (hit.round(2).to_dict("records")[0].__repr__() if len(hit) else "not in this export"))
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--brand")
    ap.add_argument("--out")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--split", nargs=4, metavar=("BRAND", "SELLER", "LABEL_SELLER", "LABEL_OTHER"),
                    help="split BRAND into two brands by seller, e.g. Milton 'HYDRO VALVES.' "
                         "'Milton (Hydro Valves)' 'Milton (original)'")
    a = ap.parse_args()
    df = load(a.path)
    if a.split:
        df = split_brand(df, *a.split)
    b = brand_table(df)
    print(summary(df, b, a.brand))
    with pd.option_context("display.width", 250):
        print(b.head(a.top).round(2).to_string())
    if a.out:
        b.round(3).to_csv(a.out)


if __name__ == "__main__":
    main()

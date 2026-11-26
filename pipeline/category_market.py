"""Normalise each run's peer (competition) data into one category-market file per run.

Usage:
    python -m pipeline.category_market          # writes runs/<run>/category_market.csv for every source below

Output columns (one row per brand per sub-category, Amazon India, Helium 10 30-day estimates):
    subcategory, platform, period, brand, units, revenue, asp, rating, yoy_pct
yoy_pct is the brand's implied year-on-year growth over listings that report a year-ago figure
(Helium 10 shows a missing year-ago figure as 0; those listings are left out of yoy only).

To add a brand's categories: add an entry to SOURCES pointing at its ASIN-level peer files.
"""
import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PERIOD = "30 days to 25 Nov 2026"


def num(s):
    return pd.to_numeric(s.astype(str).str.replace(",", ""), errors="coerce")


def blackbox(files, subcat, relabel=None):
    d = pd.concat([pd.read_csv(f) for f in files]).drop_duplicates("ASIN")
    d = d[d.Subcategory == subcat]
    if relabel:
        d = relabel(d)
    return pd.DataFrame({"asin": d.ASIN, "brand": d.Brand.fillna("(no brand)").str.strip(), "units": num(d["ASIN Sales"]),
                         "revenue": num(d["ASIN Revenue"]), "yoy": num(d["Sales Year Over Year (%)"]),
                         "rating": num(d["Reviews Rating"]), "reviews": num(d["Review Count"])})


def h10_peers_csv(path):
    d = pd.read_csv(path)
    return pd.DataFrame({"asin": d.asin, "brand": d.brand.fillna("(no brand)").str.strip(), "units": d.units, "revenue": d.revenue,
                         "yoy": d.yoy, "rating": d.rating, "reviews": d.review_count})


def h10_json(path):
    p = pd.DataFrame(json.load(open(path))["data"]["products"])
    return pd.DataFrame({"asin": p.amazon_standard_identification_number, "brand": p.brand.fillna("(no brand)").str.strip(),
                         "units": p.child_monthly_sales, "revenue": p.child_monthly_revenue / 100, "yoy": p.child_sales_year_over_year,
                         "rating": pd.to_numeric(p.reviews_rating, errors="coerce"), "reviews": p.review_count})


def milton_split(d):
    d = d.copy()
    m = d.Brand.astype(str).str.casefold() == "milton"
    hv = m & d.Seller.fillna("").str.contains("HYDRO", case=False)
    d.loc[hv, "Brand"] = "Milton (Hydro Valves)"
    d.loc[m & ~hv, "Brand"] = "Milton (original)"
    return d


RAW = ROOT / "data" / "raw" / "helium10"
SOURCES = {
    "runs/2026-11-24_auradecor": [
        ("Taper Candles", lambda: blackbox([RAW / "subcat_blackbox_2_2026-11-24.csv"], "Taper Candles")),
        ("Candle Sets", lambda: blackbox([RAW / "subcat_blackbox_3_2026-11-24.csv", RAW / "subcat_blackbox_1_2026-11-24.csv"], "Candle Sets")),
        ("Pillar Candles", lambda: blackbox([RAW / "subcat_blackbox_4_2026-11-24.csv"], "Pillar Candles")),
        ("Jar Candles", lambda: blackbox([RAW / "subcat_blackbox_5_2026-11-24.csv"], "Jar Candles")),
    ],
    "runs/2026-11-25_milton": [
        ("Electric Kettles", lambda: blackbox(sorted(glob.glob(str(RAW / "milton" / "bb_[015].csv"))), "Electric Kettles", milton_split)),
        ("Sandwich Makers", lambda: blackbox([RAW / "milton" / "bb_2.csv"], "Sandwich Makers", milton_split)),
        ("Gas Stoves", lambda: blackbox([RAW / "milton" / "bb_3.csv", RAW / "milton" / "bb_4.csv"], "Gas Stoves", milton_split)),
        ("Rice & Pasta Cookers", lambda: blackbox([RAW / "milton" / "bb_6.csv"], "Rice & Pasta Cookers", milton_split)),
        ("Air Fryers", lambda: blackbox([RAW / "milton" / "bb_7.csv", RAW / "milton" / "bb_5.csv"], "Air Fryers", milton_split)),
    ],
    "runs/2026-11-25_hokipo": [
        ("Sofa Covers", lambda: h10_json(RAW / "hokipo" / "h10_api_peers_sofacover_min30.json")),
    ],
    "runs/2026-11-26_tekavo": [
        (name, (lambda s=slug: h10_peers_csv(ROOT / "runs/2026-11-26_tekavo" / f"peers_{s}.csv")))
        for name, slug in [("Desks", "desks"), ("Computer Workstations", "computer_workstations"),
                           ("Bedside Tables", "bedside_tables"), ("Bathroom Shelves", "bathroom_shelves")]
    ],
    "runs/2026-11-25_cadlec": [
        (name, (lambda s=slug: h10_peers_csv(ROOT / "runs/2026-11-25_cadlec" / f"peers_{s}.csv")))
        for name, slug in [("Induction Cooktops", "induction_cooktop"), ("Oven Toaster Grills", "otg"), ("Ceiling Fans", "ceiling_fans"),
                           ("Mixer Grinders", "mixer_grinders"), ("Kitchen Chimneys", "wall_mount_hoods"), ("Immersion Rods", "immersion_rods")]
    ],
}


def brand_table(d):
    d = d.dropna(subset=["units", "revenue"]).drop_duplicates("asin")
    key = d.brand.str.casefold().str.replace(" ", "")
    canon = d.groupby(key).brand.agg(lambda s: s.value_counts().index[0])
    d = d.assign(brand=key.map(canon))
    rows = []
    for b, g in d.groupby("brand"):
        y = g[(g.yoy.notna()) & (g.yoy != 0) & (g.yoy > -100)]
        prior = (y.units / (1 + y.yoy / 100)).sum()
        rc = g.reviews.fillna(0)
        rows.append({"brand": b, "units": g.units.sum(), "revenue": g.revenue.sum(),
                     "rating": (g.rating * rc).sum() / rc.sum() if rc.sum() else np.nan,
                     "yoy_pct": (y.units.sum() / prior - 1) * 100 if prior else np.nan, "yoy_units": y.units.sum()})
    t = pd.DataFrame(rows)
    t["asp"] = t.revenue / t.units
    return t.sort_values("revenue", ascending=False)


def main():
    for run, subs in SOURCES.items():
        out = []
        for name, load in subs:
            try:
                t = brand_table(load())
            except FileNotFoundError as e:
                print(f"skip {run} {name}: {e}")
                continue
            t.insert(0, "period", PERIOD)
            t.insert(0, "platform", "Amazon India")
            t.insert(0, "subcategory", name)
            out.append(t)
        if out:
            df = pd.concat(out)
            df.round({"revenue": 0, "asp": 0, "rating": 2, "yoy_pct": 1}).to_csv(ROOT / run / "category_market.csv", index=False)
            print(run, df.groupby("subcategory").agg(brands=("brand", "count"), rev_cr=("revenue", lambda s: round(s.sum() / 1e7, 1))).to_dict("index"))


if __name__ == "__main__":
    main()

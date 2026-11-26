"""Category view from Black Box sub-category exports (target-list waves).

    python -m pipeline.category_wave <folder with w<N>_cat_*.csv> --group-map runs/_target/waves/wave1_subcats.json

Each export is one Amazon India sub-category (top listings by revenue, monthly sales >= 5). The file name
gives the sub-category (w1_cat_<name>.csv); the JSON maps sub-category -> our category group. Output is
appended to runs/_categories/category_market.csv (replacing earlier rows for the same sub-category), in the
same shape as each brand run's category_market.csv plus a `group` column; the dashboard's Categories
pages read it.
"""
import argparse
import glob
import json
import os
import re

import pandas as pd

from pipeline.category_market import brand_table, num

OUT = "runs/_categories/category_market.csv"


def load(f):
    d = pd.read_csv(f).drop_duplicates("ASIN")
    return pd.DataFrame({"asin": d.ASIN, "brand": d.Brand.fillna("(no brand)").astype(str).str.strip(), "units": num(d["ASIN Sales"]),
                         "revenue": num(d["ASIN Revenue"]), "yoy": num(d["Sales Year Over Year (%)"]),
                         "rating": num(d["Reviews Rating"]), "reviews": num(d["Review Count"])})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--group-map", required=True)
    ap.add_argument("--period", default="30 days to late Nov 2026")
    a = ap.parse_args()
    gm = json.load(open(a.group_map))
    gm_slug = {re.sub(r"[^a-z0-9]", "", k.lower()): (k, v) for k, v in gm.items()}
    out = []
    for f in sorted(glob.glob(os.path.join(a.folder, "*_cat_*.csv"))):
        label = re.sub(r"^w\d+_cat_", "", os.path.basename(f)[:-4])
        name, group = gm_slug.get(re.sub(r"[^a-z0-9]", "", label.lower()), (label.replace("_", " "), "Unassigned"))
        t = brand_table(load(f))
        t.insert(0, "group", group)
        t.insert(0, "period", a.period)
        t.insert(0, "platform", "Amazon India")
        t.insert(0, "subcategory", name)
        out.append(t)
        print(f"{name} ({group}): {len(t)} brands, Rs {t.revenue.sum() / 1e7:.1f} Cr")
    if not out:
        raise SystemExit("no *_cat_*.csv files found")
    new = pd.concat(out).round({"revenue": 0, "asp": 0, "rating": 2, "yoy_pct": 1})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if os.path.exists(OUT):
        old = pd.read_csv(OUT)
        new = pd.concat([old[~old.subcategory.isin(new.subcategory)], new])
    new.to_csv(OUT, index=False)
    print(f"wrote {OUT}: {new.subcategory.nunique()} sub-categories")


if __name__ == "__main__":
    main()

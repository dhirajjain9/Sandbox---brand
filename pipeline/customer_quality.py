"""Customer Quality inputs judged against the brand's own category (method from 26 Nov 2026).

Usage:
    python -m pipeline.customer_quality runs/<run>        # reads runs/<run>/customer_quality.json, rescores

Why: the fixed scales failed every brand for reasons that were partly category, partly sampling.
Seller feedback norms differ widely (furniture peers ~5% negative, appliances ~18%), ratings differ by
category, and the review sample (20 most recent + 10 most recent critical) over-represents complaints.

customer_quality.json (raw figures; the script fills the derived block):
{
  "category_group": "Furniture",                   # row group in runs/_benchmarks/seller_feedback_peers_*.csv
  "rating": 4.21, "category_rating": 4.12,         # same sub-categories, revenue-weighted (category_market.csv)
  "one_two_star": 0.098,                           # 9a, rating-weighted share of 1-2 star ratings
  "sample_problem_share": 0.539,                   # share of reviews read citing damage/defect/missing/wrong item
  "sample_design": "recent+critical",              # or "recent" (no correction needed)
  "seller_negative_90d": 0.35                      # revenue-weighted across the brand's sellers
}

Inputs it sets:
- 9b Product problems per buyer = sample share x (1-2 star share / critical share of the sample),
  where the sample's critical share = (10 + 20 x 1-2 star share) / 30. Scale 2% (100) to 15% (0).
- 9c Rating vs category average, in stars. Scale -0.2 (0) to +0.2 (100).
- 9d Seller negative feedback / category median (peer sellers, 90 days). Scale 0.5x (100) to 2x (0).
"""
import glob
import json
import subprocess
import sys

import pandas as pd

ROWS = {
    "9b": ("Product problems per buyer (damage, defect, missing, wrong item; sample-corrected)", "L", 0.02, 0.15),
    "9c": ("Rating vs category average (stars, same sub-categories)", "H", -0.2, 0.2),
    "9d": ("Seller negative feedback vs category median (x, 90 days)", "L", 0.5, 2.0),
}


def bench():
    f = sorted(glob.glob("runs/_benchmarks/seller_feedback_peers_*.csv"))[-1]
    d = pd.read_csv(f)
    d = d[d.note.fillna("") != "screened brand"]
    return f, d.groupby("category_group").negative_90d.agg(["median", "count"])


def main():
    run = sys.argv[1].rstrip("/")
    cfg = json.load(open(f"{run}/customer_quality.json"))
    src, b = bench()
    s, p = cfg["one_two_star"], cfg["sample_problem_share"]
    per_buyer = p if cfg["sample_design"] == "recent" else p * s / ((10 + 20 * s) / 30)
    gap = cfg["rating"] - cfg["category_rating"]
    med, n = b.loc[cfg["category_group"], "median"], int(b.loc[cfg["category_group"], "count"])
    ratio = cfg["seller_negative_90d"] / med
    cfg["derived"] = {"9b": round(per_buyer, 4), "9c": round(gap, 3), "9d": round(ratio, 3),
                      "category_seller_median": round(float(med), 3), "peer_sellers": n, "benchmark": src}
    json.dump(cfg, open(f"{run}/customer_quality.json", "w"), indent=1)
    df = pd.read_csv(f"{run}/screen_scoring_inputs.csv")
    for k, (label, d, lo, hi) in ROWS.items():
        df.loc[df.id == k, ["input", "dir", "floor", "ceiling"]] = [label, d, lo, hi]
    df.to_csv(f"{run}/screen_scoring_inputs.csv", index=False)
    subprocess.run([sys.executable, "-m", "pipeline.rescore", run,
                    f"9b={per_buyer}", f"9c={gap}", f"9d={ratio}"], check=True)


if __name__ == "__main__":
    main()

"""Set raw-input values in a run's screen_scoring_inputs.csv and recompute mid and output scores.

Usage:
    python -m pipeline.rescore runs/<run> 3b=-0.74 4a=2.5 6a=0.45 ...

Same method as the original scoring: an input scores 0-100 between its floor and ceiling
(reversed when lower is better); missing inputs are left out and weights rescaled; coverage =
scored weight / total weight. A check clears at >= 60. Tier: a must-clear Miss is a Pass;
otherwise 5+ Clears is Strong fit, 4 is Worth a look, fewer is Pass.
"""
import sys

import numpy as np
import pandas as pd

CHECKS = [
    ("SKU Spikiness", {"M2": .4, "M3": .6}, "No"),
    ("Demand Durability", {"M4": .4, "M5": .3, "M6": .3}, "No"),
    ("Qcomm Traction", {"M7": .5, "M8": .5}, "No"),
    ("Customer Quality Signal", {"M9": 1}, "Yes"),
    ("Pricing Power", {"M10": .5, "M11": .5}, "Yes"),
    ("Concentration Risk", {"M2": .2, "M12": .5, "M13": .3}, "No"),
]


def score(v, d, lo, hi):
    if pd.isna(v):
        return np.nan
    x = (v - lo) / (hi - lo) if d == "H" else (hi - v) / (hi - lo)
    return max(0, min(100, x * 100))


def main():
    run, sets = sys.argv[1].rstrip("/"), sys.argv[2:]
    df = pd.read_csv(f"{run}/screen_scoring_inputs.csv")
    for s in sets:
        k, v = s.split("=")
        assert (df.id == k).any(), k
        df.loc[df.id == k, "value"] = float(v)
    df["score"] = [score(v, d, lo, hi) for v, d, lo, hi in zip(df.value, df.dir, df.floor, df.ceiling)]
    mids = {}
    for m, g in df.groupby("mid", sort=False):
        a = g.dropna(subset=["score"])
        mids[m] = (np.average(a.score, weights=a.weight) if len(a) else np.nan,
                   a.weight.sum() / g.weight.sum(), len(a), len(g))
    res = []
    for name, w, mc in CHECKS:
        av = {k: v for k, v in w.items() if not np.isnan(mids[k][0])}
        s = sum(mids[k][0] * v for k, v in av.items()) / sum(av.values())
        cov = sum(mids[k][1] * v for k, v in w.items()) / sum(w.values())
        res.append((name, mc, round(s, 1), "Clear" if s >= 60 else "Miss", round(cov * 100)))
    out = pd.DataFrame(res, columns=["output", "must_clear", "score", "result", "input_coverage_pct"])
    df.to_csv(f"{run}/screen_scoring_inputs.csv", index=False)
    pd.DataFrame([(m, *v) for m, v in mids.items()],
                 columns=["mid", "score", "weight_coverage", "inputs_scored", "inputs_total"]
                 ).to_csv(f"{run}/screen_scoring_mid.csv", index=False)
    out.to_csv(f"{run}/screen_scoring_outputs.csv", index=False)
    print(out.to_string(index=False))
    must_ok = not ((out.must_clear == "Yes") & (out.result == "Miss")).any()
    clears = int((out.result == "Clear").sum())
    tier = "Pass" if not must_ok else "Strong fit" if clears >= 5 else "Worth a look" if clears >= 4 else "Pass"
    w = df.weight.sum()
    print(f"Tier: {tier} ({clears} Clears; must-clears {'passed' if must_ok else 'missed'}); "
          f"inputs scored {df.score.notna().sum()}/{len(df)}, weight coverage {df.loc[df.score.notna(), 'weight'].sum() / w:.0%}")


if __name__ == "__main__":
    main()

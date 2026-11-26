"""Build the static Brand Fit Screen dashboard from the run folders.

Usage:
    python -m pipeline.build_dashboard            # writes outputs/dashboard/index.html

Brands come from pipeline/brands.json (one entry per brand: key, name, group, category, run,
asof, channels, report, why). To add a brand, add an entry and rebuild. Reads, for each brand, runs/<run>/screen_scoring_inputs.csv, screen_scoring_mid.csv and
screen_scoring_outputs.csv, embeds them as JSON in one self-contained HTML page (no external
scripts), and writes it to outputs/dashboard/. Re-run after any rescore, then redeploy.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "dashboard"

BRANDS = json.loads((ROOT / "pipeline" / "brands.json").read_text())

MID_FEEDS = {
    "M2": "SKU Spikiness, Concentration Risk", "M3": "SKU Spikiness", "M4": "Demand Durability",
    "M5": "Demand Durability", "M6": "Demand Durability", "M7": "Qcomm Traction", "M8": "Qcomm Traction",
    "M9": "Customer Quality Signal", "M10": "Pricing Power", "M11": "Pricing Power", "M12": "Concentration Risk",
    "M13": "Concentration Risk",
}
CHECK_MIDS = {
    "SKU Spikiness": "0.4 x M2 + 0.6 x M3", "Demand Durability": "0.4 x M4 + 0.3 x M5 + 0.3 x M6",
    "Qcomm Traction": "0.5 x M7 + 0.5 x M8", "Customer Quality Signal": "M9",
    "Pricing Power": "0.5 x M10 + 0.5 x M11", "Concentration Risk": "0.2 x M2 + 0.5 x M12 + 0.3 x M13",
}


def clean(v):
    return None if pd.isna(v) else (round(float(v), 4) if isinstance(v, float) else v)


def load(b):
    run = ROOT / b["run"]
    inp = pd.read_csv(run / "screen_scoring_inputs.csv")
    mid = pd.read_csv(run / "screen_scoring_mid.csv")
    out = pd.read_csv(run / "screen_scoring_outputs.csv")
    checks = [{"name": r.output, "must": r.must_clear == "Yes", "score": clean(r.score), "result": r.result,
               "coverage": int(r.input_coverage_pct), "formula": CHECK_MIDS.get(r.output, "")} for r in out.itertuples()]
    must_ok = not any(c["must"] and c["result"] == "Miss" for c in checks)
    clears = sum(c["result"] == "Clear" for c in checks)
    # Brand verdict: FIT = through both gates (must-clear checks) and 4+ of 6 checks met; otherwise NO FIT.
    tier = "FIT" if must_ok and clears >= 4 else "NO FIT"
    scored = inp["score"].notna()
    return {**b, "tier": tier, "clears": clears, "mustOk": must_ok,
            "coverage": round(float(inp.loc[scored, "weight"].sum() / inp["weight"].sum()) * 100),
            "inputsScored": int(scored.sum()), "mustMissed": [c["name"] for c in checks if c["must"] and c["result"] == "Miss"], "inputsTotal": len(inp), "checks": checks,
            "mids": [{"id": r.mid, "feeds": MID_FEEDS.get(r.mid, ""), "score": clean(r.score),
                      "coverage": round(float(r.weight_coverage) * 100), "scored": int(r.inputs_scored),
                      "total": int(r.inputs_total)} for r in mid.itertuples()],
            "inputs": [{"id": r.id, "mid": r.mid, "name": r.input, "dir": r.dir, "floor": clean(r.floor),
                        "ceiling": clean(r.ceiling), "weight": clean(r.weight), "value": clean(r.value),
                        "score": clean(r.score)} for r in inp.itertuples()]}


def slug(s):
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")


def categories(brands):
    """Group sub-category markets (runs/<run>/category_market.csv) under each brand's group."""
    norm = lambda s: str(s).casefold().replace(" ", "")
    groups = {}
    for b in brands:
        f = ROOT / b["run"] / "category_market.csv"
        if not f.exists():
            continue
        m = pd.read_csv(f)
        for name, t in m.groupby("subcategory"):
            g = groups.setdefault(b["group"], {})
            if name in g and g[name]["revenue"] >= t.revenue.sum():
                continue
            t = t.sort_values("revenue", ascending=False).reset_index(drop=True)
            rev, units = t.revenue.sum(), t.units.sum()
            y = t[t.yoy_pct.notna() & (t.yoy_units > 0)]
            prior = (y.yoy_units / (1 + y.yoy_pct / 100)).sum()
            screened = []
            for x in brands:
                hit = t.index[t.brand.map(norm) == x["match"]]
                if len(hit):
                    i = hit[0]
                    screened.append({"key": x["key"], "rank": int(i) + 1, "revShare": round(t.revenue[i] / rev * 100, 1),
                                     "asp": clean(t.asp[i]), "rating": clean(t.rating[i])})
            g[name] = {"name": name, "slug": slug(name), "platform": t.platform[0], "period": t.period[0],
                       "revenue": float(rev), "units": int(units), "asp": round(rev / units), "brands": len(t),
                       "top5": round(t.revenue.head(5).sum() / rev * 100, 1),
                       "yoy": round((y.yoy_units.sum() / prior - 1) * 100, 1) if prior else None,
                       "yoyCoverage": round(y.yoy_units.sum() / units * 100) if units else 0,
                       "leader": t.brand[0], "screened": screened,
                       "top": [{"brand": r.brand, "revShare": round(r.revenue / rev * 100, 1), "unitShare": round(r.units / units * 100, 1),
                                "asp": clean(r.asp), "rating": clean(r.rating), "yoy": clean(r.yoy_pct),
                                "screened": next((x["key"] for x in brands if norm(r.brand) == x["match"]), None)}
                               for r in t.head(10).itertuples()]}
    return [{"name": gname, "slug": slug(gname), "subs": sorted(subs.values(), key=lambda s: -s["revenue"]),
             "brandKeys": [b["key"] for b in brands if b["group"] == gname]} for gname, subs in sorted(groups.items())]


def main():
    data = [load(b) for b in BRANDS]
    for d in data:
        d["groupSlug"] = slug(d["group"])
    cats = categories(BRANDS)
    html = (Path(__file__).with_name("dashboard_template.html").read_text()
            .replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
            .replace("/*__CATS__*/null", json.dumps(cats, ensure_ascii=False)))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(html)
    print(f"wrote {OUT / 'index.html'} ({len(html):,} bytes, {len(data)} brands, {len(cats)} categories, {sum(len(c['subs']) for c in cats)} sub-categories)")


if __name__ == "__main__":
    main()

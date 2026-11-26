"""Build the static Brand Fit Screen dashboard from the run folders.

Usage:
    python -m pipeline.build_dashboard            # writes outputs/dashboard/index.html

Reads, for each brand in BRANDS, runs/<run>/screen_scoring_inputs.csv, screen_scoring_mid.csv and
screen_scoring_outputs.csv, embeds them as JSON in one self-contained HTML page (no external
scripts), and writes it to outputs/dashboard/. Re-run after any rescore, then redeploy.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "dashboard"

BRANDS = [
    {"key": "auradecor", "name": "Aura Decor", "run": "runs/2026-11-24_auradecor", "asof": "2026-11-25",
     "category": "Candles and home fragrance", "channels": "Blinkit-led (about 87% of known sales); Amazon; D2C; Flipkart",
     "report": "https://claude.ai/artifact/CMw6k8EPzF8rAKmXQwUgNG",
     "why": "Fails on quality (seller feedback 69% negative over 3 months) and price (value brand, deep discounts)."},
    {"key": "milton", "name": "Milton Home Appliances (Hydro Valves)", "run": "runs/2026-11-25_milton", "asof": "2026-11-25",
     "category": "Small kitchen appliances", "channels": "Amazon about 98%; small D2C site; a few Flipkart listings",
     "report": "https://claude.ai/artifact/A1vRC6cBhKZmkaNvqn6Fv1",
     "why": "Fails on product defects; pricing borderline; almost entirely Amazon."},
    {"key": "hokipo", "name": "HOKIPO", "run": "runs/2026-11-25_hokipo", "asof": "2026-11-25",
     "category": "Home furnishing (sofa covers)", "channels": "Amazon-led; hokipo.in D2C; Flipkart; not on quick commerce",
     "report": "https://claude.ai/artifact/MKb17AvDJD5CQfY6uHcBmm",
     "why": "Strong pricing, but sofa-cover complaints and no growth in the core."},
    {"key": "cadlec", "name": "CADLEC", "run": "runs/2026-11-25_cadlec", "asof": "2026-11-26",
     "category": "Small kitchen and home appliances", "channels": "Amazon about Rs 5.1 crore/month; Flipkart material; small D2C; Zepto (3 products)",
     "report": "https://claude.ai/artifact/HzXsPWRsABn3e3ayitwuJq",
     "why": "Fast-growing value brand; fails on quality (23% 1-2 star) and price (57% off list)."},
]

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
    tier = "Pass" if not must_ok else ("Strong fit" if clears >= 5 else "Worth a look" if clears >= 4 else "Pass")
    scored = inp["score"].notna()
    return {**b, "tier": tier, "clears": clears, "mustOk": must_ok,
            "coverage": round(float(inp.loc[scored, "weight"].sum() / inp["weight"].sum()) * 100),
            "inputsScored": int(scored.sum()), "inputsTotal": len(inp), "checks": checks,
            "mids": [{"id": r.mid, "feeds": MID_FEEDS.get(r.mid, ""), "score": clean(r.score),
                      "coverage": round(float(r.weight_coverage) * 100), "scored": int(r.inputs_scored),
                      "total": int(r.inputs_total)} for r in mid.itertuples()],
            "inputs": [{"id": r.id, "mid": r.mid, "name": r.input, "dir": r.dir, "floor": clean(r.floor),
                        "ceiling": clean(r.ceiling), "weight": clean(r.weight), "value": clean(r.value),
                        "score": clean(r.score)} for r in inp.itertuples()]}


def main():
    data = [load(b) for b in BRANDS]
    html = (Path(__file__).with_name("dashboard_template.html").read_text()
            .replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False)))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(html)
    print(f"wrote {OUT / 'index.html'} ({len(html):,} bytes, {len(data)} brands)")


if __name__ == "__main__":
    main()

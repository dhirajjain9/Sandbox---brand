"""Hero-ASIN history metrics from Helium 10 connector pulls (Step A inputs 3b, 4a, 10b, 10f, 13a).

Usage:
    python -m pipeline.h10_history_metrics --brand hokipo --raw-dir data/raw/helium10/hokipo/history \
        --heroes heroes.json --out runs/<run>/h10_history_metrics.csv [--extract-from-transcripts]

heroes.json: {"<ASIN>": {"title": "...", "core": ["sofa cover"], "desc": ["chenille"]}, ...}
  core/desc are only needed for heroes that have a competitor pull (copycats).

Raw files in --raw-dir: bsr_<ASIN>.json (get_asin_bsr_history), price_<ASIN>.json
(get_asin_price_history, values already in rupees) and comp_<ASIN>.json
(search_competitors_by_asin, prices in paise).

--extract-from-transcripts writes those raw files from this session's subagent transcripts,
because the connector often returns BSR and price histories inline rather than as saved files.

Definitions (as of RUN_DATE):
- yoy_rank_change      = 1 - median main BSR (last 30 days) / median main BSR (same 30 days a year ago)
- rank_improvement_8wk = 1 - median main BSR (last 14 days) / median main BSR (8 weeks ago, 14 days)
- months_subcat_le_100 = months (of the last 12) whose median sub-category BSR is <= 100
- deal_days_per_month  = days with price <= 90% of the 12-month median price, / 12
- sale_event_rank_lift = median BSR on non-deal days / median BSR on deal days (needs >= 5 deal days)
- copycats_count       = competitor listings (other brands) whose title has a core phrase and whose
                         price is within +/-25% of the hero's current price; strict = also a descriptor
"""
import argparse
import csv
import glob
import json
import os
import statistics as st
from collections import Counter
from datetime import date, timedelta

D = date.fromisoformat
RUN_DATE = D("2026-11-25")
TRANSCRIPTS = "/root/.claude/projects/*/*/subagents/agent-*.jsonl"
PREFIX = {
    "mcp__Helium_10__get_asin_bsr_history": "bsr",
    "mcp__Helium_10__get_asin_price_history": "price",
    "mcp__Helium_10__search_competitors_by_asin": "comp",
}


def load(fn):
    t = open(fn).read().strip()
    return json.loads(t[: t.rfind("}") + 1])


def extract(raw_dir, asins):
    os.makedirs(raw_dir, exist_ok=True)
    for src in glob.glob(TRANSCRIPTS):
        tools, res = {}, []
        for line in open(src):
            try:
                c = json.loads(line).get("message", {}).get("content")
            except Exception:
                continue
            if not isinstance(c, list):
                continue
            for b in c:
                if b.get("type") == "tool_use":
                    tools[b["id"]] = (b["name"], b.get("input", {}))
                elif b.get("type") == "tool_result":
                    res.append((b["tool_use_id"], b.get("content")))
        for tid, content in res:
            name, inp = tools.get(tid, (None, {}))
            if name not in PREFIX or inp.get("asin") not in asins:
                continue
            txt = content if isinstance(content, str) else "".join(
                x.get("text", "") for x in content or [] if isinstance(x, dict))
            fn = os.path.join(raw_dir, f"{PREFIX[name]}_{inp['asin']}.json")
            if os.path.exists(fn):
                continue
            t = txt.strip()
            try:
                obj = json.loads(t[: t.rfind("}") + 1])
            except Exception:
                continue  # saved-file notice; copy that file by hand
            if "data" in obj:
                json.dump(obj, open(fn, "w"))
                print("wrote", fn)


def expand(segs, key):
    out = {}
    last = max(D(s["end"]) for s in segs)
    for s in segs:
        a, b = D(s["start"]), D(s["end"])
        v = s.get(key)
        for d in [a] if a == b else [a + timedelta(i) for i in range((b - a).days)]:
            out[d] = v
    if last not in out:
        fin = [s for s in segs if D(s["end"]) == last]
        if fin and fin[-1].get(key) is not None:
            out[last] = fin[-1][key]
    return {d: v for d, v in out.items() if v is not None}


def med(xs):
    return st.median(xs) if xs else None


def rng(dct, a, b):
    return [v for d, v in dct.items() if a <= d <= b]


def metrics(raw_dir, heroes, brand):
    months = [((RUN_DATE.replace(day=1) - timedelta(days=1)).replace(day=1))]
    for _ in range(11):
        months.insert(0, (months[0] - timedelta(days=1)).replace(day=1))
    months = [(m.year, m.month) for m in months]
    rows = []
    for a, h in heroes.items():
        r = {"asin": a, "title": h.get("title", "")}
        b = load(os.path.join(raw_dir, f"bsr_{a}.json"))["data"]
        main = expand(b["segments"], "bsr")
        yr = timedelta(days=365)
        m26 = med(rng(main, RUN_DATE - timedelta(days=30), RUN_DATE))
        m25 = med(rng(main, RUN_DATE - yr - timedelta(days=30), RUN_DATE - yr))
        r["main_bsr_year_ago"], r["main_bsr_now"] = m25, m26
        r["yoy_rank_change"] = round(1 - m26 / m25, 4) if m25 and m26 else ""
        last14 = med(rng(main, RUN_DATE - timedelta(days=13), RUN_DATE))
        base = med(rng(main, RUN_DATE - timedelta(days=56), RUN_DATE - timedelta(days=43)))
        r["rank_improvement_8wk"] = round(1 - last14 / base, 4) if last14 and base else ""
        subs = b.get("subcategories") or []
        c100 = cm = 0
        if subs:
            prim = sorted(subs, key=lambda s: max(p["date"] for p in s["points"]))[-1]
            r["subcat_name"] = prim["name"]
            r["other_subcats"] = "|".join(s["name"] for s in subs if s is not prim)
            sp = {D(p["date"]): p["bsr"] for p in prim["points"]}
            r["best_subcat_bsr"] = min(v for d, v in sp.items() if d >= RUN_DATE - yr)
        else:
            sp = {}
        for y, m in months:
            ms = med([v for d, v in sp.items() if (d.year, d.month) == (y, m)])
            mm = med([v for d, v in main.items() if (d.year, d.month) == (y, m)])
            r[f"subcat_med_{y}-{m:02d}"], r[f"main_med_{y}-{m:02d}"] = ms, mm
            c100 += ms is not None and ms <= 100
            cm += mm is not None and mm <= 10000
        r["months_subcat_le_100"], r["months_main_le_10000"] = c100, cm
        pf = os.path.join(raw_dir, f"price_{a}.json")
        if os.path.exists(pf):
            pr = expand(load(pf)["data"]["segments"], "price")
            pm = med(list(pr.values()))
            deal = [d for d, v in pr.items() if v <= 0.9 * pm]
            r["median_price_rs"] = pm
            r["current_price_rs"] = pr.get(RUN_DATE, pr[max(pr)])
            r["deal_days_per_month"] = round(len(deal) / 12, 2)
            r["max_drop_pct"] = round(1 - min(pr.values()) / pm, 4)
            dd = [main[d] for d in deal if d in main]
            nd = [main[d] for d in pr if d not in deal and d in main]
            r["sale_event_rank_lift"] = round(med(nd) / med(dd), 3) if len(deal) >= 5 and dd else ""
        cf = os.path.join(raw_dir, f"comp_{a}.json")
        if os.path.exists(cf) and h.get("core") and r.get("current_price_rs"):
            comp = load(cf)["data"]["competitor_products"]
            hp = float(r["current_price_rs"])
            cc, strict = [], []
            for c in comp:
                br, t = (c.get("brand") or "").strip(), (c.get("title") or "").lower()
                own = [x.strip() for x in brand.split(",")]
                if any(x in br.lower().replace(" ", "") or x in t.replace(" ", "") for x in own) or c.get("price") is None:
                    continue
                if any(k in t for k in h["core"]) and 0.75 * hp <= c["price"] / 100 <= 1.25 * hp:
                    cc.append(br or "(none)")
                    if any(k in t for k in h.get("desc", [])):
                        strict.append(br or "(none)")
            r["comp_results_total"] = len(comp)
            r["copycats_count"], r["copycats_strict_count"] = len(cc), len(strict)
            r["copycat_top3_brands"] = "; ".join(f"{b} ({n})" for b, n in Counter(cc).most_common(3))
        rows.append(r)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", required=True, help="lower-case, no spaces; comma-separate sister brands; all excluded from copycats")
    ap.add_argument("--raw-dir", required=True)
    ap.add_argument("--heroes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--extract-from-transcripts", action="store_true")
    a = ap.parse_args()
    heroes = json.load(open(a.heroes))
    if a.extract_from_transcripts:
        extract(a.raw_dir, set(heroes))
    rows = metrics(a.raw_dir, heroes, a.brand)
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    for k in ["yoy_rank_change", "rank_improvement_8wk", "months_subcat_le_100", "months_main_le_10000",
              "deal_days_per_month", "sale_event_rank_lift", "copycats_count", "copycats_strict_count"]:
        v = [r[k] for r in rows if r.get(k, "") != ""]
        if v:
            print(f"{k}: mean {sum(v)/len(v):.3f} median {st.median(v):.3f} n {len(v)}")


if __name__ == "__main__":
    main()

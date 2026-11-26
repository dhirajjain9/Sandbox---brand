# Sandbox---brand
Sandbox is the model which will help us critically evaluate brands

## Dashboard

A static, self-contained dashboard (`outputs/dashboard/index.html`) shows every screened brand, its six checks,
its category markets, and side-by-side comparisons. Views use URL hashes, e.g. `#/brand/cadlec`,
`#/category/kitchen-appliances`, `#/compare/cadlec,milton`.

To add a brand:

1. Score it as usual (`runs/<run>/screen_scoring_*.csv`).
2. Add its peer sources to `SOURCES` in `pipeline/category_market.py`, then run `python -m pipeline.category_market`.
3. Add an entry to `pipeline/brands.json` (key, name, group, category, run, asof, channels, report, why, match).
4. Run `python -m pipeline.build_dashboard` and push. If the Vercel project points at `outputs/dashboard`, it redeploys automatically.

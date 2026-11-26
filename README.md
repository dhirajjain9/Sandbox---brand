# Sandbox---brand
Sandbox is the model which will help us critically evaluate brands

## Dashboard

A static, self-contained dashboard (`outputs/dashboard/index.html`) shows every screened brand, its six checks,
its category markets, and side-by-side comparisons. Views use URL hashes, e.g. `#/brand/cadlec`,
`#/category/kitchen-appliances`, `#/compare/cadlec,milton`.

### Adding a brand (`pipeline/new_brand.py`)

1. **Register it.** `python -m pipeline.new_brand add --name "TEKAVO" --group "Home & office furniture" --category "Computer tables and office furniture"`
   creates `runs/<date>_<key>/` (blank scoring sheet, checklist) and adds the brand to `pipeline/brands.json` as *in screening*.
   It appears on the dashboard straight away with a 6-step progress bar.
2. **Brand houses.** For sister brands screened as one: `python -m pipeline.new_brand subbrand --key tekavo --name FFO --amazon-brand "FFO FURNITURE FACTORY OUTLET"`.
3. **Brand pull and heroes.** Save the Helium 10 brand pull(s) to `data/raw/helium10/<key>/`, then
   `python -m pipeline.new_brand heroes --key <key> --pull data/raw/helium10/<key>/brand_pull_*.json`.
   This writes the listing file, picks the 10 hero families, records each sub-brand's share, and writes both Claude in Chrome
   run sheets (Keepa and Step B) with the heroes and main sub-categories filled in.
4. **Data steps.** Competition, hero history (`pipeline.h10_history_metrics`), Keepa run, Chrome run. Tick each with
   `python -m pipeline.new_brand stage --key <key> --done competition history ...`.
5. **Score.** Fill inputs with `python -m pipeline.rescore runs/<run> id=value ...`; add peer sources to `pipeline/category_market.py`;
   then `stage --done scored` turns it into a full FIT / NO FIT brand.
6. **Publish.** `python -m pipeline.build_dashboard` and push; Vercel redeploys automatically.

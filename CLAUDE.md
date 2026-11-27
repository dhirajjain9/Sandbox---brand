# Notes for Claude

## Quick-commerce sales by brand (ready to use)

`runs/_qcom/qcom_brand_sales.csv`: every brand in our GobbleCube exports, by platform (Blinkit, Zepto,
Instamart), category and month. 1,669 brands, Jul-Oct 2026 for all three platforms, plus Blinkit Home Decor
top-5 brands back to Aug 2025. Sales = Est. Category Share x category size (Rs lakh, at MRP and at selling
price); months without a category size keep the share and leave sales blank.

- Look up a brand: `python -m pipeline.qcom_brand_sales brand <name> [--by category]`
- Rebuild after adding a GobbleCube export to `data/raw/gobblecube/`: `python -m pipeline.qcom_brand_sales build`
  (see the module docstring for sources and how to add one)
- Use this before asking the user for a GobbleCube run. A brand absent from it is not listed in the
  exported home and kitchen categories; say that, not "no data".
- Brand names are as GobbleCube shows them ("Milton" there mixes Hydro Valves and the original Milton).

## Amazon 30-day sales for the quick-commerce brands

`runs/_qcom/amazon_brand_sales_30d.csv` (brand totals) and `runs/_qcom/qcom_amazon_by_category.csv`
(quick-commerce category x brand, Sep/Oct 2026, with Amazon alongside); shown on the dashboard's Quick
commerce page (`outputs/dashboard/qcom.json`). Helium 10 pull of 26 Nov 2026: 580 brands queried (96% of
quick-commerce sales); 1,189 small brands have amazon_status "not queried". To extend: run search_products
batches with context starting "Amazon 30-day sales for quick-commerce brands", then
`python -m pipeline.amazon_brand_sales extract` and `build`, then rebuild the dashboard. Splitting capped
batches is expensive (about one call per brand); budget Helium 10 calls (1,000 a month).

## TARGET: master extraction list (set by the user, 26 Nov 2026)

`runs/_target/master_list.csv`: **1,317 brands** (after wave 1 Part B listed-company and licence additions and 27 no-product-fit electronics/gaming brands) = Master File brands excluding "Skipped" and
"Skipped (Established)" (336) + quick-commerce brands not in the Master File (1,233), minus 215 exclusions
(established per workbook or well-known, listed-company owned, roll-up owned: Mensa, GlobalBees, Upscalio, GOAT;
lists in `pipeline/target_exclusions.py`; excluded rows kept in master_list_with_exclusions.csv).
This is the list data extraction must cover. Rebuild after each pull: `python -m pipeline.target_list <workbook.xlsx>`.
Coverage at setting: Amazon full pull 290 (239 found, 51 none selling), 1,064 not yet; quick commerce 1,060.
Extraction runs in category waves (`runs/_target/master_list_waves.csv`, groups in `pipeline/category_groups.py`):
wave 1 Appliances + Kitchen & Dining + Kitchen Storage (250 brands), wave 2 Home Furnishing + Decor & Gifting +
Lighting (292), wave 3 Cleaning, Pooja, Storage, Home Improvement, Bath (308), wave 4 the rest (214). Each wave =
Black Box sub-category exports (category view) + brand batches (`runs/_target/waves/`).
Status 27 Nov: WAVE 1 COMPLETE. Brand pulls: 214 found, 115 no match. Categories: 39 sub-categories on the dashboard
(Appliances 20, Kitchen & Dining 14, Kitchen Storage & Bottles 5; Egg Boilers had nothing to export). Sales floors differ
and are labelled per sub-category: 5 (most), 20 (Bakeware, Mugs, Glasses, Bottles, Flasks, Lunch Boxes, Spice), 50 (Kitchen
Tools, Storage Containers). Kitchen Tools excludes products already in Knives, Choppers, Bakeware, Serveware, Cutlery; Glasses excludes Mugs and Flasks products; Cutlery = cutlery
sub-categories only. Next: wave 2 (run sheet: brand batches first, one search per category at min 20).
Roles: we do data and diligence; outreach decisions belong to the outreach team.

## Sourcing universe (the team's brand list)

`runs/_sourcing/universe.csv`, from the team's CH dashboard workbook (`data/raw/sourcing/`, gitignored):
1,562 brands above Rs 1 Cr ARR with status, outreach status and owner, joined to our full Amazon pull,
our quick-commerce figures and screen verdicts. Rebuild: `python -m pipeline.sourcing <workbook.xlsx>`,
then `python -m pipeline.build_dashboard` (dashboard Sourcing page). Target = "Part of existing list" + "New" (742).
The workbook's Amazon comes from bestseller lists and misses long tails (full pull median 9.6x); our figures and
its quick commerce both cover the festive Sep-Oct/Nov period.

## Other conventions

- Brand verdict is FIT / NO FIT (never "pass"); checks are Met / Not met; the two must-clear checks are Gates; bar 60.
- Do not change the scoring method without asking the user first.
- Brand registry: `pipeline/brands.json`; dashboard: `python -m pipeline.build_dashboard` (Vercel redeploys on push).
- Customer Quality inputs 9b-9d are category-relative: `python -m pipeline.customer_quality runs/<run>`.

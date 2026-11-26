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

## Other conventions

- Brand verdict is FIT / NO FIT (never "pass"); checks are Met / Not met; the two must-clear checks are Gates; bar 60.
- Do not change the scoring method without asking the user first.
- Brand registry: `pipeline/brands.json`; dashboard: `python -m pipeline.build_dashboard` (Vercel redeploys on push).
- Customer Quality inputs 9b-9d are category-relative: `python -m pipeline.customer_quality runs/<run>`.

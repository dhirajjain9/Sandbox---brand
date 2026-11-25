# Claude in Chrome run sheet: Keepa data for Milton Home Appliances

Copy everything below the line into Claude in Chrome, with Keepa open and signed in.

---

You are collecting Amazon India data from Keepa for a brand evaluation. Keepa is open and signed
in in this browser. Work read-only: do not change account, subscription or notification
settings, do not buy tokens or upgrades, and do not delete saved searches or tracked products.
If something needs a login, payment or a plan upgrade, stop and tell me.

## The brand

- **Brand:** Milton Home Appliances. On Amazon the brand field reads **"Milton"** or
  **"MILTON"**; the seller is **HYDRO VALVES.** (seller ID A1GWROAAOIF0LC).
- **Do not mix up** with Milton housewares (bottles, flasks, lunch boxes: a different company,
  Hamilton Housewares) or with **Hamilton Beach**. Only kitchen and home **appliances** count.
- **Marketplace / locale:** **Amazon India (.in)** for every step. Check the locale selector
  before each search and export.

## File names

Save every export as XLSX or CSV (whatever Keepa gives) with these names, and tell me the names
at the end:

- Category pulls: `milton_keepa_<subcategory>_2026-11-25.xlsx`
- Brand pull: `milton_keepa_brand_2026-11-25.xlsx`

## Part A: Product Finder by sub-category, no brand filter (about 30 minutes)

Tool: **Keepa > Data > Product Finder**. For each sub-category below, run one search:

- Locale: **.in**
- Category: **Home & Kitchen**, then the sub-category named below (use Keepa's category picker;
  tell me the exact category path used)
- **No brand, seller or manufacturer filter**
- Sort by **Sales Rank: Current, ascending** (best sellers first)
- Result limit: the **top 500** (or the most your plan allows)
- Export: **all columns** (Keepa's export / download button, "all columns" option)

| # | Sub-category | Notes |
|---|---|---|
| 1 | Electric Kettles | |
| 2 | Sandwich Makers | Include sandwich grillers / toasters if Keepa groups them together |
| 3 | Gas Stoves | Gas stoves / gas hobs, not induction |
| 4 | Egg Boilers | If there is no separate node, use the nearest "Egg Cookers" / "Small Kitchen Appliances" node |
| 5 | Rice Cookers (Rice & Pasta Cookers) | |
| 6 | Air Fryers | |

After each export, check the file and note: row count, whether "Brand", "List Price: Current",
"Buy Box: Current" and "Monthly Sales Trends: Bought in past month" columns are present, and how
many rows have brand Milton / MILTON.

Do not combine several sub-categories into one search: one search per sub-category.

## Part B: refresh the Milton brand pull (about 5 minutes)

Same tool, same locale:

- **Brand** field: type "Milton" and pick the matching option(s) from the dropdown (there may be
  both "Milton" and "MILTON"; include both).
- Category: **Home & Kitchen** (to leave out bottles and other housewares as far as possible)
- No other filters; sort by Sales Rank: Current, ascending
- Export all columns

Then tell me how many rows list the Buy Box seller or manufacturer as HYDRO VALVES, and how many
look like housewares (bottles, flasks, lunch boxes, casseroles) that should be excluded.

## Rules

- .in locale for everything. If an export shows amazon.com URLs or US-dollar prices, discard it
  and redo the step.
- Export the full file; do not filter, sort or edit it after download.
- Do not guess numbers. If a step fails or a column is missing, say so.
- If Keepa limits exports by tokens or plan, do the sub-categories in the table's order and stop
  when the limit is reached; tell me which were done.
- Stop after about 45 minutes of work, or earlier when done.

## What to give me at the end

1. A table of every file: file name, sub-category and exact Keepa category path, filters used,
   sort, row count, number of Milton rows.
2. Which of these columns each file has: Brand, List Price: Current, Buy Box: Current,
   Buy Box: 90 days avg., Monthly Sales Trends: Bought in past month, Reviews: Rating,
   Reviews: Rating Count, New Offer Count: Current, Listed since, Parent ASIN.
3. For the brand pull: rows with HYDRO VALVES as Buy Box seller, and rows that look like
   housewares.
4. Anything that went wrong: wrong locale, token or plan limits, missing columns, steps skipped.

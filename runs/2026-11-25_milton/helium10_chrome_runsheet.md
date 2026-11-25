# Claude in Chrome run sheet: Helium 10 data for Milton Home Appliances

Copy everything below the line into Claude in Chrome, with Helium 10 open and signed in.

---

You are collecting Amazon India data from Helium 10 for a brand evaluation. Helium 10 is open
and signed in in this browser. Work read-only: do not change account, billing, team or
alert settings, do not buy or start paid add-ons, and do not delete anything (saved
searches, tracked products). If something needs a login, approval, payment or a plan
upgrade, stop and tell me.

## The brand

- **Brand:** Milton Home Appliances (seller name on Amazon: **HYDRO VALVES.**, seller ID
  A1GWROAAOIF0LC). On Amazon the brand field reads **"Milton"** or **"MILTON"**.
- **Do not mix up** with Milton housewares (bottles, flasks, lunch boxes: a different company,
  Hamilton Housewares) or with **Hamilton Beach**. Only kitchen and home **appliances** count.
- **Marketplace:** **Amazon India (amazon.in)** for every step. Helium 10 sometimes defaults to
  amazon.com: check the marketplace selector before each search and export.

## File names

Save every export as CSV with these names (rename after download if needed), and tell me the
names at the end:

- Black Box: `milton_bb_<subcategory>_2026-11-25.csv` (e.g. `milton_bb_electric_kettles_2026-11-25.csv`)
- Cerebro multi-ASIN: `milton_cerebro_multi_2026-11-25.csv`
- Cerebro single-ASIN: `milton_cerebro_<ASIN>_2026-11-25.csv`

## Part A: Black Box, one export per sub-category (about 30 minutes)

Tool: **Helium 10 > Black Box > Products**. For each sub-category below, run one search:

- Marketplace: amazon.in
- Category: **Home & Kitchen**, then the sub-category named below (pick the closest match
  Helium 10 offers and tell me the exact name used)
- **No brand filter**, no seller filter, no price filter
- Minimum monthly ASIN sales: the value in the table
- Run the search, then **Export > CSV** (all columns)

| # | Sub-category | Min. monthly ASIN sales | Notes |
|---|---|---|---|
| 1 | Electric Kettles | 50 | Crowded; if results still hit the 200-row limit, try 100 |
| 2 | Sandwich Makers | 20 | Include grillers if Helium 10 groups them here |
| 3 | Gas Stoves | 10 | Gas stoves / cooktops (not induction) |
| 4 | Egg Boilers (Small Kitchen Appliances) | 20 | If there is no "Egg Boilers" level, use "Small Kitchen Appliances" |
| 5 | Rice & Pasta Cookers | 10 | Includes multi-cook kettles |
| 6 | Air Fryers | 20 | |

**The 200-row limit.** Black Box exports at most 200 rows. After each export, note the row count
and the smallest "ASIN Sales" value in the file.

- Fewer than 200 rows: fine, the sub-category is complete down to the minimum.
- Exactly 200 rows: the list is cut off. Raise the minimum (e.g. 50 to 100), export again, and
  keep both files, noting which minimum each used.

Do not run one search across several sub-categories at once: a combined search came back uneven
and missed whole sub-categories last time.

## Part B: choose the peer ASINs for Cerebro

From the Part A files, find the **best-selling ASIN that is not Milton** in each of these four
sub-categories (highest "ASIN Sales"; skip any listing whose brand is Milton or MILTON):

1. Electric Kettles
2. Sandwich Makers
3. Gas Stoves
4. Egg Boilers / Small Kitchen Appliances

Write down for each: ASIN, brand, title (first 60 characters), ASIN Sales. If you cannot read the
CSV files, use the Black Box results table on screen, sorted by ASIN Sales.

## Part C: Cerebro, one multi-ASIN run (about 10 minutes)

Tool: **Helium 10 > Cerebro**. Marketplace amazon.in.

Enter these 6 Milton ASINs first, **in this order**, then the 4 peer ASINs from Part B (10 in
total):

```
B0F54GKQ38, B0DF6D49G7, B08TTRVWKY, B0D3XVTRRY, B0845ZQN9T, B0G6L7GKN1
```

| ASIN | Product |
|---|---|
| B0F54GKQ38 | Milton Rapid electric kettle 1.8L |
| B0DF6D49G7 | Milton Royal Express sandwich maker |
| B08TTRVWKY | Milton Smart egg boiler |
| B0D3XVTRRY | Milton Champ multi-cook kettle |
| B0845ZQN9T | Milton Premium 3-burner gas stove |
| B0G6L7GKN1 | Milton Glass air fryer oven |

Run **Get Keywords** with no filters, then **Export > CSV** with all keywords. The export should
have one column of organic rank per ASIN. Check the file has the 10 ASIN columns.

## Part D: Cerebro, single-ASIN runs (about 15 minutes)

A multi-ASIN export only shows sponsored rank for the first ASIN, so each ASIN also needs its own
run. For **each of the 10 ASINs** from Part C, separately:

- Cerebro, amazon.in, enter that **one** ASIN only
- Get Keywords, no filters
- Export > CSV (all keywords). The file should include "Organic Rank" and "Sponsored Rank"
  columns.

That is 10 files. Check that each file's name matches the ASIN that was actually searched.

## Rules

- amazon.in for everything. If any export shows amazon.com URLs or US-dollar prices, discard it
  and redo the step.
- Export the full CSV; do not filter, sort or edit the files after download.
- Do not guess numbers. If a step fails or a column is missing, say so.
- Stop after about 75 minutes of work, or earlier when done.

## What to give me at the end

1. A table of every file: file name, tool, sub-category or ASIN, filters used (minimum sales),
   row count, smallest ASIN Sales value (Black Box files).
2. The exact sub-category names Helium 10 used for each Part A search.
3. The four peer ASINs chosen in Part B, with brand, title and ASIN Sales.
4. Anything that went wrong: wrong marketplace, plan limits, missing columns, steps skipped.

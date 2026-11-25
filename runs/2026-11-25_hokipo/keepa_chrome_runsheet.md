# Claude in Chrome run sheet: Keepa peer data for HOKIPO

Copy everything below the line into Claude in Chrome, with Keepa open and signed in.

---

You are collecting Amazon India data from Keepa for a brand evaluation. Keepa is open and signed
in in this browser. Work read-only: do not change account, subscription or notification
settings, do not buy tokens or upgrades, and do not delete saved searches or tracked products.
If something needs a login, payment or a plan upgrade, stop and tell me.

## What this is for

The brand being evaluated is **HOKIPO** (home furnishing: sofa covers, armrest covers, chair
covers, storage boxes, doormats). HOKIPO's own listings are already collected. This run collects
**the competitors in the same sub-categories**, so we can compare list prices and discounts.

## Settings for every search

- Tool: **Keepa > Data > Product Finder**
- Locale: **.in** (check it before each search)
- **No brand, seller or manufacturer filter** (HOKIPO will appear in the results; that is fine)
- Sort by **Sales Rank: Current, ascending** (best sellers first)
- Rows: the **top 500**
- Columns: turn on all columns ("Show all") before exporting, so the file includes at least:
  Brand, List Price: Current, Buy Box: Current, Buy Box: 90 days avg., Buy Box: Buy Box Seller,
  Monthly Sales Trends: Bought in past month, Reviews: Rating, Reviews: Rating Count,
  New Offer Count: Current, Buy Box: 90 days OOS, Listed since, Parent ASIN, Categories: Sub
- Export the page (Keepa exports only the page on screen, so keep 500 rows on one page)

## The searches, in priority order

Use Keepa's category picker. All are under **Home & Kitchen**. Tell me the exact category path
you used for each.

| # | Sub-category | Expected path | File name |
|---|---|---|---|
| 1 | **Sofa Slipcovers** | Home & Kitchen > Home Furnishing > Slipcovers > Sofa Slipcovers | `hokipo_peers_sofa-slipcovers_2026-11-25.xlsx` |
| 2 | **Armrest Covers** | Home & Kitchen > Home Furnishing > Slipcovers > Armrest Covers (or nearest) | `hokipo_peers_armrest-covers_2026-11-25.xlsx` |
| 3 | **Dining Chair Slipcovers** | Home & Kitchen > Home Furnishing > Slipcovers > Dining Chair Slipcovers | `hokipo_peers_dining-chair-slipcovers_2026-11-25.xlsx` |
| 4 | **Storage Boxes** | Home & Kitchen > Storage & Organisation > ... > Storage Boxes (nearest node) | `hokipo_peers_storage-boxes_2026-11-25.xlsx` |
| 5 | **Doormats** | Home & Kitchen > Home Furnishing > ... > Doormats (nearest node) | `hokipo_peers_doormats_2026-11-25.xlsx` |

If the quota runs low, stop after Sofa Slipcovers and Armrest Covers: those two matter most.

## Rules

- Keep one search per sub-category; do not combine sub-categories.
- .in locale only. If an export shows amazon.com links or US-dollar prices, discard it and redo.
- If some rows fail to load (blank rows), reload before exporting.
- Export the full file; do not filter, sort or edit it after download.
- Do not guess numbers. If a step fails or a column is missing, say so.
- Stop after about 30 minutes of work, or earlier when done.
- Afterwards you may set the results table back to its usual columns and page size; these are
  display settings only.

## What to give me at the end

1. A table of every file: file name, sub-category, exact Keepa category path, rows, number of
   HOKIPO rows in it.
2. Confirmation that List Price: Current and Buy Box: Current are present in each file.
3. Anything that went wrong: locale, token limits, blank rows, missing columns, steps skipped.
4. Keepa token or quota used.

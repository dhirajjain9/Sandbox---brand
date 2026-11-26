# Claude in Chrome run sheet: Keepa data for {name}

Copy everything below the line into Claude in Chrome, with Keepa open and signed in.

---

You are collecting Amazon India data from Keepa for a brand evaluation. Keepa is open and signed
in in this browser. Work read-only: do not change account, subscription or notification
settings, do not buy tokens or upgrades, and do not delete saved searches or tracked products.
If something needs a login, payment or a plan upgrade, stop and tell me.

## The brand

**{name}**: {category}. {brand_line}{seller_line}. Locale **.in** for every step.

## Settings for every search

- Tool: **Keepa > Data > Product Finder**, locale **.in** (check it before each search)
- Sort by **Sales Rank: Current, ascending**; rows: the **top 500** on one page
- Columns: "Show all" before exporting, so the file has at least: Brand, List Price: Current,
  Buy Box: Current, Buy Box: 90 days avg., Buy Box: Buy Box Seller, Monthly Sales Trends: Bought
  in past month, Reviews: Rating, Reviews: Rating Count, New Offer Count: Current, Buy Box: 90
  days OOS, Listed since, Parent ASIN, Categories: Sub
- Export the page; do not filter, sort or edit the file afterwards

## Part A: {name} brand pull (5 minutes)

{brand_pull_steps}
- Tell me each file's row count and how many rows list a Buy Box seller other than the sellers
  named above.

## Part B: peers by sub-category, no brand filter (about 25 minutes)

Use Keepa's category picker. Tell me the exact category path used.

{subcat_table}

If the quota runs low, stop after the first three.

## What to give me at the end

1. A table of every file: name, sub-category, exact Keepa category path, rows, and rows for each of: {brand_names}.
2. Confirmation that List Price: Current and Buy Box: Current are in each file.
3. Anything that went wrong: locale, token limits, blank rows, missing columns, steps skipped.

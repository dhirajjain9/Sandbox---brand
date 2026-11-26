# Claude in Chrome run sheet: Keepa data for Desidiya

Copy everything below the line into Claude in Chrome, with Keepa open and signed in.

---

You are collecting Amazon India data from Keepa for a brand evaluation. Keepa is open and signed
in in this browser. Work read-only: do not change account, subscription or notification
settings, do not buy tokens or upgrades, and do not delete saved searches or tracked products.
If something needs a login, payment or a plan upgrade, stop and tell me.

## The brand

**Desidiya**: Decorative lights, diyas and festive home decor. Amazon sellers: **ETrade Online** (56% of revenue), **ELAAR Store** (44% of revenue). Locale **.in** for every step.

## Settings for every search

- Tool: **Keepa > Data > Product Finder**, locale **.in** (check it before each search)
- Sort by **Sales Rank: Current, ascending**; rows: the **top 500** on one page
- Columns: "Show all" before exporting, so the file has at least: Brand, List Price: Current,
  Buy Box: Current, Buy Box: 90 days avg., Buy Box: Buy Box Seller, Monthly Sales Trends: Bought
  in past month, Reviews: Rating, Reviews: Rating Count, New Offer Count: Current, Buy Box: 90
  days OOS, Listed since, Parent ASIN, Categories: Sub
- Export the page; do not filter, sort or edit the file afterwards

## Part A: Desidiya brand pull (5 minutes)

- **Brand** field: type "Desidiya" and pick every matching option (any spelling or case). No
  other filters.
- File: `desidiya_keepa_brand_2026-11-26.xlsx`.
- Tell me each file's row count and how many rows list a Buy Box seller other than the sellers
  named above.

## Part B: peers by sub-category, no brand filter (about 25 minutes)

Use Keepa's category picker. Tell me the exact category path used.

| # | Sub-category | File name |
|---|---|---|
| 1 | LED Strips | `desidiya_peers_ledstrips_2026-11-26.xlsx` |
| 2 | Home & Décor | `desidiya_peers_homedécor_2026-11-26.xlsx` |
| 3 | Specialty Lighting | `desidiya_peers_specialtylighting_2026-11-26.xlsx` |
| 4 | Clip Photo Holders | `desidiya_peers_clipphotoholders_2026-11-26.xlsx` |

If the quota runs low, stop after the first three.

## What to give me at the end

1. A table of every file: name, sub-category, exact Keepa category path, rows, and rows for each of: Desidiya.
2. Confirmation that List Price: Current and Buy Box: Current are in each file.
3. Anything that went wrong: locale, token limits, blank rows, missing columns, steps skipped.

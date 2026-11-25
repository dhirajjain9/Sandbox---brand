# Claude in Chrome run sheet: Keepa data for CADLEC

Copy everything below the line into Claude in Chrome, with Keepa open and signed in.

---

You are collecting Amazon India data from Keepa for a brand evaluation. Keepa is open and signed
in in this browser. Work read-only: do not change account, subscription or notification
settings, do not buy tokens or upgrades, and do not delete saved searches or tracked products.
If something needs a login, payment or a plan upgrade, stop and tell me.

## The brand

**CADLEC**: small kitchen and home appliances (OTGs, mixer grinders, induction and infrared
cooktops, ceiling fans, kitchen chimneys, immersion rods, kettles). Most listings are sold by
**RetailEZ Pvt Ltd**; the chimneys by **Dawntech Electronics**. Locale **.in** for every step.

## Settings for every search

- Tool: **Keepa > Data > Product Finder**, locale **.in** (check it before each search)
- Sort by **Sales Rank: Current, ascending**; rows: the **top 500** on one page
- Columns: "Show all" before exporting, so the file has at least: Brand, List Price: Current,
  Buy Box: Current, Buy Box: 90 days avg., Buy Box: Buy Box Seller, Monthly Sales Trends: Bought
  in past month, Reviews: Rating, Reviews: Rating Count, New Offer Count: Current, Buy Box: 90
  days OOS, Listed since, Parent ASIN, Categories: Sub
- Export the page; do not filter, sort or edit the file afterwards

## Part A: CADLEC brand pull (5 minutes)

- **Brand** field: type "CADLEC" and pick every matching option (there may be "CADLEC" and
  "Cadlec"). No other filters.
- File: `cadlec_keepa_brand_2026-11-25.xlsx`. Tell me the row count and how many rows list a Buy
  Box seller other than RetailEZ or Dawntech.

## Part B: peers by sub-category, no brand filter (about 25 minutes)

Use Keepa's category picker under **Home & Kitchen**. Tell me the exact category path used.

| # | Sub-category | File name |
|---|---|---|
| 1 | Oven Toaster Grills (OTG) | `cadlec_peers_otg_2026-11-25.xlsx` |
| 2 | Mixer Grinders | `cadlec_peers_mixer-grinders_2026-11-25.xlsx` |
| 3 | Induction Cooktops | `cadlec_peers_induction_2026-11-25.xlsx` |
| 4 | Ceiling Fans | `cadlec_peers_ceiling-fans_2026-11-25.xlsx` |
| 5 | Kitchen chimneys (Wall-Mount Hoods / Range Hoods) | `cadlec_peers_chimneys_2026-11-25.xlsx` |

If the quota runs low, stop after the first three.

## What to give me at the end

1. A table of every file: name, sub-category, exact Keepa category path, rows, CADLEC rows.
2. Confirmation that List Price: Current and Buy Box: Current are in each file.
3. Anything that went wrong: locale, token limits, blank rows, missing columns, steps skipped.

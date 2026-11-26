# Claude in Chrome run sheet: Keepa data for TEKAVO

Copy everything below the line into Claude in Chrome, with Keepa open and signed in.

---

You are collecting Amazon India data from Keepa for a brand evaluation. Keepa is open and signed
in in this browser. Work read-only: do not change account, subscription or notification
settings, do not buy tokens or upgrades, and do not delete saved searches or tracked products.
If something needs a login, payment or a plan upgrade, stop and tell me.

## The brand

**TEKAVO**: Computer tables, office desks and storage furniture. A brand house screened as one: **TEKAVO** (Amazon brand "TEKAVO"), **FFO** (Amazon brand "FFO FURNITURE FACTORY OUTLET"), **Deskio** (Amazon brand "Deskio"). Amazon sellers: **EVERS** (73% of revenue), **Furniture Factory Outlet** (27% of revenue). Locale **.in** for every step.

## Settings for every search

- Tool: **Keepa > Data > Product Finder**, locale **.in** (check it before each search)
- Sort by **Sales Rank: Current, ascending**; rows: the **top 500** on one page
- Columns: "Show all" before exporting, so the file has at least: Brand, List Price: Current,
  Buy Box: Current, Buy Box: 90 days avg., Buy Box: Buy Box Seller, Monthly Sales Trends: Bought
  in past month, Reviews: Rating, Reviews: Rating Count, New Offer Count: Current, Buy Box: 90
  days OOS, Listed since, Parent ASIN, Categories: Sub
- Export the page; do not filter, sort or edit the file afterwards

## Part A: brand pulls for TEKAVO, FFO and Deskio (10 minutes)

- Run one search per brand, each with the **Brand** field set to that brand (pick every matching
  spelling) and no other filters, and export each:
  - **TEKAVO** → `tekavo_keepa_brand_tekavo_2026-11-26.xlsx`
  - **FFO FURNITURE FACTORY OUTLET** → `tekavo_keepa_brand_ffo_2026-11-26.xlsx`
  - **Deskio** → `tekavo_keepa_brand_deskio_2026-11-26.xlsx`
- Tell me each file's row count and how many rows list a Buy Box seller other than EVERS or
  Furniture Factory Outlet.

## Part B: peers by sub-category, no brand filter (about 25 minutes)

Use Keepa's category picker. Tell me the exact category path used.

| # | Sub-category | What the group sells there | File name |
|---|---|---|---|
| 1 | **Desks** (Home & Kitchen › Furniture › Home Office Furniture › Desks) | Computer, L-shaped and gaming tables (72% of group sales) | `tekavo_peers_desks_2026-11-26.xlsx` |
| 2 | **Computer Workstations** | Multi-person workstations | `tekavo_peers_computerworkstations_2026-11-26.xlsx` |
| 3 | **Bedside Tables** | FFO bedside tables | `tekavo_peers_bedsidetables_2026-11-26.xlsx` |
| 4 | **Bathroom Shelves** (where FFO's washing-machine racks sit) | FFO washing-machine racks | `tekavo_peers_bathroomshelves_2026-11-26.xlsx` |

If the quota runs low, stop after Desks and Computer Workstations: those matter most.

## What to give me at the end

1. A table of every file: name, sub-category, exact Keepa category path, rows, and rows for each of: TEKAVO, FFO, Deskio.
2. Confirmation that List Price: Current and Buy Box: Current are in each file.
3. Anything that went wrong: locale, token limits, blank rows, missing columns, steps skipped.

# Claude in Chrome run sheet, wave 2: Home Furnishing, Home Decor & Gifting, Lighting & Electricals

Copy everything below the line into Claude in Chrome with Helium 10 open and signed in, and give it
`wave2_brand_batches.tsv` (same folder) when it asks. Do Part B (brand batches) FIRST, then Part A. Part B fills in the full Amazon sales of 271
target brands; Part A builds the category view. Expect 3-4 hours; it can run across sittings (say where to resume).

## Extra: wave 1 spelling retry (3 searches), paste into Chrome at any break

Give Claude in Chrome `spelling_retry_batches.tsv` (same folder) with this:

> Before continuing, run these 3 extra brand searches in Black Box Products: marketplace Amazon India,
> Exact Brand Search = the brands in each row of spelling_retry_batches.tsv (comma-separated), ASIN Sales
> min 1, no category or price. Export each as `w1_retry_<batch>.csv`. Tell me rows per file and which
> brand names matched nothing. For R2 say which Modern Quests spelling matched. For R3 also note the main
> seller name and what the products are, so we can confirm they are our brands. Then resume where you were.

---

You are collecting Amazon India data from Helium 10 Black Box, open and signed in in this browser.
Work read-only: do not change account, billing or alert settings, do not save or delete lists, do not buy
anything. If something needs a login, payment or upgrade, stop and tell me. Work at a normal human pace;
if Helium 10 shows a rate or usage limit, stop and tell me how far you got.

Every search: Black Box > Products, marketplace **Amazon India (.in)** (check it each time), all columns
selected, export as CSV. If the browser cannot rename files, note each downloaded file name against its row.

## Part A: category market exports (about 1 hour)

One search per sub-category below. Filters: **Category = Home & Kitchen**, then the sub-category (use
Black Box's category picker; if the exact name differs, pick the closest and tell me what you used);
**Monthly Sales (ASIN level) at least 20**; no brand, price or other filters. Sort by **ASIN Revenue,
highest first**, export the top 500 in ONE search per sub-category (no price splits, to save Black Box
searches); note in the log whether it hit 500. File name: `w2_cat_<sub-category>.csv`.

Home Furnishing: Bedsheets · Comforters & Quilts · Blankets & Dohars · Pillows · Cushion Covers · Curtains · Sofa Covers · Mattress Protectors · Bath Towels · Doormats · Carpets & Rugs · Table Linen

Home Decor & Gifting: Wall Decor · Showpieces & Figurines · Vases · Artificial Flowers · Candles · Clocks · Photo Frames · Decorative Trays & Bowls · Gift Hampers · Party Decorations

Lighting & Electricals: LED Strips · String & Fairy Lights · Decorative Lamps · Ceiling Lights · Wall Lamps · Table Lamps · LED Bulbs · Extension Boards · Night Lights

For each: tell me the exact category path, rows exported, and whether the result hit Black Box's row cap.

## Part B: brand exports (about 2-3 hours)

`wave2_brand_batches.tsv` lists 16 batches (some shortened after the no-product-fit exclusions) (`batch <tab> category group <tab> brand | brand | ...`).
For each batch: **Brand** = every brand in the batch (pick every matching spelling Black Box suggests;
case, spaces, "&", ® signs vary); **Monthly Sales (ASIN level) at least 1**; no category or other filters.
Export as `w2_brands_<batch>.csv`. If a batch hits the row cap, split it in half and export each half
(`..._a.csv`, `..._b.csv`); if one brand alone hits the cap, export it once and mark it "capped".

## What to give me at the end

1. Part A table: `sub-category, category path used, file, rows, capped`.
2. Part B table: `batch, file, rows, capped, brands with no match`.
3. Spellings that differ from our list (`our name -> Amazon brand name`), and brands that matched a
   different company (same name, unrelated products), so I can drop them.
4. The exact export column names, and anything that went wrong or was skipped.

Then upload the CSVs (a zip is fine).

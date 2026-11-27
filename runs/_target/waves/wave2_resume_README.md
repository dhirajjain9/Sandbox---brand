# Wave 2: resume instructions for Claude in Chrome (27 Nov 2026)

You are continuing the wave 2 Amazon India data collection in Helium 10 Black Box, open and signed in in
this browser. Work read-only: do not change account, billing or alert settings, do not save or delete
lists, do not buy anything. If something needs a login, payment or upgrade, stop and tell me. If Helium 10
shows a usage limit or repeated "Unknown server error", stop and tell me how far you got.

Every search: Black Box > Products, marketplace **Amazon India (.in)** (check it each time), export as CSV
("Export Data..." > "...as a CSV file"). Use element (ref) clicks, not screen coordinates; keep the
window full size. The results text reads "Viewing 1-100 of N items"; N = 500 means the result is capped.

## Already done (do not repeat)

Part B brand batches 2.1 to 2.16, including MPROW (67 exports).

## Step 1: brand batch 2.17 (last row of wave2_brand_batches.tsv)

Brands: Foam Home, Surya Living, Aurave Décor, Restofit, Decorum, Purav Lights, 1st Step, 3R, Airganic, AVS

Filters: **Exact Brand Search** = the 10 names (comma-separated), **ASIN Sales min 1**, no category, no
price. Export as `w2_brands_2.17.csv`. If it hits 500, split the batch in half. Tell me the rows and which
names matched nothing. "3R" and "AVS" are short names: note if they pull products from unrelated
companies (check the seller and product types).

## Step 2: Part A, category view (31 sub-categories, one search each)

- Home Furnishing: Bedsheets · Comforters & Quilts · Blankets & Dohars · Pillows · Cushion Covers ·
  Curtains · Sofa Covers · Mattress Protectors · Bath Towels · Doormats · Carpets & Rugs · Table Linen
- Home Decor & Gifting: Wall Decor · Showpieces & Figurines · Vases · Artificial Flowers · Candles ·
  Clocks · Photo Frames · Decorative Trays & Bowls · Gift Hampers · Party Decorations
- Lighting & Electricals: LED Strips · String & Fairy Lights · Decorative Lamps · Ceiling Lights ·
  Wall Lamps · Table Lamps · LED Bulbs · Extension Boards · Night Lights

For each sub-category:

- **Category** = Home & Kitchen > the sub-category (expand the tree with the arrow buttons; the picker's
  search box is unreliable). If the exact name differs, pick the closest node and tell me the path used.
- **ASIN Sales (units) min 20**. No brand, price or other filters. (The drawer's "Clear" button wipes the
  ASIN Sales minimum too; re-enter 20 after using it.)
- Sort by **ASIN Revenue, highest first**; export the top 500. Do NOT split by price band.
- File name: `w2_cat_<sub-category>.csv`.

Keep a log: `seq, sub-category, category path used, rows, capped (N = 500?)`.

## At the end

1. Log tables for Step 1 and Step 2 (as `partB_log.tsv` / `partA_log.tsv`) and short resume notes.
2. Upload the CSVs (a zip is fine).

# Claude in Chrome run sheet, wave 1: Appliances, Kitchen & Dining, Kitchen Storage & Bottles

Copy everything below the line into Claude in Chrome with Helium 10 open and signed in, and give it
`wave1_brand_batches.tsv` (same folder) when it asks. Part A builds the category view; Part B fills in the
full Amazon sales of 250 target brands. Expect 3-4 hours; it can run across sittings (say where to resume).

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
**Monthly Sales (ASIN level) at least 5**; no brand, price or other filters. Sort by **ASIN Revenue,
highest first**, show the maximum rows Black Box allows, export. File name: `w1_cat_<sub-category>.csv`.

Appliances: Mixer Grinders · Electric Kettles · Induction Cooktops · Air Fryers · Oven Toaster Grills ·
Sandwich Makers · Juicers · Hand Blenders · Rice Cookers · Coffee Makers · Toasters · Water Purifiers ·
Vacuum Cleaners · Irons · Room Heaters · Ceiling Fans · Table & Pedestal Fans · Air Purifiers ·
Water Heaters / Geysers · Kitchen Chimneys · Egg Boilers

Kitchen & Dining: Cookware Sets · Pressure Cookers · Kadhais & Woks · Tawas & Griddles · Gas Stoves ·
Dinner Sets · Serveware · Cutlery · Kitchen Knives · Choppers & Graters · Bakeware · Mugs · Glasses ·
Kitchen Tools & Utensils

Kitchen Storage & Bottles: Kitchen Storage Containers · Water Bottles · Flasks & Thermos · Lunch Boxes ·
Spice Racks & Organisers

For each: tell me the exact category path, rows exported, and whether the result hit Black Box's row cap.

## Part B: brand exports (about 2-3 hours)

`wave1_brand_batches.tsv` lists 14 batches (`batch <tab> category group <tab> brand | brand | ...`).
For each batch: **Brand** = every brand in the batch (pick every matching spelling Black Box suggests;
case, spaces, "&", ® signs vary); **Monthly Sales (ASIN level) at least 1**; no category or other filters.
Export as `w1_brands_<batch>.csv`. If a batch hits the row cap, split it in half and export each half
(`..._a.csv`, `..._b.csv`); if one brand alone hits the cap, export it once and mark it "capped".

## What to give me at the end

1. Part A table: `sub-category, category path used, file, rows, capped`.
2. Part B table: `batch, file, rows, capped, brands with no match`.
3. Spellings that differ from our list (`our name -> Amazon brand name`), and brands that matched a
   different company (same name, unrelated products), so I can drop them.
4. The exact export column names, and anything that went wrong or was skipped.

Then upload the CSVs (a zip is fine).

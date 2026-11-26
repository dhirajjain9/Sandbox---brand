# Claude in Chrome run sheet: full Amazon sales for 514 sourcing brands (Helium 10 Black Box)

Copy everything below the line into Claude in Chrome, with Helium 10 open and signed in. Attach or paste
`batches.tsv` (same folder) when it asks for the brand list. Expect 3-5 hours; it can be split across
sessions: say which batch to start from.

---

You are collecting Amazon India sales for a list of brands from Helium 10 Black Box, which is open and
signed in in this browser. Work read-only: do not change account, billing or alert settings, do not save
or delete lists, and do not buy anything. If something needs a login, payment or a plan upgrade, stop and
tell me. Work at a normal human pace (a few seconds between actions); if Helium 10 shows a rate-limit or
usage-limit message, stop and tell me how far you got.

## The brand list

I will give you `batches.tsv`: one line per batch, `batch number <tab> brand | brand | ...`. There are 70
batches and 514 brands. Brand names are as our team spells them; Amazon may spell them differently
(case, spaces, "&" vs "and", a ® sign). For each brand, pick every matching spelling Black Box suggests
in the Brand field. If a brand has no match at all, note it and move on.

## Settings for every search (Black Box > Products)

- Marketplace: **Amazon India (.in)**. Check it before every search.
- Filters: **Brand** = the batch's brands (all matching spellings); **Monthly Sales (child / ASIN level)
  at least 1**. No category, price or other filters.
- Columns: choose all available columns, and make sure the export includes at least: ASIN, Brand,
  Seller / Buy Box seller, Price, ASIN Revenue, ASIN Sales, Parent Level Revenue, Sales Year Over Year
  (%), Sales Trend (90 days), Reviews, Rating, Category, Listing Age, and **any 12-month or annual sales
  column** (it may be called "Last Year Sales", "12 Month Sales", "Year Sales" or similar). Tell me the
  exact names of any 12-month columns you find. If there are none, say so.
- Export the results as CSV, named `bb_batch_<batch number>.csv` (if the browser cannot rename, note
  the downloaded file name against the batch number).

## If a batch hits the result cap

Black Box caps how many rows a search returns. If a batch's result count equals the cap (or Black Box
says there are more results than shown), split the batch: run the first half of its brands, then the
second half, each as its own export (`bb_batch_<n>a.csv`, `bb_batch_<n>b.csv`). If a single brand still
hits the cap, export it once and note "capped" for that brand.

## What to give me at the end

1. A table: `batch, file name, rows, capped (yes/no), brands with no match`.
2. The exact column names in the export, especially any 12-month sales column.
3. Any spelling you picked that differs from our list (`our name -> Amazon brand name`).
4. Anything that went wrong: usage limits, missing columns, wrong marketplace, steps skipped, and the
   last batch completed.

Then upload the CSV files into this session (or zip them), and I will load them.

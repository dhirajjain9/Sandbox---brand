# Claude in Chrome prompt: Aura Decor SKU price history on Blinkit (GobbleCube)

Copy everything below the line into Claude in Chrome, with GobbleCube open and signed in.

---

Please collect monthly price history for specific SKUs from GobbleCube, which is open and signed
in. Work read-only: do not change any settings, alerts, team or billing, and do not share anything.
Stop and tell me if anything needs a login, approval or payment.

## Where to look

- Platform: **Blinkit**
- Path: **Digital Shelf > Category RCA > [category card] > Competition > SKUs**
- Categories: **Home Decor** and **Festive Gifting** (exact GobbleCube names). There are no
  sub-categories in GobbleCube; the category is the lowest level.
- Brand: **Auradecor** (one word). Not "Asian Aura", "AuraCam" or "Flower Aura".
- Months: every calendar month from **2025-08 to 2026-11** (Nov 2026 is partial, to the latest
  date available). Set the date range to one calendar month at a time.

## SKUs (Product ID | category | pack | name)

| # | Product ID | Category | Pack | Name |
|---|---|---|---|---|
| 1 | 477889 | Festive Gifting | 5 pcs | Ceramic Diffuser Gift Set (Lemongrass, Cream) |
| 2 | 477891 | Festive Gifting | 5 pcs | Ceramic Diffuser Gift Set (Jasmine, Brown) |
| 3 | 532001 | Festive Gifting | 1 set | Urli Gift Set with Floating Candles & Potpourri |
| 4 | 480510 | Home Decor | 10 pcs | Heart Shaped Tea Light Candles (Rose) |
| 5 | 494201 | Home Decor | 50 pcs | Tea Light Candles (Unscented) |
| 6 | 559041 | Home Decor | 6 pcs | Aroma Oil Set |
| 7 | 477886 | Home Decor | 6 pcs | Votive Pillar Candle (Raspberry) |
| 8 | 531999 | Home Decor | 2 pcs | Urli Soy Wax Candle Set (Vanilla, Oudh) |
| 9 | 531995 | Home Decor | 10 pcs | Stick Candle |
| 10 | 559233 | Home Decor | 1 set | Premium Scented Diffuser Set (Oudh) |

If a SKU did not exist yet in a month, write "not listed" for that month (do not leave it out).

## Also, for comparison: the whole Home Decor category

For each month, if the Competition > Brands view shows them, note the **category-level** weighted
discount and the **top 5 brands by share** with their weighted discount and weighted PPU.

## Columns to collect

For each SKU and month, from the SKUs table:
`month, product_id, sku_name, pack, sp, mrp, wt_discount_pct, est_cat_share_mrp_pct, wt_osa_pct, wt_ppu`

For the category check:
`month, category, brand, est_cat_share_mrp_pct, wt_discount_pct, wt_ppu`

## Rules

- Prefer the page's own Download / Export; otherwise read the values from the table on screen.
- Do not guess. If a value is not shown, write "not shown".
- Use YYYY-MM for months and keep names exactly as GobbleCube shows them.
- Note if MRP changes for any SKU between months: that is the most important thing to catch.
- Stop after about 30 minutes, or earlier when done.

## Give me at the end

1. A CSV-ready table with the SKU columns above (one row per SKU per month).
2. A CSV-ready table with the category columns above.
3. A short list of any SKU whose **MRP changed**, and any month where a SKU's SP moved more than
   15% from the month before.
4. Any file names you downloaded, with the filters used.

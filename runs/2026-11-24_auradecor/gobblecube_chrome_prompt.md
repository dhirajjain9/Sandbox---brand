# Claude in Chrome prompt: GobbleCube deep dive for Aura Decor

Copy everything below the line into Claude in Chrome, with GobbleCube open and signed in.

---

You are helping me collect quick-commerce data for one brand from GobbleCube, which is already
open and signed in in this browser. Work read-only: do not change any account, alert, team or
billing settings, do not share anything, and do not start paid add-ons. If something needs a
login, approval or payment, stop and tell me.

## The brand and where it sits

- **Brand:** Aura Decor. In GobbleCube it appears as **"Auradecor"** (one word). Do not confuse it
  with "Asian Aura", "AuraCam" or "Flower Aura", which are different brands.
- **What it sells:** candles and home fragrance: tea lights, pillar, jar, taper, votive and
  floating candles, candle gift sets, diyas, reed diffusers, oil burners / heat diffusers,
  aroma oils, potpourri, pooja gift hampers.
- **Main platform: Blinkit.** Aura has ~63 SKUs there. It has 1 SKU on Zepto and none on Instamart.

Categories to use (exact GobbleCube names):

| Platform | Category | Why |
|---|---|---|
| Blinkit | **Home Decor** | ~53 Aura SKUs; Aura ~45% category share in Oct 2026 |
| Blinkit | **Festive Gifting** | ~8 Aura gift sets; Aura ~43% share |
| Blinkit | **Pooja Needs** | 2 Aura SKUs (pooja hamper, diyas) |
| Zepto | **Pooja & Worship Needs** | 1 Aura SKU |
| Instamart | **Home Decor**, **Pooja Needs** | Check only: confirm Aura is absent |

Sub-categories: inside each category above, look for any sub-category or product-type level.
The ones I care about are anything like **Candles, Tea Lights, Diyas, Scented / Aroma Candles,
Diffusers / Reed Diffusers, Aroma / Essential Oils, Fragrance, Potpourri, Gift Sets / Hampers**.
Record the exact sub-category names GobbleCube uses.

Peer brands to keep in the same views where a view lists several brands: Homestrap, Shubh Kart,
Ekam, Party Propz, Dream Living, Prestige, Artisyn, Soulflower, Iris, Desidiya, Asian Aura.

## Step 1: map what exists (about 10 minutes)

Before downloading anything, explore the menus and tell me which of these views exist on our plan,
where they are (menu path), what filters they allow (platform, category, sub-category, brand, SKU,
city, pincode / dark store, keyword, date range, granularity: daily / weekly / monthly) and the
earliest date available:

1. Category / brand share over time (how far back does history go?)
2. SKU-level sales, offtake or units (are Offtake / Units filled or blank?)
3. Availability (OSA) by city, dark store or pincode
4. Keyword-level share of search (organic vs ad) and keyword search rank
5. Price and discount history by SKU
6. Category size (market size) by month
7. Anything else brand-level (e.g. brand dashboard, competitor benchmarking, new launches)

Report Step 1 as a table: View | Menu path | Filters available | Granularity | Earliest date |
Works on our plan? (yes / blank columns / locked). Then continue.

## Step 2: collect, in this priority order

Use **Blinkit** and the **Home Decor** and **Festive Gifting** categories unless a step says otherwise.
Prefer the tool's own Download / Export button. Only read numbers off the screen when there is no
export. For each download, tell me the file name and what filters it was taken with.

1. **History for year-on-year.** Category RCA (or the equivalent brand / SKU table) for Blinkit
   Home Decor and Festive Gifting, **monthly, as far back as available, at least Oct 2025 to
   Nov 2026**. Same columns as the standard RCA export (SP, MRP, Wt. OSA %, Wt. Discount %,
   Est. Category Share, Est. Category Share SP, Overall / Organic / Ad SOV).
2. **November 2026 to date** for the same two categories (post-Diwali check; Diwali was 8 Nov).
3. **Category size** (₹, MRP and SP) for Blinkit Home Decor and Festive Gifting for every month
   from Jul 2026 back as far as available. Note the unit shown (₹ Cr or ₹ lac) exactly.
4. **Keyword share of search on Blinkit** for these keywords, organic vs ad, Aura vs peers,
   latest month and one month before Diwali (Oct 2026):
   `candles`, `candle`, `scented candles`, `tea light candles`, `diya`, `diyas for diwali`,
   `diffuser`, `reed diffuser`, `aroma oil`, `candle gift set`, `diwali gift`, `pooja items`,
   `floating candles`, `auradecor`, `aura decor`.
   If the tool lets you search any keyword, also note the top 10 keywords where Auradecor appears.
5. **Availability (OSA) by city** (or dark store / pincode) for Auradecor on Blinkit, latest
   month: per city, the share of stores where Aura's top 10 SKUs are listed and in stock.
6. **SKU-level trend** for Aura's top 10 SKUs on Blinkit (by Est. Category Share SP), weekly or
   daily for Sep-Nov 2026, if that granularity exists.
7. **Price / discount history** for the same top 10 SKUs, if available.
8. **Checks:** search Instamart and Zepto for "Auradecor" / "Aura Decor" (all categories) and
   confirm SKU counts; note any differently spelled brand name that looks like the same brand.

## Rules

- Do not guess numbers. If a value is not shown, write "not shown". If a column is blank in an
  export, say so.
- Keep exact names for categories, sub-categories, brands and SKUs as GobbleCube shows them.
- Write all dates as YYYY-MM-DD, and say for each number whether it is MRP-based or SP-based.
- Stop after about 45 minutes of work, or earlier when done.

## What to give me at the end

1. The Step 1 table (what exists and where).
2. A list of downloaded files with: file name, view, platform, category, sub-category, date range,
   granularity.
3. Any numbers read off the screen, as tables with a header row, ready to paste into a CSV.
   Use these columns where they fit:
   - Keyword share: `platform, month, keyword, brand, organic_sov_pct, ad_sov_pct, overall_sov_pct, rank`
   - City availability: `platform, month, city, brand, sku, listed_stores_pct, in_stock_pct`
   - Category size: `platform, category, month, size_mrp, unit_mrp, size_sp, unit_sp`
4. Anything that was locked, blank or unavailable, and anything surprising you noticed.

# Test run 2: Aura Decor (24 Nov 2026)

Purpose: test how easy or hard it is to extract the Brand Fit Screen inputs for a
quick-commerce-first brand. This tests **the model and the process, not the brand**.

Category: candles and home fragrance (Amazon: Home & Kitchen > Home & Décor > Candles etc.;
quick commerce: inside Home Decor and Festive Gifting).

## What was pulled

| # | Export | Tool | Rows | Covers |
|---|---|---|---|---|
| 1 | GobbleCube Category RCA, Blinkit / Instamart / Zepto, Jul-Oct | GobbleCube | 77k (all brands) | Qcomm #22-29 |
| 2 | Brand search: AuraDecor | Keepa Product Finder | 650 ASINs | Listing data, ratings, price/list price, Buy Box, OOS, age, weight, sub-categories |
| 3 | Sub-category search: candles + home fragrance, no brand | Keepa Product Finder | 4,843 ASINs, 370 brands | Peer set |
| 4 | Brand AuraDecor, ASIN sales >= 10 (200-row cap) | Helium 10 Black Box | 200 ASINs | Sales estimates, YoY, 90-day trend |
| 5 | Sub-category pulls: Taper, Candle Sets, Pillar, Jar (+ one mixed pull) | Helium 10 Black Box | 129-200 each | Peer benchmarks per sub-category |

| 6 | 10-ASIN run + single-ASIN runs (6 Aura, 4 peers) | Helium 10 Cerebro | 7,367 keywords | Search rank, paid placement, branded and category search volume |

Not pulled (decided enough for this test): Tea Lights, star split and reviews, Flipkart,
D2C site, Instagram / Meta Ad Library.

## Effort

| Block | What it took |
|---|---|
| Quick commerce | **0 new pulls**: category files already held cover every brand |
| Amazon brand data | Keepa Product Finder (brand) + Helium 10 Black Box (brand) |
| Search rank and paid placement | Cerebro: one 10-ASIN run + single-ASIN runs, same day |
| Peer benchmarks | Keepa sub-category pull + one Black Box export per sub-category; processing about 1-2 minutes each |
| Hands-on time (estimate) | ~1.5-2 h of exports |

## What we learned about the process

1. **Category-level pulls are the scale lever.** One GobbleCube file per platform per month covers
   every brand; one Black Box / Keepa export per sub-category gives the full peer set.
2. **Helium 10 Black Box caps at 200 rows.** Workaround: set a minimum ASIN sales filter so the
   200 rows are the real sellers. Pull **one sub-category per export**; a multi-sub-category pull
   (pull 1) came back uneven and missed whole sub-categories.
3. **Keepa Product Finder does search by brand** (Brand field). Seller Lookup is the seller-wise view.
4. **The 'bought in past month' badge undercounts badly** (12,000 vs 22,100 Helium 10 units on the
   same ASINs; badge on only 57 of 255 families). Use Helium 10 for order estimates.
5. **Orders per rating differs hugely by category**: about 75-100 orders per new rating for
   low-ticket candles, vs 15 assumed in the sandbox. Calibrate per category.
6. **Seasonality distorts snapshots.** 82 of Aura's top 200 ASINs list Oct 2026 (Diwali) as their
   best month. Use year-on-year growth, not 90-day growth, for seasonal categories.
7. **Quick-commerce categories don't match Amazon's.** Candles sit inside Home Decor / Festive
   Gifting on Blinkit; a product-name keyword rule was needed to isolate them.
8. **Review counts are pooled across variation families** in both Keepa and Helium 10; count at
   family level.

## Provisional fit read (directional, not scored)

| Check | Read | Evidence | Confidence |
|---|---|---|---|
| 01 SKU Spikiness | Likely Clear | New pooja hamper at 1,425 units/month within 2 months; +29% 90-day (festive) | Medium |
| 02 Demand Durability | Likely Clear | +20% YoY on Amazon; Blinkit share up from 32% to 45% Jul-Oct; listings 3-4 years old still top-ranked | Medium |
| 03 Qcomm Traction | Clear on Blinkit, absent elsewhere | ~45% of Blinkit Home Decor; not on Instamart, 1 SKU on Zepto | High |
| 04 Customer Quality (must-clear) | Borderline | Weighted rating 3.96-4.09, in line with peers; star split and reviews not read | Low |
| 05 Pricing Power (must-clear) | **Likely Miss** | 68% median discount off list price; below category average price in 3 of 4 sub-categories; premium end held by others (except Candle Sets) | Medium-High |
| 06 Concentration Risk | Mixed | Product mix well spread (top ASIN 21-32% of units); channel heavily concentrated on Blinkit; high copy exposure (new brands reach top 5 in 2-3 months) | Medium |

Amazon position: #1 in Taper Candles (37%), #3 in Pillar (7.5%, but down 20% YoY while the
sub-category grew 52%), #5 in Candle Sets (#2 by revenue) and Jar Candles.

## Cerebro (added after first notes)

One 10-ASIN Cerebro run (6 Aura + 4 peers) plus single-ASIN runs for each.
A multi-ASIN export gives organic rank for every ASIN but sponsored rank only for the
first ASIN; single-ASIN runs are needed for paid vs organic per product.

- **Category search demand (#37):** ~1.02M searches/month on core candle and fragrance keywords.
- **Branded search (#36):** Aura Decor ~4,600/month vs Iris ~15,800, Ekam ~5,100, Floryn and Vervenix ~300.
- **Search rank (#18):** Aura's taper candle ASIN ranks #2-3 on "candle" (73.8k) and "candles" (48.4k);
  it carries most of Aura's top-10 visibility. Other Aura ASINs are page 1 but rarely top 10.
- **Paid dependence (#19):** Aura's established ASINs show almost no sponsored placements (0-2% of
  visible search volume). The new pooja hamper is the exception: 61% of its visible search volume is
  sponsored, 52% sponsored-only. Peers: Floryn 22%, Ekam 26%, Vervenix 2%, Prosperro 0%.

Revised reads: SKU Spikiness Medium-Low (the standout new SKU is ad-driven); Demand Durability
strengthened (earned organic rank on the category's biggest keywords, low ad reliance);
Concentration Risk adds a flag (one ASIN carries most organic visibility).

## GobbleCube deep dive (Claude in Chrome, Blinkit)

- Access: the GobbleCube login is another brand's workspace, so own-brand views (Trends, keyword
  SOV, Offtake / Units) are empty for Aura. **Competition views** (brand and SKU share, OSA,
  discount, SOV) and category size work for any brand, with history back to 2025-07-27.
- No sub-categories in GobbleCube: product type = category, so the keyword rule is needed.
- Share and size here are **MRP-based**; Aura's SP-based share is lower (Oct 2026: 45% SP vs
  55.8% MRP), so its MRPs are inflated relative to peers. ₹ sales on MRP are ~2.5-3x SP.
- **Share grew sharply year on year:** Home Decor 32% (Aug-Sep 2025) to 50% (Aug-Sep 2026);
  60.8% in Nov 2026 to date.
- **Festive season (Diwali 2025-10-20, 2026-11-08):** Aug-Nov MRP sales ~Rs 42.8 Cr (2025) vs
  ~Rs 49.6 Cr (2026, Nov to the 22nd): **+16% and rising**, while Blinkit Home Decor shrank 15%
  (Rs 86.7 Cr to 74.0 Cr). The growth is share, not category.
- **Last 12 months (Dec 2025-Nov 2026): ~Rs 107 Cr MRP** on Blinkit Home Decor + Festive Gifting;
  at ~65% weighted discount that is roughly Rs 35-40 Cr at selling price. Off-season run rate
  (Jan-Jul 2026) ~Rs 6.9 Cr MRP a month.
- **Earned visibility rising:** Home Decor organic SOV 35% (Aug 2025) to 60% (Sep-Oct 2026). Ad SOV
  is bursty (0-12% most months, 28-42% in Jun, Jul, Sep, Oct 2026).
- **Discount creeping up:** weighted discount ~56-57% (Aug-Sep 2025) to ~65% (2026).
- **Availability is the weak spot:** Wt. OSA dips to 46-56% at peaks and in summer (Jun 2026 49.5%,
  Nov 2026 56% Home Decor / 46% Festive Gifting).
- **Festive Gifting competition rising:** Dream Living 3.5% to 22.4%, Artisyn ~20%; Aura's
  gifting share is 32.7% in Nov 2026 vs 35.7% in Nov 2025.
- **Blinkit keywords:** Aura ranks #2 organic and #1 ad on "candle" and "scented candle";
  no presence on "diya" (~11.8 lac searches).
- Pooja Needs: Auradecor not in the brand list for Oct or Nov 2026.

File: `gobblecube_deep_dive_blinkit_monthly.csv` (brand x category x month: share, OSA, listing,
discount, organic / ad SOV, PPU, category size, Aura MRP sales).

## Files in this folder

- `qcomm_aroma_candles_*.csv`: quick-commerce SKU and brand-month extract, Aura + peers
- `amazon_families_keepa.csv`, `amazon_subcategories_keepa.csv`: Aura catalogue from Keepa
- `amazon_peer_brands_candles_fragrance.csv`: Keepa peer table
- `amazon_h10_top200_enriched.csv`, `amazon_h10_families.csv`: Aura sales from Black Box
- `amazon_h10_peer_brands_*.csv`: Black Box peer tables per sub-category

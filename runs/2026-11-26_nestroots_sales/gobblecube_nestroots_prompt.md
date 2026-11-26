# Claude in Chrome prompt: Nestroots quick-commerce sales by platform (GobbleCube)

Copy everything below the line into Claude in Chrome, with GobbleCube open and signed in.

---

You are collecting quick-commerce sales for one brand from GobbleCube, which is open and signed in
in this browser. Work read-only: do not change account, alert, team or billing settings, do not
share anything, and do not start paid add-ons. If something needs a login, approval or payment,
stop and tell me.

## The brand

- **Brand:** Nestroots (may appear as "nestroots", "Nest Roots" or "NestRoots"). Check spellings and
  tell me every variant you find. Do not confuse it with other "Nest" brands.
- **What it sells:** wooden and acacia kitchen and serveware (napkin holders, roti casseroles,
  masala boxes, cake stands, bowls, racks and holders), home decor (urli bowls, decorative bowls),
  ottomans and some office chairs.
- **Platforms:** Blinkit, Zepto, Instamart. I don't know yet where it is listed.

## Step 1: find it (about 10 minutes)

1. Search for the brand on each platform. Likely categories: **Home Decor**, **Kitchen / Kitchenware /
   Kitchen & Dining**, **Serveware**, **Festive Gifting**, **Home Needs / Home Improvement**. Use the
   brand search if GobbleCube has one; otherwise check each of these categories per platform.
2. For each platform, tell me: listed (yes / no), number of Nestroots SKUs, and the exact
   GobbleCube category names they sit in.

## Step 2: sales by platform (about 20 minutes)

For every platform and category where Nestroots is listed, use Category RCA (or the brand / SKU
table that gives the same figures), **monthly, Dec 2025 to Nov 2026** (as far back as available),
and record per month:

- Nestroots **Est. Category Share** (MRP) and **Est. Category Share SP**
- **Category size** for that month, MRP and SP, with the unit exactly as shown (₹ Cr or ₹ lac)
- Number of Nestroots SKUs, Wt. OSA %, Wt. Discount %

Prefer the Download / Export button; read numbers off the screen only when there is no export.
For each download, tell me the file name and the filters used.

If GobbleCube shows Nestroots' sales directly (₹ offtake or units), give those as well and say so.

## Rules

- Do not guess numbers. Write "not shown" when a value is missing; say if an export column is blank.
- Keep exact names for categories, brands and SKUs. Dates as YYYY-MM. Say whether each number is
  MRP-based or SP-based.
- Stop after about 35 minutes, or earlier when done.

## What to give me at the end

1. Step 1 table: `platform, listed, skus, categories`.
2. A table ready to paste as CSV:
   `platform, category, month, nestroots_share_mrp_pct, nestroots_share_sp_pct, category_size_mrp, category_size_sp, unit, skus, osa_pct, discount_pct`
3. Any direct sales figures, the list of downloaded files, and anything locked, blank or surprising.

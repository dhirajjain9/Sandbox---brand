# Claude in Chrome run sheet: TEKAVO customer quality, social, ads, D2C, Flipkart and quick commerce

Copy everything below the line into Claude in Chrome. You need to be signed in to Amazon.in (reviews
need a signed-in session). No other logins are needed; if a site asks you to log in, skip that item.

---

You are collecting public, outside-in information about the **TEKAVO group**: three sister furniture brands, **TEKAVO**, **FFO (Furniture Factory Outlet)** and **Deskio** (Computer tables, office desks and storage furniture;
Amazon sellers: **EVERS** (73% of revenue), **Furniture Factory Outlet** (27% of revenue)) for a brand evaluation. Work
read-only: do not post, follow, like, message, add to cart beyond what a step says, place orders,
or change any account settings. Do not guess numbers: if something is not shown, write "not
shown". Stop after about 80 minutes, or earlier when done.

## Part 1: Amazon.in star splits and reviews (about 40 minutes)

For each ASIN below, open `https://www.amazon.in/dp/<ASIN>`:

| # | ASIN | Product |
|---|---|---|
| 1 | B0F1DKCW78 | TEKAVO Kynes Computer Table for Home Pc | Office Table for Home with L |
| 2 | B0GT58FQX7 | FFO Washing Machine Rack for Front Load Washer & Dryer | Dishwasher St |
| 3 | B0H9Z3NJRK | FFO Nova Computer Table for Home pc with 2 Side Storage & Drawer, 150  |
| 4 | B0GDTM7VC2 | FFO FURNITURE FACTORY OUTLET Bedside Table with Drawers | 1-Year Warra |
| 5 | B0HHN51X79 | TEKAVO Tonny L Shape Table for Home Office, Computer Table for Home Pc |
| 6 | B0BWV3XFD2 | TEKAVO Trio Computer Table for Home Pc | Office Table for Home with Mo |
| 7 | B0HJ4XM539 | FFO Stepora Shoe Racks with 2 Doors & Open Shelves | Multipurpose Foot |
| 8 | B0GS9KYHYF | FFO Foldable Dining Table for Home for 4 Seater Space-Saving Wooden Fo |
| 9 | B0GDY869K6 | FFO Foldable Dining Table for Home for 4 Seater Space-Saving Wooden Fo |
| 10 | B0HKCT8NLS | TEKAVO Zento Wooden Shoe Rack with 2 Doors White & Mile Oak - 75x35x11 |

For each:

1. **Star split:** total ratings, average rating, and the % for 5, 4, 3, 2 and 1 star. If several
   products share one rating pool (same numbers), say so.
2. **Reviews:** read the **20 most recent** reviews and the **10 most recent critical** (1-2 star)
   reviews (if Amazon shows 10 per page, build the 20 most recent from the newest at each star
   level, and say so). Count how many mention:
   - damaged / broken / dented on arrival
   - defect or stops working (breaks, stops working, poor build, wobble, noise, finish problems)
   - smaller / less powerful than described, or missing parts
   - wrong item or used product
   - safety issue (shock, fire, collapse, sharp edges, chemical smell) - quote it briefly
   - poor service: installation delay (large items), warranty or service-centre problems
3. Top 3 complaints in a few words, and Amazon's "Customers say" summary if shown.

## Part 2: Seller pages (3 minutes)

Open the seller page for each seller named above (click the seller name on a listing). Note the
feedback rating and the positive / neutral / negative split for 30 days, 90 days, 12 months and
lifetime, and the number of ratings. If the page only shows star splits, give those.

## Part 3: Meta Ad Library (5 minutes)

`https://www.facebook.com/ads/library/`, country **India**, **All ads**, search **TEKAVO**, then **FFO Furniture Factory Outlet**, then **Deskio** (report each advertiser separately). Note:
active ads, how many started in the last 30 days, platforms, 2-3 example ad themes, and where the
ads link to.

## Part 4: Instagram (10 minutes)

Find the official Instagram accounts for TEKAVO, FFO (Furniture Factory Outlet) and Deskio (search each name; report each account separately). Note: followers, total posts, posts in the
last 30 days, likes and comments for the 12 most recent posts (and the median likes of the
brand's own posts), creator collaborations in the last 90 days with up to 5 handles.

## Part 5: TEKAVO, FFO and Deskio websites (10 minutes)

Search for each brand's own website (e.g. tekavo.in / tekavo.com, ffo / furniturefactoryoutlet, deskio.in / deskio.com). If one sells online: number of
products (Shopify: `<site>/products.json`), sold-out count on the first two pages, sale banner and
typical discount %, new arrivals, and the checkout terms (COD, COD fee, free-shipping threshold)
**without placing an order**; empty the cart afterwards. Also note the company name in the
footer, contact or policy pages (who owns the brand).

## Part 6: Flipkart (5 minutes)

Search flipkart.com for **TEKAVO**, **FFO** and **Deskio**. Note whether it sells there, approximate listings, sellers
seen, and for the top 5 listings the price, MRP, rating and number of ratings.

## Part 7: Quick commerce (5 minutes)

Search **TEKAVO**, **FFO** and **Deskio** on blinkit.com, zeptonow.com and swiggy.com/instamart (use any delivery pincode
in Delhi or Bengaluru if asked; do not log in). For each: listed or not, how many products, and
2-3 example products with price and MRP.

## What to give me at the end

CSV-ready tables:

1. `asin, total_ratings, avg_rating, pct_5, pct_4, pct_3, pct_2, pct_1, pooled_family(y/n),
   reviews_read, damaged, defect, smaller_missing, wrong_used, safety, service, top_complaints`
2. `seller, period, positive_pct, neutral_pct, negative_pct, ratings`
3. One row per advertiser: `advertiser, active_ads, started_last_30d, platforms, links_to, example_themes`
4. One row per account: `handle, followers, total_posts, posts_last_30d, avg_likes_12, median_likes_own, avg_comments_12,
   creator_collabs_90d, creator_handles`
5. One row per site: `site, owner_company, products, sold_out_first_2_pages, sale_banner, typical_discount_pct,
   new_arrivals, cod_available, cod_fee, free_shipping_threshold`
6. `on_flipkart, listings, sellers_seen`, then per top listing `title, price, mrp, rating, ratings_count`
7. `platform, listed, products, example_products`
8. Anything you could not do, and why.

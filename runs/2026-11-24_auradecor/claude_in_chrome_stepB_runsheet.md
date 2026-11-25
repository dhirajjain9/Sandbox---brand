# Claude in Chrome run sheet: Aura Decor customer quality, social, ads, D2C and Flipkart

Copy everything below the line into Claude in Chrome. You need to be signed in to Amazon.in (reviews
need a signed-in session). No other logins are needed; if a site asks you to log in, skip that item.

---

You are collecting public, outside-in information about the brand **AuraDecor / Aura Decor**
(candles, scented candles, diyas, diffusers, potpourri and festive gift sets) for a brand
evaluation. Work read-only: do not post, follow, like, message, add to cart beyond what a step
says, place orders, or change any account settings. Do not guess numbers: if something is not
shown, write "not shown". Stop after about 75 minutes, or earlier when done.

## Part 1: Amazon.in star splits and reviews (about 40 minutes)

For each ASIN below, open `https://www.amazon.in/dp/<ASIN>`:

| # | ASIN | Product |
|---|---|---|
| 1 | B0H71SYY4J | Divine Pooja gift hamper (lotus urli candle, dhoop, diyas) |
| 2 | B07V4YRJX5 | Floating candles, pack of 20 nuggets |
| 3 | B0C2J1BT96 | Fragrance heat diffuser gift set with tealights |
| 4 | B0D3F5QLDD | Wax lotus candle gift set (urli) |
| 5 | B0983JPZL6 | Unscented stick / taper candles, pack of 20 |
| 6 | B0H2HM25RY | Vanilla caramel scented pillar candles, set of 2 |
| 7 | B0C9T8VV26 | Ivory taper candles, dripless |
| 8 | B0CB3864MH | Soy wax scented jar candles, set of 4 |
| 9 | B0C2Q8SBGC | Fragrance votive glass candles, set of 4 |
| 10 | B096BHFD4G | Dried natural fragrance potpourri, 150 g |

For each:

1. **Star split:** note total ratings, average rating, and the % for 5, 4, 3, 2 and 1 star from the
   rating histogram. If several products share one rating pool (same numbers), say so.
2. **Reviews:** open "See more reviews". Read the **20 most recent** reviews and the **10 most
   recent critical** (1-2 star) reviews. Count how many of the 30 mention:
   - damaged / broken / melted item on arrival
   - defect or poor quality (weak or no fragrance, uneven burn, tunnelling, smoke, wick problems)
   - smaller than shown / fewer pieces than stated
   - wrong item, wrong colour or scent, missing pieces
   - safety issue (fire, glass cracking, chemical smell, skin reaction) - quote it briefly
3. Note the top 3 complaints in a few words, and Amazon's "Customers say" summary if shown.

## Part 2: Seller page (2 minutes)

Open the Aura Decor seller page (click the seller name, usually "Auradecor", on any listing). Note
the feedback rating, % positive / neutral / negative for 30 days, 90 days, 12 months and lifetime,
and the number of ratings.

## Part 3: Meta Ad Library (5 minutes)

Open `https://www.facebook.com/ads/library/`, country **India**, ad category **All ads**, search
**AuraDecor** (also try "Aura Decor"). Pick the Aura Decor advertiser page. Note: number of
**active** ads, how many started in the last 30 days, platforms (Facebook / Instagram), and 2-3
example ad themes (product, offer, discount shown).

## Part 4: Instagram (10 minutes)

Find Aura Decor's official Instagram account (search "auradecor"; check it links to Amazon or an
Aura Decor website). Note: followers, total posts, posts in the last 30 days, and for the 12 most
recent posts the likes and comments (to compute engagement). Count posts in the last 90 days that
are collaborations with creators (collab posts, tagged creators, "paid partnership" labels) and
list up to 5 creator handles.

## Part 5: Aura Decor website (10 minutes)

Search for Aura Decor's own website (e.g. auradecor.in or auradecor.com). If one exists:

1. Catalogue: approximate number of products (if the site is Shopify, open `<site>/products.json`
   and count, or use the collection page counts). Count products marked "sold out" on the first
   two pages of the main collection.
2. Sales: is there a site-wide sale or discount banner now? Typical discount % shown.
3. New launches: any "new arrivals" collection; how many items.
4. Checkout: add one low-price item to the cart and go to checkout **without placing the order**.
   Note whether cash on delivery is offered and any COD fee, the free-shipping threshold, then
   remove the item.

If there is no website, say so.

## Part 6: Flipkart (5 minutes)

Search flipkart.com for **AuraDecor** and **Aura Decor**. Note: whether Aura Decor sells there,
approximate number of listings shown, and for the top 5 listings the price, MRP, rating and number
of ratings.

## What to give me at the end

Tables I can paste into a CSV:

1. Part 1: `asin, total_ratings, avg_rating, pct_5, pct_4, pct_3, pct_2, pct_1, pooled_family(y/n),
   reviews_read, damaged, defect_quality, smaller_fewer, wrong_item, safety, top_complaints`
2. Part 2: `period, positive_pct, neutral_pct, negative_pct, ratings`
3. Part 3: `active_ads, started_last_30d, platforms, example_themes`
4. Part 4: `handle, followers, total_posts, posts_last_30d, avg_likes_12, avg_comments_12,
   creator_collabs_90d, creator_handles`
5. Part 5: `site, products, sold_out_first_2_pages, sale_banner, typical_discount_pct,
   new_arrivals, cod_available, cod_fee, free_shipping_threshold`
6. Part 6: `on_flipkart, listings, then per top listing: title, price, mrp, rating, ratings_count`
7. Anything you could not do, and why.

# Claude in Chrome run sheet: HOKIPO customer quality, social, ads, D2C and Flipkart

Copy everything below the line into Claude in Chrome. You need to be signed in to Amazon.in (reviews
need a signed-in session). No other logins are needed; if a site asks you to log in, skip that item.

---

You are collecting public, outside-in information about the brand **HOKIPO** (home furnishing:
sofa covers, armrest covers, chair covers, storage, doormats) for a brand evaluation. Work
read-only: do not post, follow, like, message, add to cart beyond what a step says, place orders,
or change any account settings. Do not guess numbers: if something is not shown, write
"not shown". Stop after about 75 minutes, or earlier when done.

## Part 1: Amazon.in star splits and reviews (about 40 minutes)

For each ASIN below, open `https://www.amazon.in/dp/<ASIN>`:

| # | ASIN | Product |
|---|---|---|
| 1 | B0BR418RPM | Chenille sofa cover 3-seater throw |
| 2 | B0CSSLYYJH | Plush Haven sofa cover mat 3-seater |
| 3 | B0GNM9PDNN | Nestiva fully covered sofa cover 3-seater |
| 4 | B0BTD2QYGK | Jacquard stretchable sofa cover 3-seater |
| 5 | B0DPWK95JC | FurHug faux-fur winter sofa cover |
| 6 | B0GM5TZPBQ | Royal Aangan 5-seater panel set |
| 7 | B0DRKZKJX3 | Nestiva sofa cover (Burgundy) |
| 8 | B0DPX4QY5C | FurHug armrest cover |
| 9 | B09LS4WWVB | Wall-mounted dustbin |
| 10 | B0765T4X14 | Laundry bag / basket |

For each:

1. **Star split:** note total ratings, average rating, and the % for 5, 4, 3, 2 and 1 star from the
   rating histogram. If several products share one rating pool (same numbers), say so.
2. **Reviews:** open "See more reviews". Read the **20 most recent** reviews and the **10 most
   recent critical** (1-2 star) reviews. Count how many of the 30 mention:
   - damaged / dirty / used item on arrival
   - defect or poor quality (tears, stitching, colour fades, pilling, shrinks)
   - wrong size / does not fit / smaller than shown
   - wrong item, wrong colour, missing pieces
   - safety issue (fire, chemical smell, skin reaction) - quote it briefly
3. Note the top 3 complaints in a few words, and Amazon's "Customers say" summary if shown.

## Part 2: Seller page (2 minutes)

Open the HOKIPO seller page (click the seller name "HOKIPO" on any listing). Note the feedback
rating, % positive / neutral / negative for 30 days, 90 days, 12 months and lifetime, and the
number of ratings.

## Part 3: Meta Ad Library (5 minutes)

Open `https://www.facebook.com/ads/library/`, country **India**, ad category **All ads**, search
**HOKIPO**. Pick the HOKIPO advertiser page. Note: number of **active** ads, how many started in
the last 30 days, platforms (Facebook / Instagram), and 2-3 example ad themes (product, offer,
discount shown).

## Part 4: Instagram (10 minutes)

Find HOKIPO's official Instagram account (search "hokipo"; check it links to Amazon or a HOKIPO
website). Note: followers, total posts, posts in the last 30 days, and for the 12 most recent
posts the likes and comments (to compute engagement). Count posts in the last 90 days that are
collaborations with creators (collab posts, tagged creators, "paid partnership" labels) and list
up to 5 creator handles.

## Part 5: HOKIPO website (10 minutes)

Search for HOKIPO's own website (e.g. hokipo.com or hokipo.in). If one exists:

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

Search flipkart.com for **HOKIPO**. Note: whether HOKIPO sells there, approximate number of
listings shown, and for the top 5 listings the price, MRP, rating and number of ratings.

## What to give me at the end

Tables I can paste into a CSV:

1. Part 1: `asin, total_ratings, avg_rating, pct_5, pct_4, pct_3, pct_2, pct_1, pooled_family(y/n),
   reviews_read, damaged, defect_quality, wrong_size, wrong_item, safety, top_complaints`
2. Part 2: `period, positive_pct, neutral_pct, negative_pct, ratings`
3. Part 3: `active_ads, started_last_30d, platforms, example_themes`
4. Part 4: `handle, followers, total_posts, posts_last_30d, avg_likes_12, avg_comments_12,
   creator_collabs_90d, creator_handles`
5. Part 5: `site, products, sold_out_first_2_pages, sale_banner, typical_discount_pct,
   new_arrivals, cod_available, cod_fee, free_shipping_threshold`
6. Part 6: `on_flipkart, listings, then per top listing: title, price, mrp, rating, ratings_count`
7. Anything you could not do, and why.

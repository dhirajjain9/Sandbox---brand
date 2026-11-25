# Claude in Chrome run sheet: CADLEC customer quality, social, ads, D2C, Flipkart and quick commerce

Copy everything below the line into Claude in Chrome. You need to be signed in to Amazon.in (reviews
need a signed-in session). No other logins are needed; if a site asks you to log in, skip that item.

---

You are collecting public, outside-in information about the brand **CADLEC** (small kitchen and
home appliances: OTGs, mixer grinders, induction and infrared cooktops, ceiling fans, chimneys,
immersion rods, kettles; Amazon seller mostly **RetailEZ Pvt Ltd**) for a brand evaluation. Work
read-only: do not post, follow, like, message, add to cart beyond what a step says, place orders,
or change any account settings. Do not guess numbers: if something is not shown, write "not
shown". Stop after about 80 minutes, or earlier when done.

## Part 1: Amazon.in star splits and reviews (about 40 minutes)

For each ASIN below, open `https://www.amazon.in/dp/<ASIN>`:

| # | ASIN | Product |
|---|---|---|
| 1 | B0FNK7Z1JY | MultiChef Pro 3-in-1 breakfast maker / OTG |
| 2 | B0DP9JPG3L | JarGenie 750W mixer grinder, 4 jars |
| 3 | B0FQ7KCSTR | Grevity 1200mm BLDC ceiling fan with remote |
| 4 | B0DSLC124L | Breeza 1200mm ceiling fan |
| 5 | B0FSRMV225 | HeatMate 2200W infrared cooktop |
| 6 | B0FTSFX9LH | CookFusion_5 2000W induction cooktop |
| 7 | B0G46R7RZG | CurveFlow 60cm BLDC kitchen chimney |
| 8 | B0FHQB7HXR | CookEase 2000W induction cooktop |
| 9 | B0DJKY1NBL | HeatJet 1500W immersion rod |
| 10 | B0D9QFYP35 | 1.8L electric kettle + bottle combo |

For each:

1. **Star split:** total ratings, average rating, and the % for 5, 4, 3, 2 and 1 star. If several
   products share one rating pool (same numbers), say so.
2. **Reviews:** read the **20 most recent** reviews and the **10 most recent critical** (1-2 star)
   reviews (if Amazon shows 10 per page, build the 20 most recent from the newest at each star
   level, and say so). Count how many mention:
   - damaged / broken / dented on arrival
   - defect or stops working (motor failure, not heating, burnt smell, display or button failure,
     noise, wobble)
   - smaller / less powerful than described, or missing parts
   - wrong item or used product
   - safety issue (shock, sparks, fire, melting, overheating) - quote it briefly
   - poor service: installation delay (fans, chimneys), warranty or service-centre problems
3. Top 3 complaints in a few words, and Amazon's "Customers say" summary if shown.

## Part 2: Seller pages (3 minutes)

Open the seller page for **RetailEZ Pvt Ltd** (click the seller name on any listing) and for
**Dawntech Electronics** (on the chimney). Note the feedback rating and the positive / neutral /
negative split for 30 days, 90 days, 12 months and lifetime, and the number of ratings. If the
page only shows star splits, give those.

## Part 3: Meta Ad Library (5 minutes)

`https://www.facebook.com/ads/library/`, country **India**, **All ads**, search **CADLEC**. Note:
active ads, how many started in the last 30 days, platforms, 2-3 example ad themes, and where the
ads link to.

## Part 4: Instagram (10 minutes)

Find CADLEC's official Instagram (search "cadlec"). Note: followers, total posts, posts in the
last 30 days, likes and comments for the 12 most recent posts (and the median likes of the
brand's own posts), creator collaborations in the last 90 days with up to 5 handles.

## Part 5: CADLEC website (10 minutes)

Search for CADLEC's own website (e.g. cadlec.in / cadlec.com). If one sells online: number of
products (Shopify: `<site>/products.json`), sold-out count on the first two pages, sale banner and
typical discount %, new arrivals, and the checkout terms (COD, COD fee, free-shipping threshold)
**without placing an order**; empty the cart afterwards. Also note the company name in the
footer, contact or policy pages (who owns the brand).

## Part 6: Flipkart (5 minutes)

Search flipkart.com for **CADLEC**. Note whether it sells there, approximate listings, sellers
seen, and for the top 5 listings the price, MRP, rating and number of ratings.

## Part 7: Quick commerce (5 minutes)

Search **CADLEC** on blinkit.com, zeptonow.com and swiggy.com/instamart (use any delivery pincode
in Delhi or Bengaluru if asked; do not log in). For each: listed or not, how many products, and
2-3 example products with price and MRP.

## What to give me at the end

CSV-ready tables:

1. `asin, total_ratings, avg_rating, pct_5, pct_4, pct_3, pct_2, pct_1, pooled_family(y/n),
   reviews_read, damaged, defect, smaller_missing, wrong_used, safety, service, top_complaints`
2. `seller, period, positive_pct, neutral_pct, negative_pct, ratings`
3. `active_ads, started_last_30d, platforms, links_to, example_themes`
4. `handle, followers, total_posts, posts_last_30d, avg_likes_12, median_likes_own, avg_comments_12,
   creator_collabs_90d, creator_handles`
5. `site, owner_company, products, sold_out_first_2_pages, sale_banner, typical_discount_pct,
   new_arrivals, cod_available, cod_fee, free_shipping_threshold`
6. `on_flipkart, listings, sellers_seen`, then per top listing `title, price, mrp, rating, ratings_count`
7. `platform, listed, products, example_products`
8. Anything you could not do, and why.

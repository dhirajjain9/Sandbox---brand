# Claude in Chrome run sheet: Milton Home Appliances social, ads, D2C and Flipkart

Copy everything below the line into Claude in Chrome. No logins are needed; if a site asks you to
log in, skip that item. (Amazon star splits and reviews were already collected in the earlier
Helium 10 run, so they are not repeated here.)

---

You are collecting public, outside-in information about **Milton Home Appliances**: small kitchen
appliances (electric kettles, sandwich makers, egg boilers, multi-cook kettles, induction and
infrared cooktops, gas stoves) sold under the "Milton" brand by **Hydro Valves**.

**Do not mix it up with** the original Milton housewares brand (bottles, flasks, lunch boxes,
casseroles; Hamilton Housewares) or with Hamilton Beach. Wherever an account, page, website or
listing could belong to either, check whether it sells appliances and whether it names Hydro
Valves or "Milton Home Appliances"; say which one you used and why. If Milton appliances and
housewares share one account, say so.

Work read-only: do not post, follow, like, message, add to cart beyond what a step says, place
orders, or change any account settings. Do not guess numbers: if something is not shown, write
"not shown". Stop after about 45 minutes, or earlier when done.

## Part 1: Meta Ad Library (5 minutes)

Open `https://www.facebook.com/ads/library/`, country **India**, ad category **All ads**, search
**Milton Home Appliances** (also try "Milton appliances"). Pick the appliances advertiser page,
not Milton housewares. Note: number of **active** ads, how many started in the last 30 days,
platforms (Facebook / Instagram), and 2-3 example ad themes (product, offer, discount shown). If
only a combined Milton page advertises, note the share of active ads that show appliances.

## Part 2: Instagram (10 minutes)

Find the official Instagram account for Milton Home Appliances (search "milton home appliances",
"miltonappliances"). Note: followers, total posts, posts in the last 30 days, and for the 12 most
recent posts the likes and comments (to compute engagement). Count posts in the last 90 days that
are collaborations with creators (collab posts, tagged creators, "paid partnership" labels) and
list up to 5 creator handles.

## Part 3: Milton Home Appliances website (10 minutes)

Search for the appliances brand's own website (it may be a sub-site or section of a Milton site;
use the one that sells appliances). If one sells online:

1. Catalogue: approximate number of appliance products (if the site is Shopify, open
   `<site>/products.json` and count, or use the collection page counts). Count products marked
   "sold out" on the first two pages of the main collection.
2. Sales: is there a site-wide sale or discount banner now? Typical discount % shown.
3. New launches: any "new arrivals" collection; how many items.
4. Checkout: add one low-price item to the cart and go to checkout **without placing the order**.
   Note whether cash on delivery is offered and any COD fee, the free-shipping threshold, then
   remove the item.

If there is no website that sells online, say so (and give the URL if there is a catalogue-only
site).

## Part 4: Flipkart (5 minutes)

Search flipkart.com for **Milton electric kettle**, **Milton sandwich maker** and **Milton egg
boiler**. Note: whether Milton appliances sell there, approximate number of appliance listings,
the seller name shown on listings, and for the top 5 appliance listings the price, MRP, rating and
number of ratings.

## What to give me at the end

Tables I can paste into a CSV:

1. Part 1: `advertiser_page, active_ads, started_last_30d, platforms, appliance_share, example_themes`
2. Part 2: `handle, followers, total_posts, posts_last_30d, avg_likes_12, avg_comments_12,
   creator_collabs_90d, creator_handles, shared_with_housewares(y/n)`
3. Part 3: `site, products, sold_out_first_2_pages, sale_banner, typical_discount_pct,
   new_arrivals, cod_available, cod_fee, free_shipping_threshold`
4. Part 4: `on_flipkart, listings, sellers_seen, then per top listing: title, seller, price, mrp,
   rating, ratings_count`
5. Anything you could not do, and why.

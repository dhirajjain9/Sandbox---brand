"""Map quick-commerce products (Blinkit / Zepto / Instamart) onto Amazon India leaf categories.

The Amazon category tree is the backbone: the target label for every product is an Amazon leaf
category (Helium 10 Black Box `Subcategory`). Amazon rows need no classification - each Black Box
row already carries its leaf. Quick-commerce products are assigned by

1. rules: out-of-scope products (clothing, footwear, stationery, electronics accessories, food,
   paper disposables) and a few Indian-term / obvious overrides;
2. a text model trained on Amazon titles (TF-IDF word + char n-grams, LinearSVC), with a
   confidence calibrated on a 20% hold-out of Amazon titles;
3. below the confidence threshold: "Unmatched", or "Awaiting wave N" when the product's platform
   category belongs to an extraction wave (runs/_target/master_list_waves.csv) whose Amazon
   categories are not pulled yet.

    python -m pipeline.qcom_to_amazon            # build everything below
    python -m pipeline.qcom_to_amazon --sample 40   # also print a random sample of matches

Inputs: Black Box exports under data/raw/helium10/wave1/, data/raw/sourcing/ and the brand-run
Black Box files in data/raw/helium10/; GobbleCube data/raw/gobblecube/rca_JulOct.csv.gz;
runs/_taxonomy/keepa_in_tree.jsonl for the Amazon path (partial tree: path blank if not found).

Outputs (runs/_taxonomy/):
- amazon_leaves.csv: Amazon leaf label set (leaf, dominant Black Box category, ASINs, revenue,
  Keepa path, in_scope, trained)
- qcom_amazon_match.csv: platform, product_id, product_name, platform_category, brand,
  amazon_leaf, amazon_path, confidence, method (rule / model / unmatched / out_of_scope)
- qcom_amazon_coverage.csv: coverage by platform x platform category (products and Sep-Oct
  share-weighted)
"""
import argparse
import glob
import json
import re

import numpy as np
import pandas as pd

from pipeline.category_groups import QCOM_TO_GROUP

QCOM_SRC = "data/raw/gobblecube/rca_JulOct.csv.gz"
BB_GLOBS = ["data/raw/helium10/wave1/**/*.csv", "data/raw/sourcing/**/*.csv",
            "data/raw/helium10/*blackbox*.csv", "data/raw/helium10/*/bb_*.csv"]
KEEPA = "runs/_taxonomy/keepa_in_tree.jsonl"
WAVES = "runs/_target/master_list_waves.csv"
OUT_LEAVES = "runs/_taxonomy/amazon_leaves.csv"
OUT_MATCH = "runs/_taxonomy/qcom_amazon_match.csv"
OUT_COVER = "runs/_taxonomy/qcom_amazon_coverage.csv"

MIN_TRAIN = 5          # a leaf needs this many ASINs to be learnt
THRESHOLD = 0.45       # calibrated confidence below which a model match is not used
# Black Box categories that are not home & kitchen (clothing, stationery, electronics accessories, food...)
OUT_CATS = {"Grocery & Gourmet Foods", "Clothing & Accessories", "Office Products", "Computers & Accessories", "Electronics",
            "Jewellery", "Beauty", "Books", "Video Games", "Pet Supplies", "Shoes & Handbags"}
NON_HOME_LEAVES = r"protein|creatine|gainer|pre-workout|moringa|razor|toothpaste|body wash|teether|supplement|bikini|sonic\b"
IN_LEAVES = {"Uninterrupted Power Supplies", "Fans", "Hair Dryers"}
OUT_OF_SCOPE = "Out of scope"
UNMATCHED = "Unmatched"
# Black Box "Subcategory" values that are branch names, not leaves (ASIN not placed deeper)
GENERIC = {"Home Furnishing", "Home & Décor", "Home Storage & Organisation", "Kitchen & Dining",
           "Home & Kitchen", "Accessories", "Sets", "Stands", "Round", "Clothing", "Small Kitchen Appliances",
           "Kitchen Storage & Containers", "Cooking & Baking Supplies", "Bakeware", "Food Storage", "Containers"}

# ---- rules ------------------------------------------------------------------------------------
# Out of scope: not home & kitchen. First match wins; checked before the in-scope overrides.
HOME_OBJ = (r"\b(?:box|boxes|bowls?|jars?|containers?|trays?|platters?|servers?|storage|stand|holders?|organi[sz]ers?|"
            r"hangers?|covers?|racks?|baskets?|moulds?|molds?|kadai|kadhai|pan|diyas?|candles?|lights?|bottles?|flasks?|mugs?|"
            r"cups?|glass(?:es)?|plates?|dispensers?|bags?|cutters?|maker|juicer|blender|mixer|bedsheets?|pillows?|towels?|"
            r"curtains?|dohar|blankets?|quilts?|cushions?|mats?|rugs?|carpets?|lamps?|frames?)\b")
OUT_RULES = [
    ("clothing", r"\b(?:t-?shirts?|shirts?|kurtas?|kurtis?|sarees?|leggings?|jeans|trousers?|track ?pants?|pyjamas?|"
                 r"nightwear|night suit|innerwear|briefs|boxers|vests?|lingerie|jackets?|hoodies?|sweat ?shirts?|sweaters?|"
                 r"cardigans?|dupattas?|frocks?|beanies?|mufflers?|scarf|scarves|stoles?|socks?|handkerchiefs?|"
                 r"(?<!knee )caps?(?=.*\b(?:baseball|cotton|sun|prayer|men|women|kids)\b))\b", HOME_OBJ),
    ("footwear", r"\b(?:slippers?|chappals?|flip[- ]?flops?|sneakers?|shoes|crocs|clogs|floaters?|sliders?|"
                 r"sandals?(?=.*\b(?:men|women|kids|unisex|size)\b)|shoe(?=.*\b(?:men|women|kids|unisex|size)\b))\b",
                 r"\b(?:rack|stand|cabinet|organi[sz]er|polish|cleaner|brush|bag|cover|shelf|box|dhoop|agarbatti|incense)\b"),
    ("jewellery/accessories", r"\b(?:earrings?|necklaces?|bracelets?|wallets?|purses?|handbags?|sling bags?|sunglasses|"
                 r"wrist ?watch(?:es)?|smart ?watch(?:es)?)\b", r"\b(?:box|stand|organi[sz]er|holder)\b"),
    ("stationery", r"\b(?:pens|pencils?|ball ?point|gel pens?|roller ball pen|ball pen|markers?|highlighters?|crayons?|sketch pens?|"
                   r"erasers?|notebooks?|note ?pads?|diar(?:y|ies)|journals?|sticky notes?|staplers?|geometry box|rulers?|"
                   r"glue sticks?|correction (?:pen|tape)|envelopes?|a4 (?:paper|sheets?)|chart paper|craft paper|"
                   r"colou?ring (?:book|kit|set)|drawing book|sketch ?book|exam pad|clip ?board|calculators?|stationery|"
                   r"poster colou?rs?|water ?colou?rs?|oil pastels?|slime|greeting cards?|gift tags?|rakhis?|rakhee|"
                   r"pencil (?:box|case|pouch))\b|\bpen\b(?=.*\b(?:ink|refill|blue|black|0\.\d ?mm|writing)\b)", None),
    ("electronics accessories", r"\b(?:chargers?|power ?banks?|usb (?:cable|hub|flash drive|drive)|type[- ]?c (?:cable|charger|adapter)|"
                   r"lightning cable|data cable|charging cable|lan cable|ethernet|earphones?|headphones?|earbuds?|headsets?|neckband|"
                   r"tws|bluetooth speaker|speakers?|sound ?bar|pen ?drive|memory card|sd card|micro ?sd|"
                   r"(?:wireless|gaming|optical|bluetooth) mouse|keyboard|mouse ?pad|phone (?:case|cover)|mobile (?:cover|case)|"
                   r"screen (?:guard|protector)|selfie stick|smart ?band|fitness band|batter(?:y|ies)|alkaline|hdmi|"
                   r"router|gamepad|game controller|airpods?)\b", r"\b(?:trap|kill|lamps?|lights?|torch|fan|clock|holder)\b"),
    ("food", r"\b(?:chocolates?|cookies|biscuits|namkeen|sweets|mithai|almonds?|cashews?|raisins|kaju|badam|"
             r"green tea|tea bags?|tea leaves|coffee powder|instant coffee|ready to eat|dry ?fruits?|snacks?)\b", HOME_OBJ),
    ("paper disposables", r"\b(?:facial tissues?|face tissues?|tissues?(?=.*\b(?:pulls|ply|sheets)\b)|toilet (?:paper|rolls?|tissues?)|"
             r"kitchen (?:towels?|rolls?)(?=.*\b(?:paper|pulls?|ply|tissue)\b)|paper (?:napkins?|towels?|plates?|cups?|bowls?|"
             r"glass(?:es)?|straws?)|napkins?(?=.*\b(?:paper|ply|pulls|tissue)\b)|disposable (?:plates?|cups?|glass(?:es)?|bowls?|"
             r"spoons?|cutlery|forks?)|wet wipes|baby wipes|sanitary|diapers?|cotton (?:balls|buds)|ear ?buds|"
             r"areca (?:leaf )?plates?|bagasse)\b", r"\b(?:holder|stand|dispenser|box|case)\b"),
    ("personal care", r"\b(?:face ?wash|body ?wash|bathing soap|tooth ?paste|deodorant|body lotion|lipstick|kajal|"
             r"nail polish|hair oil|sanitary pads?|sunscreen|moisturi[sz]er|face serum)\b", r"\b(?:dispenser|holder|stand|case|dish)\b"),
]
# In-scope overrides: (Amazon leaf, regex). Only used where the model is known to slip; the leaf
# must exist in the label set or the rule is skipped.
LEAF_RULES = [
    ("Pot & Pan Sets", r"\bcookware set\b|\b\d+\s*(?:pc|pcs|piece)s? cookware\b"),
    ("Electric Kettles", r"\belectric (?:tea )?kettle|\bkettle\b.*\b(?:\d{3,4}\s*w|watts?|electric)\b"),
    ("Bucket Mops", r"\bspin mop|\bbucket mop|\bmop\b.*\bbucket\b|\bbucket\b.*\bmop\b"),
    ("Replacement Mop Pads", r"\bmop (?:refill|head|pad)s?\b|\brefill\b.*\bmop\b"),
    ("Wet & Dry Mops", r"\bmops?\b"),
    ("Towel Sets", r"\btowel set\b"),
    ("Jiggers", r"\b(?:peg (?:measure|measurer)|jigger)s?\b"),
    ("Brooms", r"\b(?:broom|jhadu|jhaadu|jharu|jhadoo)s?\b"),
    ("Squeegees", r"\b(?:squeegee|wiper)s?\b(?!.*\b(?:car|blade|windshield)\b)"),
    ("Scrubbers", r"\b(?:steel scrubber|scrub pad|scrubber|scourer|steel wool)s?\b"),
    ("Doormats", r"\bdoor ?mats?\b"),
    ("Waste & Recycling", r"\b(?:dust ?bin|garbage bin|trash can|waste bin|pedal bin)s?\b(?!.*\bbags?\b)"),
    ("Cleaning Gloves", r"\b(?:cleaning|kitchen|rubber|dishwashing|household) gloves?\b"),
    ("Clothes Pegs", r"\bcloth(?:es)? (?:pegs?|clips?|pins?)\b"),
    ("Clotheslines", r"\bcloth(?:es)? ?(?:line|rope|drying rope)s?\b"),
    ("Standard Hangers", r"\b(?:cloth(?:es)?|shirt|coat|plastic|velvet|wooden|saree|kids) hangers?\b|\bhangers? \(?(?:pack|set)"),
    ("Keyrings & Keychains", r"\bkey ?(?:chain|ring)s?\b"),
    ("Combination Padlocks", r"\b(?:number|combination) (?:pad ?)?lock"),
    ("Keyed Padlocks", r"\bpad ?locks?\b"),
    ("Tealight Candle Holders", r"\b(?:tea ?light|t-?light)\s*(?:candle\s*)?holders?\b"),
    ("Tealight Candle Holders", r"\b(?:votive|candle) (?:holders?|stands?)\b"),
    ("Hanging Planters", r"\b(?:plant|pot) hangers?\b|\bhanging (?:planters?|pots?)\b"),
    ("Dustbin Bags", r"\b(?:garbage|dustbin|trash|bin) bags?\b"),
    ("Tea Lights", r"\btea ?light candles?\b|\btealights?\b(?!.*holder)"),
    ("Pressure Cookers", r"\bpressure cooker\b(?!.*\b(?:gasket|whistle|valve|handle)\b)"),
    ("Tawas", r"\b(?:tawa|tava)s?\b"),
    ("Kadhai & Woks", r"\b(?:kadhai|kadai|karahi|kadhais|kadais)\b"),
    ("Sauce Pots & Handis", r"\b(?:handi|patila|pateela|patili|tope|topes|bhagona|degchi)\b"),
    ("Tadka Pans", r"\b(?:tadka|vaghariya)\b"),
    ("Lunch Bags", r"\b(?:tiffin|lunch) bags?\b"),
    ("Lunch Boxes", r"\b(?:tiffin|lunch ?box)(?:es)?\b"),
    ("Serving Casseroles & Tureens", r"\bcasseroles?\b|\bhot ?pot\b|\bhot ?case\b|\bchapati box\b|\broti (?:box|server)"),
    ("Dressing, Seasoning & Spice Dispensers", r"\b(?:masala (?:box|dabba|dani)|spice box|masaladani|anjarai)\b"),
    ("Mixer Grinders", r"\bmixer[- ]?grinder\b|\bmixie\b"),
    ("Hand Blenders", r"\bhand blender\b|\bstick blender\b|\bmathani\b|\bmadhani\b"),
    ("Gas Lighters", r"\bgas lighter\b|\b(?:kitchen|stove) lighter\b"),
    ("Idols & Figurines", r"\b(?:idol|murti|moorti)s?\b"),
    ("Incense Sticks", r"\b(?:agarbatti|agarbathi|incense sticks?)\b"),
    ("Pooja Supplies", r"^(?!.*\b(?:mosquito|repellent|insect)\b).*\b(?:dhoop|sambrani|camphor|pooja samagri|puja samagri|"
                       r"cotton wicks?|kumkum|roli|chandan|havan|hawan|lota|gangajal|kalawa|mauli)\b"),
    ("Standard Pillows", r"^(?!.*\b(?:covers?|cases?|slips?|neck|travel|bedsheets?|sheets?|car|nursing|feeding|cushion)\b).*\bpillows?\b"),
    ("Shower Curtains", r"\bshower curtains?\b(?!.*\b(?:rod|ring)s?\b)"),
    ("Curtains & Drapes", r"^(?!.*\bshower\b)(?!.*\bcurtain (?:lights?|rods?|rings?)\b).*\bcurtains?\b"),
    ("Cutting Boards, Mats and Sets", r"\b(?:chopping|cutting) (?:board|block|mat)s?\b(?!.*\b(?:stand|rack|holder)\b)"),
    ("Storage Container Lids", r"\b(?:glass|steel|spare|replacement|universal) lids?\b|^(?!.*\b(?:container|jar|box|cooker|pan|kadai|kadhai|pot|tope)\b).*\blids?\b"),
    ("LED Bulbs", r"\bled bulbs?\b"),
]


# Product kinds with no Amazon leaf in the pulled data yet: never force a model match.
AWAIT_RULE = (r"\b(?:balloons?|diyas?|deepak|rangoli|gulal|abir|pichkari|fairy lights?|string lights?|led batten|tube ?lights?|"
              r"bandhanwar|ladi|jhalar|kulhad|kulhar|kullad|lantern|bath(?:room)? mugs?|pendant lights?|ceiling lights?|"
              r"hanging lights?|chandeliers?|jhoomar|egg boilers?|curtain\\b.*\\blights?|mixing bowls?|tds|gift (?:box|hamper|set)|hampers?|"
              r"(?:basket|foot|volley|cricket|tennis) ?balls?|rackets?|racquets?|shuttlecocks?|stumps|skipping ropes?)\b")


def _bb_files():
    fs = sorted({f for g in BB_GLOBS for f in glob.glob(g, recursive=True)})
    return [f for f in fs if "Subcategory" in open(f, encoding="utf-8", errors="ignore").readline()]


def load_amazon():
    cols = ["ASIN", "Title", "Brand", "Category", "Subcategory", "ASIN Revenue"]
    ds = []
    for f in _bb_files():
        d = pd.read_csv(f, low_memory=False, usecols=cols)
        d["source"] = "wave1" if "/wave1/" in f else ("sourcing" if "/sourcing/" in f else "brand_run")
        ds.append(d)
    a = pd.concat(ds, ignore_index=True)
    a["revenue"] = pd.to_numeric(a["ASIN Revenue"].astype(str).str.replace(",", ""), errors="coerce")
    a = a.sort_values("revenue", ascending=False).drop_duplicates("ASIN")
    return a.dropna(subset=["Title", "Subcategory"]).reset_index(drop=True)


def keepa_paths():
    best = {}
    for line in open(KEEPA, encoding="utf-8"):
        r = json.loads(line)
        k = _key(r["name"])
        if k not in best or (r.get("productCount") or 0) > best[k][1]:
            best[k] = (r["path"], r.get("productCount") or 0)
    return {k: v[0] for k, v in best.items()}


def _key(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower().replace("é", "e"))


def leaves(a):
    kp = keepa_paths()
    g = a.groupby("Subcategory")
    t = pd.DataFrame({
        "asins": g.size(),
        "revenue": g.revenue.sum().round(0),
        "bb_category": g.Category.agg(lambda s: s.value_counts().index[0]),
    }).reset_index().rename(columns={"Subcategory": "amazon_leaf"})
    t["amazon_path"] = t.amazon_leaf.map(lambda x: kp.get(_key(x), ""))
    t["in_scope"] = (~t.bb_category.isin(OUT_CATS) & ~t.amazon_leaf.str.contains(NON_HOME_LEAVES, case=False)
                     | t.amazon_leaf.isin(IN_LEAVES))
    t["generic"] = t.amazon_leaf.isin(GENERIC) | t.amazon_leaf.isin(set(a.Category))
    t["trained"] = (t.asins >= MIN_TRAIN) & ~t.generic
    return t.sort_values("asins", ascending=False)


# ---- text -------------------------------------------------------------------------------------
def clean(name, brand=""):
    s = str(name or "").lower().replace("&amp;", "&")
    b = str(brand or "").lower().strip()
    if b and b != "nan":
        s = s.replace(b, " ")
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", s) if len(s) > 160 else s
    s = s[:160]
    s = re.sub(r"\d+(?:\.\d+)?\s*(?:ml|l|ltr|litres?|liters?|kg|g|gm|gms|cm|mm|inch|inches|pcs?|pieces?|w|watts?)\b", " ", s)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


def build_model():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.pipeline import make_union
    from sklearn.multiclass import OneVsRestClassifier
    from sklearn.svm import LinearSVC
    vec = make_union(
        TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=2, sublinear_tf=True, max_features=80000),
        TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=3, sublinear_tf=True, max_features=100000),
    )
    return vec, OneVsRestClassifier(LinearSVC(C=0.5), n_jobs=4)


def train(a, lv):
    """Fit on 80%, calibrate confidence and report hold-out accuracy, then refit on all."""
    from sklearn.isotonic import IsotonicRegression
    from sklearn.model_selection import train_test_split
    labs = set(lv.loc[lv.trained, "amazon_leaf"])
    d = a[a.Subcategory.isin(labs)].copy()
    d["text"] = [clean(t, b) for t, b in zip(d.Title, d.Brand)]
    tr, ho = train_test_split(d, test_size=0.2, random_state=0, stratify=d.Subcategory)
    vec, clf = build_model()
    clf.fit(vec.fit_transform(tr.text), tr.Subcategory)
    sc = clf.decision_function(vec.transform(ho.text))
    top = sc.max(1)
    pred = clf.classes_[sc.argmax(1)]
    ok = pred == ho.Subcategory.values
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0, y_max=1).fit(top, ok.astype(float))
    conf = iso.predict(top)
    w = ho.revenue.fillna(0).values
    stats = {
        "train_asins": len(tr), "holdout_asins": len(ho), "leaves": len(labs),
        "holdout_accuracy": ok.mean(), "holdout_accuracy_rev": (w * ok).sum() / w.sum(),
        "holdout_share_above_threshold": (conf >= THRESHOLD).mean(),
        "holdout_accuracy_above_threshold": ok[conf >= THRESHOLD].mean(),
    }
    # top-level check: same Keepa top branch / Black Box category
    cat = lv.set_index("amazon_leaf").bb_category
    stats["holdout_same_bb_category"] = (cat.reindex(pred).values == cat.reindex(ho.Subcategory).values).mean()
    vec, clf = build_model()
    clf.fit(vec.fit_transform(d.text), d.Subcategory)
    return vec, clf, iso, stats


# ---- quick commerce ---------------------------------------------------------------------------
def wave_of_category():
    """Platform category -> extraction wave, via its group (majority wave of that group's brands)."""
    w = pd.read_csv(WAVES)
    gw = w.groupby("group").wave.agg(lambda s: int(s.value_counts().index[0])).to_dict()
    return {c: gw.get(g, 4) for c, g in QCOM_TO_GROUP.items()}


def load_qcom():
    d = pd.read_csv(QCOM_SRC, low_memory=False, dtype={"Product ID": str})
    so = d[d.Date.astype(str).str[:7].isin(["2026-09", "2026-10"])]
    share = so.groupby(["Platform", "Product ID"])["Est. Category Share"].sum().rename("share_sepoct")
    u = d.sort_values("Date").drop_duplicates(["Platform", "Product ID"], keep="last")
    u = u[["Platform", "Product ID", "Product Name", "Category", "Brand"]].merge(
        share.reset_index(), on=["Platform", "Product ID"], how="left")
    u.columns = ["platform", "product_id", "product_name", "platform_category", "brand", "share_sepoct"]
    u["share_sepoct"] = u.share_sepoct.fillna(0)
    return u.reset_index(drop=True)


def assign(u, vec, clf, iso, lv):
    names = u.product_name.fillna("").astype(str)
    leaf = pd.Series("", index=u.index, dtype=object)
    method = pd.Series("", index=u.index, dtype=object)
    conf = pd.Series(np.nan, index=u.index)
    for _, rx, keep in OUT_RULES:
        hit = (method == "") & names.str.contains(rx, case=False, regex=True)
        if keep:
            hit &= ~names.str.contains(keep, case=False, regex=True)
        leaf[hit], method[hit], conf[hit] = OUT_OF_SCOPE, "out_of_scope", 1.0
    wv = u.platform_category.map(wave_of_category()).fillna(4).astype(int)
    hit = (method == "") & names.str.contains(AWAIT_RULE, case=False, regex=True)
    leaf[hit] = np.where(wv[hit] > 1, "Awaiting wave " + wv[hit].astype(str), UNMATCHED)
    method[hit] = "unmatched"
    known = set(lv.amazon_leaf)
    for lab, rx in LEAF_RULES:
        if lab not in known:
            continue
        hit = (method == "") & names.str.contains(rx, case=False, regex=True)
        leaf[hit], method[hit], conf[hit] = lab, "rule", 1.0
    todo = method == ""
    X = vec.transform([clean(n, b) for n, b in zip(names[todo], u.brand[todo])])
    sc = clf.decision_function(X)
    p = clf.classes_[sc.argmax(1)]
    c = iso.predict(sc.max(1))
    conf[todo] = c.round(3)
    leaf[todo] = p
    method[todo] = "model"
    # predicted a non-home leaf -> out of scope
    scope = lv.set_index("amazon_leaf").in_scope
    oos = todo & leaf.map(scope).eq(False) & (conf >= THRESHOLD)
    leaf[oos], method[oos] = OUT_OF_SCOPE, "out_of_scope"
    low = todo & (conf < THRESHOLD)
    leaf[low] = np.where(wv[low] > 1, "Awaiting wave " + wv[low].astype(str), UNMATCHED)
    method[low] = "unmatched"
    u = u.assign(amazon_leaf=leaf, confidence=conf, method=method, wave=wv)
    u["model_guess"] = ""
    u.loc[low, "model_guess"] = p[(conf[todo] < THRESHOLD).values]
    paths = lv.set_index("amazon_leaf").amazon_path
    u["amazon_path"] = u.amazon_leaf.map(paths).fillna("")
    return u


def coverage(u):
    u = u.assign(matched=u.method.isin(["rule", "model"]), oos=u.method.eq("out_of_scope"),
                 awaiting=u.amazon_leaf.str.startswith("Awaiting"))
    rows = []
    for (p, c), g in u.groupby(["platform", "platform_category"]):
        w = g.share_sepoct
        tw = w.sum() or np.nan
        rows.append({"platform": p, "platform_category": c, "group": QCOM_TO_GROUP.get(c, ""), "wave": g.wave.iloc[0],
                     "products": len(g), "matched_pct": g.matched.mean() * 100, "out_of_scope_pct": g.oos.mean() * 100,
                     "awaiting_pct": g.awaiting.mean() * 100, "unmatched_pct": (g.method.eq("unmatched") & ~g.awaiting).mean() * 100,
                     "matched_pct_sepoct_share": (w[g.matched].sum() / tw) * 100,
                     "oos_pct_sepoct_share": (w[g.oos].sum() / tw) * 100,
                     "top_leaf": g.loc[g.matched, "amazon_leaf"].value_counts().index[0] if g.matched.any() else ""})
    return pd.DataFrame(rows).round(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sample", type=int, default=0, help="print N random rule/model matches for a spot check")
    ap.add_argument("--model-cache", help="pickle path: reuse the trained model if present (for rule iteration)")
    args = ap.parse_args()
    a = load_amazon()
    lv = leaves(a)
    lv.to_csv(OUT_LEAVES, index=False)
    print(f"Amazon: {len(a):,} ASINs, {len(lv):,} leaves ({lv.trained.sum()} trained, "
          f"{(lv.amazon_path != '').sum()} with a Keepa path) -> {OUT_LEAVES}")
    import os
    import pickle
    if args.model_cache and os.path.exists(args.model_cache):
        vec, clf, iso, st = pickle.load(open(args.model_cache, "rb"))
    else:
        vec, clf, iso, st = train(a, lv)
        if args.model_cache:
            pickle.dump((vec, clf, iso, st), open(args.model_cache, "wb"))
    print("hold-out:", {k: round(v, 3) if isinstance(v, float) else v for k, v in st.items()})
    u = assign(load_qcom(), vec, clf, iso, lv)
    cols = ["platform", "product_id", "product_name", "platform_category", "brand", "amazon_leaf", "amazon_path",
            "confidence", "method", "model_guess"]
    u[cols].to_csv(OUT_MATCH, index=False)
    cv = coverage(u)
    cv.to_csv(OUT_COVER, index=False)
    print(f"wrote {OUT_MATCH}, {OUT_COVER}")
    w = u.share_sepoct
    for p, g in [("ALL", u)] + list(u.groupby("platform")):
        m = g.method.value_counts(normalize=True).mul(100).round(1).to_dict()
        ws = g.groupby("method").share_sepoct.sum() / g.share_sepoct.sum() * 100
        print(f"{p}: {len(g):,} products; % products {m}; % Sep-Oct share {ws.round(1).to_dict()}")
    aw = u[u.amazon_leaf.str.startswith("Awaiting")].groupby(["amazon_leaf", "platform_category"]).size()
    print("awaiting by platform category (top 25):")
    print(aw.sort_values(ascending=False).head(25).to_string())
    if args.sample:
        s = u[u.method.isin(["rule", "model"])].sample(args.sample, random_state=1)
        for r in s.itertuples():
            print(f"[{r.method} {r.confidence:.2f}] {r.product_name[:80]!r} ({r.platform_category}) -> {r.amazon_leaf}")


if __name__ == "__main__":
    main()

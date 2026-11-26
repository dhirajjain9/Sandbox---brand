# TEKAVO: brand screen

Started 2026-11-26. Group: Home & office furniture. Category: Computer tables, office desks and storage furniture.

Checklist (tick with `python -m pipeline.new_brand stage --key tekavo --done <stage>`):

1. brand_pull: Helium 10 brand pull saved to data/raw/helium10/tekavo/, then `new_brand heroes`
2. competition: Helium 10 peers per main sub-category, keyword paid share, seller feedback
3. history: hero rank / price history, copycats, branded search (pipeline.h10_history_metrics)
4. keepa: Claude in Chrome Keepa run (keepa_chrome_runsheet.md), discount vs list price
5. chrome: Claude in Chrome Step B run (claude_in_chrome_stepB_runsheet.md)
6. scored: inputs filled with pipeline.rescore, report written, dashboard rebuilt

## Keepa and Step B (26 Nov 2026)

- Keepa exports in data/raw/keepa/tekavo/ (renamed in run order; CSV copies with the needed columns).
  10a = 0.568: discount vs list price over 224 live listings weighted by Helium 10 revenue (99.7% of revenue);
  only 12 listings carry the "bought in past month" badge (badge-weighted: TEKAVO 0.645, FFO 0.541). Peers: Desks 0.570,
  Computer Workstations 0.549, Bedside Tables 0.489.
- Step B reviews in data/raw/chrome/tekavo/stepB_part1_reviews.csv. 9a = 0.098 (rating-weighted 1-2 star);
  9b = 0.539 (damaged+defect+missing+wrong / reviews read, pooled; sample leans critical).
- 5d = 10 (FFO Meta ads, all started 13-24 Nov; TEKAVO and Deskio none). 6d = 1,492 (@tekavo 178 + @wudinox 1,314);
  6e = 0.0037 (median likes 3 + 2.5 over combined followers); 6f = 0. 7a = 0, 7d = 0 (Blinkit, Zepto; Instamart not checked).
  10c = 0 (no site-wide sale); 10d = 0.39 (tekavo.in 36%, wudinox.com 48%, weighted 73/27); 12d = 743 (497 + 246).
- Result: NO FIT, 2 of 6 met, blocked at Customer Quality (38.0); 36/49 inputs, 78% weight.

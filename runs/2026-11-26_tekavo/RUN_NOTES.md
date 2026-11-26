# TEKAVO: brand screen

Started 2026-11-26. Group: Home & office furniture. Category: Computer tables, office desks and storage furniture.

Checklist (tick with `python -m pipeline.new_brand stage --key tekavo --done <stage>`):

1. brand_pull: Helium 10 brand pull saved to data/raw/helium10/tekavo/, then `new_brand heroes`
2. competition: Helium 10 peers per main sub-category, keyword paid share, seller feedback
3. history: hero rank / price history, copycats, branded search (pipeline.h10_history_metrics)
4. keepa: Claude in Chrome Keepa run (keepa_chrome_runsheet.md), discount vs list price
5. chrome: Claude in Chrome Step B run (claude_in_chrome_stepB_runsheet.md)
6. scored: inputs filled with pipeline.rescore, report written, dashboard rebuilt

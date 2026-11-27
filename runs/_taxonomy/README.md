# Amazon India category tree (from Keepa)

`keepa_in_tree.jsonl`: one line per Amazon.in browse node under the home-related branches, pulled with
Keepa category_lookup (domain "in"). Fields: catId, name, parent, depth, path, productCount, brandCount,
isBrowseNode, avgBuyBoxPrice, childCategoryIds. `frontier.json`: node IDs still to look up (resume from it).
This tree is the base of our category taxonomy (sub-category = Amazon node; quick commerce and Master File
labels map onto it).

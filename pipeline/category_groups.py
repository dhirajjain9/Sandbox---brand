"""One category taxonomy across Blinkit / Zepto / Instamart (GobbleCube) and the team's Master File.

Used to plan extraction in category waves and to build category views. Group names are ours.
"""
QCOM = {
    "Kitchen & Dining": ["Kitchen & Dining Needs", "Cookware", "Kitchen Tools", "Kitchen Aids", "Steel Utensils", "Pressure Cooker",
                         "Tableware", "Serveware", "Plates Bowls Crockery", "Cutlery & Ladles", "Glasses Cups Mugs", "Drinkware & Bar",
                         "Barware", "Bakeware & Bbq", "Gas Stove & Accessories"],
    "Kitchen Storage & Bottles": ["Kitchen Storage", "Jars Containers Holders", "Bottles Flasks Tiffins", "Lunch Boxes"],
    "Appliances": ["Appliances", "Home Appliances", "Kitchen Appliances", "Personal Care Appliances"],
    "Lighting & Electricals": ["Decorative Lights", "Bulbs & Lights", "Lights & Bulbs", "Extensions & Switches", "Powerbanks Chargers Cables"],
    "Home Decor & Gifting": ["Home Decor", "Festive Gifting", "Festive & Occasion Needs", "Party Essentials"],
    "Pooja": ["Pooja Needs", "Pooja & Worship Needs"],
    "Home Furnishing": ["Home Furnishing", "Linen And Furnishing"],
    "Cleaning & Household": ["Cleaning Tools", "Cleaning Aids", "Kitchen Cleaning", "Garbage Bags", "Tissues & Disposables", "Household Utility"],
    "Bath & Laundry": ["Bathroom Essentials", "Bath & Laundry", "Bathware & Laundry"],
    "Storage & Organisation": ["Storage & Organizers", "Utility & Tools"],
    "Home Improvement & Tools": ["Home Improvement", "Hardware & Fittings"],
    "Gardening": ["Flowers, Plants & Gardening", "Gardening"],
    "Stationery": ["Stationery Needs", "Stationery & Crafts"],
    "Sports & Fitness": ["Sports & Fitness", "Sports & Gym"],
    "Bags, Travel & Apparel": ["Bags", "Travel And Luggage", "Clothing, Footwear & Accessories"],
}
QCOM_TO_GROUP = {c: g for g, L in QCOM.items() for c in L}
MASTER_FILE = {"Kitchenware & Cookware": "Kitchen & Dining", "Appliances": "Appliances", "Home Furnishings": "Home Furnishing",
               "Home Improvement": "Home Improvement & Tools"}

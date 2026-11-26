"""Exclusions applied to the master target list (26 Nov 2026, on the user's instruction).

Excluded: well-known established brands (MNCs, listed companies, large corporates) and brands owned by
roll-ups that will not partner (Mensa, GlobalBees, Upscalio, GOAT Brand Labs). Roll-up ownership is
taken only where a source confirms it; the established list is deliberately conservative.
"""
ROLLUP = {
    "Mensa Brands": ["Pretty Krafts", "PrettyKrafts", "TrustBasket", "Folkulture", "Karagiri", "Dennis Lingo", "Villain", "Helea", "Anubhutee", "Priyaasi", "Hubberholme", "Ishin", "MYFITNESS", "Estalon"],
    "GlobalBees": ["The Better Home", "Yellow Chimes", "Frootle", "Wellspire", "Absorbia", "andMe", "Mush"],
    "Upscalio": ["Hestia"],
    "GOAT Brand Labs": ["Chumbak", "The Label Life", "TrueBrowns", "Frangipani"],
}
ESTABLISHED = [
    # global electronics / appliances / MNC
    "Samsung", "Apple", "Philips", "HP", "Xiaomi", "Bosch", "SanDisk", "Canon", "TP-Link", "Tapo", "Instax", "Midea", "Voltas Beko",
    "Kohler", "Hafele", "IKEA", "NutriBullet", "Hamilton Beach", "PlayStation", "Western Digital", "WD", "Ecovacs", "Eureka Forbes",
    "WD-40", "Mr Muscle", "Reynolds", "Veet", "BIC", "Parker", "Pilot", "Uni-ball", "Faber-Castell", "Camlin", "Speedo", "Adidas",
    "Stanley", "Yonex", "Citizen", "Pierre Cardin", "Tineco", "Coway", "Kuvings", "Instant Brands",
    # Decathlon house brands
    "Decathlon", "Nabaiji", "Domyos", "Quechua", "Kipsta", "Olaian", "Btwin", "Inesis",
    # Indian listed / large corporate brands
    "Prestige", "Judge", "Havells", "Crompton", "Bajaj", "Cello", "Borosil", "La Opala", "Butterfly", "Glen", "Wipro", "Eveready",
    "Safari", "American Tourister", "Skybags", "Aristocrat", "Fastrack", "Raymond", "Jockey", "Campus", "Liberty", "Sparx", "Red Chief",
    "Welspun", "Patanjali", "Aashirvaad", "Classmate", "Cycle", "Goldmedal", "Godrej Cartini", "Godrej Locks", "JK Paper", "Nataraj",
    "Doms", "Linc", "Luxor", "Fevikwik", "Fevicol", "Pitambari", "Cosco", "Nivia", "Vega", "Tynor", "Dr Trust", "Beardo",
    "MuscleBlaze", "boAt", "Bombay Shaving Company", "Mokobara", "Cult", "Sanjeev Kapoor", "FNP", "IGP", "Astrotalk", "Astroyogi",
    "GoMechanic", "Zouk", "Urban Yog",
]

# Brands owned by listed companies (parent in brackets); checked against the kept list on 26 Nov 2026
LISTED = {
    "Pidilite": ["Fevicreate", "Fevibond", "Fevistik", "Dr. Fixit", "Fevikwik", "Fevicol"],
    "ITC": ["Fiama", "Paperkraft", "Classmate", "Aashirvaad"],
    "Hindustan Unilever": ["Lever Ayush", "Cif"],
    "3M": ["3M", "Scotch"],
    "Nestle": ["Nescafe"],
    "Keurig Dr Pepper": ["Snapple"],
    "Strauss Group": ["Strauss"],
    "Newell Brands": ["Contigo"],
    "Vista Outdoor / Revelyst": ["CamelBak"],
    "Amer Sports": ["Wilson"],
    "Carter's": ["Skip Hop"],
    "Lock & Lock (KRX)": ["Lock & Lock"],
    "MRF": ["Funskool"],
    "Reliance Industries": ["Jio"],
    "Palred Technologies": ["pTron"],
    "VIP Industries": ["VIP", "Caprese"],
    "Samsonite": ["Samsonite"],
    "Nike": ["Nike"],
    "PVH": ["Tommy Hilfiger"],
    "Monte Carlo Fashions": ["Monte Carlo"],
    "Provogue (India)": ["Provogue"],
    "Asian Paints": ["Asian Paints"],
    "Foxconn (Belkin)": ["Belkin"],
    "Take-Two Interactive": ["Rockstar Games"],
    "Asahi Kasei": ["Asahi Kasei"],
    "Walton Hi-Tech": ["Walton"],
    "Prism Johnson": ["Johnson Bathware"],
    "Groupe SEB": ["Maharaja"],
    "Mitsubishi Pencil": ["Uni"],
    "Amazon": ["Amazon"],
    "PhysicsWallah": ["Physics Wallah"],
    "GoPro": ["GoPro"],
    "Warner Bros. Discovery": ["Warner Bros."],
    "Electronic Arts": ["EA"],
    "Bandai Namco": ["Bandai Namco"],
    "CD Projekt": ["CD Projekt Red"],
    "Ubisoft": ["Assassin's Creed"],
    "Schneider Electric": ["Schneider", "APC"],
    "De'Longhi": ["Ariete"],
    "Disney (licence)": ["Star Wars"],
    "Warner Bros. Discovery (licence)": ["Harry Potter"],
}
# Large private MNCs / house brands treated as established
ESTABLISHED += ["Amul", "Mars", "Crayola", "Razer", "Solognac", "Forclaz", "Artengo", "Perfly", "Kiprun", "Tarmak", "Oxelo", "Tribord", "Elops"]

# No product fit (user decision, 26 Nov 2026): gaming, computer, phone, audio and car electronics accessories.
# Applied to quick-commerce-only brands; the team's Master File picks are left as they are.
NO_FIT = ["Cosmic Byte", "Kreo", "Evofox", "Ant Esports", "Onelap", "Sounce", "Ausha", "Ailkin", "ajjas", "Tygot", "Dubstep",
          "Digitek", "Boult", "Hammer", "CMF", "Pebble", "OnePlus", "Asus", "Amkette", "Stuffcool", "Urbn", "Gizmore", "Flix",
          "Lapcare", "Bestor", "Nu Republic", "Grand Pitstop"]

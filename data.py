RARITIES = {
    "Trash": {"weight": 28.0},
    "Common": {"weight": 20.0},
    "Uncommon": {"weight": 18.0},
    "Unusual": {"weight": 15.0},
    "Rare": {"weight": 10.0},
    "Legendary": {"weight": 4.5},
    "Mythical": {"weight": 2.5},
    "Exotic": {"weight": 1.0},
    "Secret": {"weight": 0.45},
    "Divine Secret": {"weight": 0.05},
}

LOCATIONS = {
    "Moosewood": {
        "theme": "bg-blue-900 text-white",
        "fish_data": {
            "Trash": [],
            "Common": ["Anchovy", "Bream", "Largemouth Bass", "Red Snapper", "Sockeye Salmon", "Trout"],
            "Uncommon": ["Carp", "Goldfish", "Yellowfin Tuna"],
            "Unusual": ["Eel", "Flounder", "Pike", "Snook"],
            "Rare": [],
            "Legendary": ["Whiptail Catfish"],
            "Mythical": ["Whisker Bill"],
            "Exotic": ["Treble Bass"],
            "Secret": [],
            "Divine Secret": ["Cataclysm Carp"],
        },
    },
    "Roslit Bay": {
        "theme": "bg-teal-900 text-white",
        "fish_data": {
            "Trash": ["Translator Core"],
            "Common": ["Chub", "Minnow", "Pearl", "Perch"],
            "Uncommon": ["Blue Tang", "Butterflyfish", "Clownfish", "Pumpkinseed"],
            "Unusual": ["Angelfish", "Clam", "Gilded Pearl", "Ribbon Eel", "Rose Pearl", "Squid", "Yellow Boxfish"],
            "Rare": ["Alligator Gar", "Arapaima", "Mauve Pearl", "Suckermouth Catfish"],
            "Legendary": ["Axolotl", "Deep Pearl", "Dumbo Octopus"],
            "Mythical": ["Aurora Pearl", "Manta Ray", "Reef Triggerfish"],
            "Exotic": ["Golden Sea Pearl"],
            "Secret": [],
            "Divine Secret": ["Aetherfin"],
        },
    },
    "Desolate Deep": {
        "theme": "bg-black text-cyan-400",
        "fish_data": {
            "Trash": ["String"],
            "Common": ["Horseshoe Crab", "Slate Tuna"],
            "Uncommon": ["Phantom Ray"],
            "Unusual": ["Cockatoo Squid", "Coral Geode", "Rockstar Hermit Crab"],
            "Rare": ["Banditfish"],
            "Legendary": ["Barbed Shark", "Midnight Axolotl"],
            "Mythical": ["Emperor Jellyfish", "Sea Mine"],
            "Exotic": ["Blue Galapagos Octopus"],
            "Secret": ["Grandpa Horseshoe Crab"],
            "Divine Secret": ["Lumilotl"],
        },
    },
    "Castaway Cliffs": {
        "theme": "bg-amber-900 text-white",
        "fish_data": {
            "Trash": [],
            "Common": ["Clowned Triggerfish", "Flamekissed Hawkfish"],
            "Uncommon": ["Cobalt Angelfish", "Mandarinfish"],
            "Unusual": ["Trevally"],
            "Rare": ["Warty Frogfish"],
            "Legendary": ["Hidden Pipefish"],
            "Mythical": ["Mirage Toadfish"],
            "Exotic": ["Scalloped Hammerhead"],
            "Secret": ["Great Goldcursed Shark"],
            "Divine Secret": ["Razorfin"],
        },
    },
    "Sunstone Island": {
        "theme": "bg-yellow-900 text-white",
        "fish_data": {
            "Trash": ["Communication Circuit"],
            "Common": ["Glassfish", "Sweetfish"],
            "Uncommon": ["Chinfish", "Longtail Bass", "Red Tang"],
            "Unusual": ["Trumpetfish"],
            "Rare": ["Mahi Mahi", "Napoleonfish"],
            "Legendary": ["Ancient Wood", "Sunfish", "Wiifish"],
            "Mythical": ["Voltfish"],
            "Exotic": ["Speed Core", "Tartaruga"],
            "Secret": [],
            "Divine Secret": ["Crustal Colossus"],
        },
    },
    "Lost Jungle": {
        "theme": "bg-emerald-950 text-white",
        "fish_data": {
            "Trash": [],
            "Common": ["Cardinal Tetra", "Neon Tetra"],
            "Uncommon": ["Bronze Corydoras"],
            "Unusual": ["Freshwater Pacu", "Oscar Cichlid"],
            "Rare": ["Black Ghost Knifefish", "Northern Snakehead", "Payara", "Redeye Piranha", "Silver Arowana"],
            "Legendary": ["Electric Eel", "Piraiba", "Pirarucu"],
            "Mythical": ["Goliath Tigerfish", "Motoro Stingray"],
            "Exotic": ["Mossjaw"],
            "Secret": ["Elder Mossjaw"],
            "Divine Secret": ["Paradox Piranha"],
        },
    },
}

LOCATION_IMAGES = {
    "Moosewood": "Moosewood.png",
    "Roslit Bay": "Roslit_Bay.png",
    "Desolate Deep": "DesolatePocket.png",
    "Castaway Cliffs": "Castaway_Cliffs.png",
    "Sunstone Island": "Sunstone_Island.png",
    "Lost Jungle": "LostJungle.png",
}

RARITY_VALUES = {
    "Trash": 2,
    "Common": 12,
    "Uncommon": 30,
    "Unusual": 75,
    "Rare": 200,
    "Legendary": 750,
    "Mythical": 3500,
    "Exotic": 15000,
    "Secret": 45000,
    "Divine Secret": 150000,
}

RODS = {
    "Flimsy Rod": {"cost": 0, "luck": 0, "coin_mult": 1.0},
    "Plastic Rod": {"cost": 2500, "luck": 15, "coin_mult": 1.1},
    "Carbon Rod": {"cost": 18000, "luck": 35, "coin_mult": 1.25},
    "Steady Rod": {"cost": 85000, "luck": 60, "coin_mult": 1.5},
    "Trident Rod": {"cost": 450000, "luck": 110, "coin_mult": 2.0},
    "Rod of the Depths": {"cost": 2000000, "luck": 180, "coin_mult": 2.75},
    "Heaven's Rod": {"cost": 10000000, "luck": 275, "coin_mult": 4.0},
}

ROD_UPGRADE_TIERS = {
    1: {"cost_mult": 0.4, "bonus_luck": 15, "bonus_coin_mult": 0.15},
    2: {"cost_mult": 0.9, "bonus_luck": 35, "bonus_coin_mult": 0.35},
    3: {"cost_mult": 1.8, "bonus_luck": 60, "bonus_coin_mult": 0.60},
    4: {"cost_mult": 3.5, "bonus_luck": 95, "bonus_coin_mult": 1.00},
    5: {"cost_mult": 6.0, "bonus_luck": 150, "bonus_coin_mult": 1.50},
}

BAITS = {
    "Worm": {"cost": 150, "bundle": 10, "luck": 15},
    "Bagel": {"cost": 600, "bundle": 10, "luck": 30},
    "Magnet": {"cost": 3500, "bundle": 10, "luck": 55},
    "Squid": {"cost": 12000, "bundle": 10, "luck": 85},
    "Truffle Worm": {"cost": 75000, "bundle": 5, "luck": 250},
}

SPECIAL_UPGRADES = {
    "fish_radar": {
        "name": "Fish Radar",
        "cost": 25000,
        "type": "permanent",
        "desc": "Reveals exact fish rarity drop odds at your selected fishing location.",
    },
    "aurora_totem": {
        "name": "Aurora Totem (10 Casts)",
        "cost": 500000,
        "type": "consumable",
        "desc": "Summons an Aurora Borealis for 10 casts, multiplying total Luck by 5x.",
    },
    "enchant_relic": {
        "name": "Enchant Relic",
        "cost": 150000,
        "type": "consumable",
        "desc": "Applies a random enchantment (Blessed, Greedy, Abyssal, or Divine) to your rod.",
    },
}

ENCHANTMENTS = {
    "Blessed": {"luck": 40, "coin_mult": 0.0},
    "Greedy": {"luck": 0, "coin_mult": 0.5},
    "Abyssal": {"luck": 25, "coin_mult": 0.35},
    "Divine": {"luck": 75, "coin_mult": 0.25},
}

# The Fischhood — Fishing RNG & Progression Tracker (By Ryan)

THis is a full-stack web application inspired by Roblox *Fisch*, built with Python, Flask, SQLAlchemy, and Tailwind CSS. Players explore 6 distinct islands, roll across a 10-tier rarity system (Trash to Divine Secret), upgrade rods with enchantments, and complete daily quests with tracking system.

**Live Demo:** https://the-fischhood.onrender.com

## Key Features
- **6 Distinct Fishing Locations:** Moosewood, Roslit Bay, Desolate Deep, Castaway Cliffs, Sunstone Island, and Lost Jungle, each with custom fish pools and dyanamic location decorations.
- **10-Tier Rarity & Luck Engine:** This is a weighted probability (RNG) that drop odds across Trash, Common, Uncommon, Unusual, Rare, Legendary, Mythical, Exotic, Secret, and Divine Secret tiers based on rod stats, upgrades, bait, enchantments, and Aurora Totem multipliers.
- **Shop & Gear Progression:** 7 purchasable rods, 5-tier rod upgrades (+1 to +5), consumable baits, Fish Radar (helps with live drop rates for each fish), Enchantments, and Aurora Totems.
- **Daily Quests & Catch Log:** Automated daily quest generation, progress tracking, and persistent catch history for each user.

## Tech Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy, Gunicorn
- **Database:** SQLite
- **Frontend:** HTML5, Jinja2, Tailwind CSS
- **Deployment:** Render, GitHub

## Local Setup
```bash
git clone [https://github.com/Ryan090909/fisch-progress-tracker.git](https://github.com/Ryan090909/fisch-progress-tracker.git)
cd fisch-progress-tracker
pip install -r requirements.txt
python app.py

import os
import random
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, CatchLog, DailyQuest
from data import (
    RARITIES,
    LOCATIONS,
    LOCATION_IMAGES,
    RARITY_VALUES,
    RODS,
    ROD_UPGRADE_TIERS,
    BAITS,
    SPECIAL_UPGRADES,
    ENCHANTMENTS,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fischhood-super-secret-key")

os.makedirs(app.instance_path, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(app.instance_path, 'fisch.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

QUEST_POOL = [
    {"type": "rarity", "target": "Rare", "count": 4, "reward": 15000, "desc": "Catch 4 Rare fish"},
    {"type": "rarity", "target": "Legendary", "count": 2, "reward": 50000, "desc": "Catch 2 Legendary fish"},
    {"type": "rarity", "target": "Secret", "count": 1, "reward": 120000, "desc": "Catch 1 Secret fish"},
    {"type": "divine_secret", "target": "Divine Secret", "count": 1, "reward": 500000, "desc": "Catch 1 Divine Secret fish"},
]


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)


def get_player_stats(user):
    rod_data = RODS.get(user.equipped_rod, RODS["Flimsy Rod"])
    upgrade_data = ROD_UPGRADE_TIERS.get(user.rod_level, {"bonus_luck": 0, "bonus_coin_mult": 0.0})
    enchant_data = ENCHANTMENTS.get(user.rod_enchant, {"luck": 0, "coin_mult": 0.0})
    bait_luck = BAITS[user.equipped_bait]["luck"] if (user.equipped_bait and user.bait_count > 0) else 0

    total_luck = rod_data["luck"] + upgrade_data["bonus_luck"] + bait_luck + enchant_data["luck"]
    if user.aurora_casts_left > 0:
        total_luck *= 5

    total_coin_mult = round(
        rod_data["coin_mult"] + upgrade_data["bonus_coin_mult"] + enchant_data["coin_mult"], 2
    )
    return total_luck, total_coin_mult


def get_upgrade_cost(user):
    if user.rod_level >= 5:
        return None
    next_level = user.rod_level + 1
    base_cost = max(RODS[user.equipped_rod]["cost"], 1000)
    return int(base_cost * ROD_UPGRADE_TIERS[next_level]["cost_mult"])


def get_or_create_daily_quest(user):
    today = date.today()
    quest = DailyQuest.query.filter_by(user_id=user.id, date_assigned=today).first()
    if not quest:
        template = random.choice(QUEST_POOL)
        quest = DailyQuest(
            user_id=user.id,
            description=template["desc"],
            quest_type=template["type"],
            target_value=template["target"],
            target_count=template["count"],
            reward_coins=template["reward"],
            date_assigned=today,
        )
        db.session.add(quest)
        db.session.commit()
    return quest


def update_quest_progress(user, fish_name, rarity):
    quest = get_or_create_daily_quest(user)
    if quest.completed:
        return

    matched = (
        (quest.quest_type == "rarity" and rarity == quest.target_value)
        or (quest.quest_type == "specific_fish" and fish_name == quest.target_value)
        or (quest.quest_type == "divine_secret" and rarity == "Divine Secret")
    )

    if matched:
        quest.current_count += 1
        if quest.current_count >= quest.target_count:
            quest.completed = True
            user.coins += quest.reward_coins
            flash(f"Daily Quest Complete! +{quest.reward_coins:,} coins!", "success")
        db.session.commit()


def compute_weights(fish_data, total_luck):
    available_rarities = [r for r, fish_list in fish_data.items() if fish_list]
    luck_factor = 1.0 + (total_luck / 100.0)
    weights = []
    for r in available_rarities:
        base_w = RARITIES[r]["weight"]
        weights.append(base_w if r in ("Trash", "Common") else base_w * luck_factor)
    return available_rarities, weights


def get_location_odds(location_name, total_luck):
    fish_data = LOCATIONS[location_name]["fish_data"]
    rarities, weights = compute_weights(fish_data, total_luck)
    total_w = sum(weights)
    return {r: round((w / total_w) * 100, 2) for r, w in zip(rarities, weights)}


def roll_catch(location_name, total_luck):
    fish_data = LOCATIONS[location_name]["fish_data"]
    rarities, weights = compute_weights(fish_data, total_luck)
    caught_rarity = random.choices(rarities, weights=weights, k=1)[0]
    caught_fish_name = random.choice(fish_data[caught_rarity])
    return caught_fish_name, caught_rarity


@app.route("/")
def index():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    selected_location = request.args.get("location")
    if selected_location not in LOCATIONS:
        selected_location = next(iter(LOCATIONS.keys()))

    total_luck, total_coin_mult = get_player_stats(user)
    radar_odds = get_location_odds(selected_location, total_luck) if user.has_radar else None
    daily_quest = get_or_create_daily_quest(user)
    catches = CatchLog.query.filter_by(user_id=user.id).order_by(CatchLog.id.desc()).limit(20).all()

    return render_template(
        "index.html",
        user=user,
        locations=LOCATIONS,
        location_images=LOCATION_IMAGES,
        selected_location=selected_location,
        total_luck=total_luck,
        total_coin_mult=total_coin_mult,
        radar_odds=radar_odds,
        catches=catches,
        daily_quest=daily_quest,
        rarity_values=RARITY_VALUES,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        action = request.form.get("action")

        if not username:
            flash("Please enter a username.", "error")
            return redirect(url_for("login"))

        existing_user = User.query.filter(db.func.lower(User.username) == username.lower()).first()

        if action == "register":
            if existing_user:
                flash(f"Username '{username}' is already taken! Pick another one.", "error")
                return redirect(url_for("login"))
            new_user = User(username=username)
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.id
            return redirect(url_for("index"))

        elif action == "login":
            if not existing_user:
                flash(f"No account found for '{username}'. Click 'Create Account' instead.", "error")
                return redirect(url_for("login"))
            session["user_id"] = existing_user.id
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/fish", methods=["POST"])
def fish():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    location_name = request.form.get("location")
    if location_name not in LOCATIONS:
        location_name = next(iter(LOCATIONS.keys()))

    total_luck, total_coin_mult = get_player_stats(user)

    if user.equipped_bait and user.bait_count > 0:
        user.bait_count -= 1
        if user.bait_count == 0:
            user.equipped_bait = None

    if user.aurora_casts_left > 0:
        user.aurora_casts_left -= 1

    caught_fish_name, caught_rarity = roll_catch(location_name, total_luck)
    coins_earned = int(RARITY_VALUES[caught_rarity] * total_coin_mult)
    user.coins += coins_earned

    log_entry = CatchLog(
        user_id=user.id,
        fish_name=caught_fish_name,
        rarity=caught_rarity,
        coins_earned=coins_earned,
    )
    db.session.add(log_entry)
    update_quest_progress(user, caught_fish_name, caught_rarity)
    db.session.commit()

    flash(f"Caught {caught_fish_name} ({caught_rarity}) for +{coins_earned:,} coins!", "success")
    return redirect(url_for("index", location=location_name))


@app.route("/shop")
def shop():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    return render_template(
        "shop.html",
        user=user,
        rods=RODS,
        baits=BAITS,
        special_upgrades=SPECIAL_UPGRADES,
        upgrade_cost=get_upgrade_cost(user),
    )


@app.route("/shop/buy_rod/<rod_name>", methods=["POST"])
def buy_rod(rod_name):
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    rod = RODS.get(rod_name)
    if rod and user.coins >= rod["cost"] and user.equipped_rod != rod_name:
        user.coins -= rod["cost"]
        user.equipped_rod = rod_name
        user.rod_level = 0
        user.rod_enchant = None
        db.session.commit()
        flash(f"Purchased {rod_name}!", "success")
    else:
        flash("Cannot purchase this rod.", "error")
    return redirect(url_for("shop"))


@app.route("/shop/upgrade_rod", methods=["POST"])
def upgrade_rod():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    cost = get_upgrade_cost(user)
    if cost is None:
        flash("Your rod is already at the maximum Level 5 (+5)!", "error")
    elif user.coins < cost:
        flash(f"Not enough coins! Need {cost:,} coins.", "error")
    else:
        user.coins -= cost
        user.rod_level += 1
        db.session.commit()
        flash(f"Upgraded {user.equipped_rod} to +{user.rod_level}!", "success")
    return redirect(url_for("shop"))


@app.route("/shop/buy_bait/<bait_name>", methods=["POST"])
def buy_bait(bait_name):
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    bait = BAITS.get(bait_name)
    if bait and user.coins >= bait["cost"]:
        user.coins -= bait["cost"]
        if user.equipped_bait == bait_name:
            user.bait_count += bait["bundle"]
        else:
            user.equipped_bait = bait_name
            user.bait_count = bait["bundle"]
        db.session.commit()
        flash(f"Bought {bait['bundle']}x {bait_name}!", "success")
    else:
        flash("Not enough coins for that bait!", "error")
    return redirect(url_for("shop"))


@app.route("/shop/buy_special/<item_key>", methods=["POST"])
def buy_special(item_key):
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    item = SPECIAL_UPGRADES.get(item_key)
    if not item or user.coins < item["cost"]:
        flash("Not enough coins!", "error")
        return redirect(url_for("shop"))

    if item_key == "fish_radar" and not user.has_radar:
        user.coins -= item["cost"]
        user.has_radar = True
        flash("Purchased Fish Radar!", "success")
    elif item_key == "aurora_totem":
        user.coins -= item["cost"]
        user.aurora_casts_left += 10
        flash("Aurora Totem activated for 10 casts!", "success")
    elif item_key == "enchant_relic":
        user.coins -= item["cost"]
        user.rod_enchant = random.choice(list(ENCHANTMENTS.keys()))
        flash(f"Rod enchanted with {user.rod_enchant}!", "success")

    db.session.commit()
    return redirect(url_for("shop"))


if __name__ == "__main__":
    app.run(debug=True)

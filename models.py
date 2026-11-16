from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    coins = db.Column(db.Integer, default=100)

    # Rod & Upgrade Tracking
    equipped_rod = db.Column(db.String(50), default="Flimsy Rod")
    rod_level = db.Column(db.Integer, default=0)  # Max 5
    rod_enchant = db.Column(db.String(50), default=None)

    # Bait & Special Items
    equipped_bait = db.Column(db.String(50), default=None)
    bait_count = db.Column(db.Integer, default=0)
    has_radar = db.Column(db.Boolean, default=False)
    aurora_casts_left = db.Column(db.Integer, default=0)

    catches = db.relationship("CatchLog", backref="player", lazy=True)
    quests = db.relationship("DailyQuest", backref="player", lazy=True)


class CatchLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    fish_name = db.Column(db.String(64), nullable=False)
    rarity = db.Column(db.String(32), nullable=False)
    coins_earned = db.Column(db.Integer, nullable=False)


class DailyQuest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    quest_type = db.Column(db.String(32), nullable=False)  # 'rarity', 'specific_fish', 'divine_secret'
    target_value = db.Column(db.String(64), nullable=False)
    target_count = db.Column(db.Integer, default=1)
    current_count = db.Column(db.Integer, default=0)
    reward_coins = db.Column(db.Integer, nullable=False)
    date_assigned = db.Column(db.Date, default=date.today)
    completed = db.Column(db.Boolean, default=False)

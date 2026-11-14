from flask import Flask, render_template, request, url_for, session, redirect
from models import db, User, Fish
from data import LOCATIONS, RARITIES
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fisch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_fisch_key'  # Required for session tracking

db.init_app(app)

with app.app_context():
    db.create_all()

LOCATION_IMAGES = {
    'Moosewood': 'images/Moosewood.png',
    'Roslit Bay': 'images/RoslitFar.png',
    'Desolate Deep': 'images/DesolatePocket.png',
    'Castaway Cliffs': 'images/Castaway_Cliffs.png',
    'Sunstone Island': 'images/Sunstone_Island.png',
    'Lost Jungle': 'images/LostJungle.png'
}

@app.route('/')
def start_screen():
    return render_template('start.html')

@app.route('/set_name', methods=['GET', 'POST'])
def set_name():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            username = "Fisherman"
        
        # Save username in session
        session['username'] = username
        
        # Fetch or create user in the database
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, coins=100)
            db.session.add(user)
            db.session.commit()
            
        return redirect(url_for('game'))
        
    return render_template('name.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    # Retrieve username from session, default to 'Ryan' if accessed directly
    username = session.get('username', 'Ryan')
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, coins=100)
        db.session.add(user)
        db.session.commit()
        
    current_loc = 'Moosewood'
    message = None

    if request.method == 'POST':
        action = request.form.get('action')
        current_loc = request.form.get('destination', 'Moosewood')
        
        if action == 'cast':
            loc_info = LOCATIONS.get(current_loc, LOCATIONS['Moosewood'])
            fish_data = loc_info['fish_data']
            
            valid_rarities = {r: data for r, data in RARITIES.items() if fish_data.get(r)}
            
            if not valid_rarities:
                chosen_fish_name = "Old Boot"
                chosen_rarity = "Trash"
            else:
                rarity_names = list(valid_rarities.keys())
                rarity_weights = [valid_rarities[r]['weight'] for r in rarity_names]
                
                chosen_rarity = random.choices(rarity_names, weights=rarity_weights, k=1)[0]
                available_fish_names = fish_data[chosen_rarity]
                chosen_fish_name = random.choice(available_fish_names)
            
            new_fish = Fish(
                name=chosen_fish_name, 
                rarity=chosen_rarity, 
                location=current_loc, 
                user_id=user.id
            )
            db.session.add(new_fish)
            db.session.commit()
            
            message = f"You caught a {chosen_fish_name} ({chosen_rarity})!"

        elif action == 'sell':
            RARITY_PRICES = {
                'Trash': 2, 'Common': 10, 'Uncommon': 25, 'Unusual': 50,
                'Rare': 100, 'Legendary': 300, 'Mythical': 750,
                'Exotic': 2000, 'Secret': 5000, 'Divine Secret': 15000
            }
            user_fish = Fish.query.filter_by(user_id=user.id).all()
            earned_coins = sum([RARITY_PRICES.get(f.rarity, 10) for f in user_fish])
            
            if earned_coins > 0:
                user.coins += earned_coins
                Fish.query.filter_by(user_id=user.id).delete()
                db.session.commit()
                message = f"Sold all fish for 🪙 {earned_coins} coins!"
            else:
                message = "No fish to sell!"

        elif action == 'clear':
            Fish.query.filter_by(user_id=user.id).delete()
            db.session.commit()
            message = "Inventory cleared!"

    image_filename = LOCATION_IMAGES.get(current_loc, 'images/Moosewood.png')
    bg_image = url_for('static', filename=image_filename)
    inventory_items = [f"{f.name} ({f.rarity})" for f in user.inventory]

    return render_template(
        'index.html', 
        user=user, 
        locations=LOCATIONS.keys(), 
        current_loc=current_loc, 
        bg_image=bg_image, 
        message=message, 
        inventory=inventory_items
    )

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
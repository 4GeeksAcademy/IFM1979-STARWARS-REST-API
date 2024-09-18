"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_people():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200


@app.route('/people/<int:character_id>', methods=['GET'])
def get_person(character_id):
    character = Character.query.get_or_404(character_id)
    return jsonify(character.serialize()), 200


@app.route('/people', methods=['POST'])
def add_person():
    data = request.get_json()
    name = data.get('name')
    species = data.get('species')
    homeworld = data.get('homeworld')
    if not name:
        return jsonify({"msg": "Se necesita que introduzcas un nombre"}), 400
    new_character = Character(name=name, species=species, homeworld=homeworld)
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201


@app.route('/people/<int:character_id>', methods=['DELETE'])
def delete_person(character_id):
    character = Character.query.get_or_404(character_id)
    db.session.delete(character)
    db.session.commit()
    return jsonify({"msg": "Personaje borrado"}), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.get_json()
    name = data.get('name')
    climate = data.get('climate')
    terrain = data.get('terrain')
    population = data.get('population')
    if not name:
        return jsonify({"msg": "Se necesita que introduzcas un nombre"}), 400
    new_planet = Planet(name=name, climate=climate, terrain=terrain, population=population)
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201


@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"msg": "Planet deleted"}), 200


@app.route('/users',methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize()for user in users]), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    current_user_id = 1  
    user = User.query.get_or_404(current_user_id)
    favorites = {
        "characters": [character.serialize() for character in user.favorite_character],
        "planets": [planet.serialize() for planet in user.favorite_planet],
    }
    return jsonify(favorites), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    current_user_id = 1  
    user = User.query.get_or_404(current_user_id)
    character = Character.query.get_or_404(people_id)
    user.favorite_character.append(character)
    db.session.commit()
    return jsonify({"msg": "Personaje añadido a favoritos"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user_id = 1  
    user = User.query.get_or_404(current_user_id)
    planet = Planet.query.get_or_404(planet_id)
    user.favorite_planet.append(planet)
    db.session.commit()
    return jsonify({"msg": "Planeta añadido a favoritos"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(people_id):
    current_user_id = 1  
    user = User.query.get_or_404(current_user_id)
    character = Character.query.get_or_404(people_id)
    if character in user.favorite_character:
        user.favorite_character.remove(character)
        db.session.commit()
        return jsonify({"msg": "Personaje eliminado de favoritos"}), 200
    return jsonify({"msg": "Personaje no encontrado en favoritos"}), 404


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user_id = 1  
    user = User.query.get_or_404(current_user_id)
    planet = Planet.query.get_or_404(planet_id)
    if planet in user.favorite_planet:
        user.favorite_planet.remove(planet)
        db.session.commit()
        return jsonify({"msg": "Planeta borrado de favoritos"}), 200
    return jsonify({"msg": "Planeta no encontrado en favoritos"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
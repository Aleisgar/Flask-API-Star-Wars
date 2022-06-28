"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for,json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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


# ---  ROUTE USER  ---

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    userList = list(map(lambda obj : obj.serialize(),users))
    response_body = {
        "msg": userList
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def show_users(user_id):
    userId = User.query.get(user_id)
    print(userId)
    return jsonify(userId.serialize()), 200

@app.route('/user', methods=['POST'])   
def create_new_user():
    body = json.loads(request.data)
    new_user = User(username=body["username"], email=body["email"],password=body["password"])
    db.session.add(new_user)
    db.session.commit()
    response_body={
        "msg": ("user created",new_user)
    }
    return jsonify(response_body,200)

# ---  ROUTE FAVORITES  ---    

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id =user_id)
    favoritesList = list(map(lambda obj : obj.serialize(),favorites))
    response_body = {
        "msg": ("These are your favorite items:",favoritesList)
    }
    return jsonify(response_body),200
    

@app.route('/user/<int:user_id>', methods=['POST'])   
# Porque puedo poner una ruta de usuario diferente al usuario del objeto
def new_favorite(user_id):
    body=json.loads(request.data)
    print(body)
    favorite_item = Favorites(name=body["name"], user_id =body ["user_id"])   
    db.session.add(favorite_item)
    db.session.commit()
    response_body={
        "msg": ("favorite added")
    }
    return jsonify(response_body,200)


@app.route('/user/<int:user_id>/favorites/<int:favorites_id>', methods=['DELETE'])
def delete_favorites(user_id,favorites_id):
    favorite = Favorites.query.filter_by(id = favorites_id).all()
    print(favorite)
    db.session.delete(favorite[0])
    db.session.commit()
    response_body = {
        "msg": "Your favorite item has been deleted!"
    }
    return jsonify(response_body),200    

# ---  ROUTE CHARACTER AND PLANET  ---    

@app.route('/character', methods=['GET'])
def get_character_list():
    characters = Character.query.all()
    character_list = list(map(lambda obj : obj.serialize(),characters))
    # Como character no es un objeto no se puede serializar, 
    # para eso es necesario mapearlo y extraer cada objeto del list para serializarlo
    print(character_list)
    response_body = {
        "msg": character_list
    }
    return jsonify(response_body), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def show_character(character_id):
    characterId = Character.query.get(character_id)
    print(characterId)
    return jsonify(characterId.serialize()), 200   


@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all()
    planet_list = list(map(lambda obj : obj.serialize(),planets))
    # Como character no es un objeto no se puede serializar, 
    # para eso es necesario mapearlo y extraer cada objeto del list para serializarlo
    print(planet_list)
    response_body = {
        "msg": planet_list
    }
    return jsonify(response_body), 200   

@app.route('/planet/<int:planet_id>', methods=['GET'])
def show_planet(planet_id):
    planetId = Planet.query.get(planet_id)
    print(planetId)
    return jsonify(planetId.serialize()), 200    

 

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

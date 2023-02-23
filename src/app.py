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
from models import db, User, People, Planet, Favorites
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
    user = User.query.all()
    list_user = list(map(lambda usuario : usuario.serialize(), user))
    print(list_user)
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "list_user":list_user
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>',methods=['GET'])
def get_usuario(user_id):
    usuario = User.query.filter_by(id=user_id).first()
    print(usuario.serialize())
  

    return jsonify(usuario.serialize()), 200


#@app.route('/favorites', methods=['GET'])
#def handle_hello():
#    favorites = Favorites.query.all()
#    list_favorites = list(map(lambda favorito : favorito.serialize(), favorites))
#    print(list_favorites)
#    response_body = {
#        "msg": "Hello, this is your GET /favorites response ",
#        "list_favorites":list_favorites
#    }

#    return jsonify(response_body), 200

#@app.route('/favorites/<int:favorites_id>',methods=['GET'])
#def get_favorito(favorites_id):
#    favorito = Favorites.query.filter_by(id=favorites_id).first()
#    print(favorito.serialize())
  

#    return jsonify(favorito.serialize()), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    list_people = list(map(lambda person : person.serialize(), people))
    print(list_people)
    response_body = {
        "msg": "Hello from people",
        "list_people":list_people
    }

    return jsonify(response_body), 200

@app.route('/people/<int:people_id>',methods=['GET'])
def get_person(people_id):
    person = People.query.filter_by(id=people_id).first()
    print(person.serialize())
  

    return jsonify(person.serialize()), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    planet = Planet.query.all()
    list_planet = list(map(lambda planeta : planeta.serialize(), planet))
    print(list_planet)
    response_body = {
        "msg": "Hello from people",
        "list_planet":list_planet
    }

    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>',methods=['GET'])
def get_planeta(planet_id):
    planeta = Planet.query.filter_by(id=planet_id).first()
    print(planeta.serialize())
  

    return jsonify(planeta.serialize()), 200
  
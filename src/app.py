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

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager



app = Flask(__name__)
app.url_map.strict_slashes = False


if __name__ == "__main__":
    app.run()

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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
#from models import Person

#login

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user=User.query.filter_by(email=email).first()
    if user is None: 
        return jsonify({"msg":"No existe el usuario"})
    if email != user.email or password != user.password:
        return jsonify({"msg": "Usuario o contrasena incorrecta"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



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

#[GET]/user

@app.route('/user/<int:user_id>',methods=['GET'])
def get_usuario(user_id):
    usuario = User.query.filter_by(id=user_id).first()
 #   print(usuario.serialize())
    if usuario is None: 
        response_body = {"msg": "No hay Usuario"}
        return response_body, 404
    return jsonify(usuario.serialize()), 200

#[GET]/user/favorites

@app.route('/user/<int:user_id>/favorites',methods=['GET'])
def get_favorites_user(user_id):
    favorites_user = Favorites.query.filter_by(user_id=user_id).all()
    #print(favorites_user.serialize())
    list_of_user_favorite = list(map(lambda favorites: favorites.serialize(), favorites_user))

    return jsonify(list_of_user_favorite), 200




#Favoritos 

@app.route('/favorites/<int:favorites_id>', methods=['GET'])
def get_favorito(favorites_id):
   favorito = Favorites.query.filter_by(id=favorites_id).first()
   #print(favorito.serialize())
  
  # if favorito is None:
  #  response_body = {"msg": "No hay favoritos"}
  #  return jsonify(response_body), 404
    
   return jsonify(favorito.serialize()), 200

#[POST] /favorite/planet/<int:planet_id>

@app.route('/favorites_planet/<int:planet_id>/<int:user_id>',methods=['POST'])
def add_favorites_planet(planet_id,user_id):
    planet_query = Planet.query.get(planet_id)
    favorites_planet = Favorites(user_id=int(user_id), planet_id=int(planet_id))
    db.session.add(favorites_planet)
    db.session.commit()
    response_body = {"msg": "Planeta agregado a favoritos correctamente"}
    
    return jsonify(response_body), 200

#[POST] /favorite/people/<int:people_id>

@app.route('/favorites_people/<int:people_id>/<int:user_id>',methods=['POST'])
def add_favorites_people(people_id,user_id):
    people_query = People.query.get(people_id)
    favorites_people = Favorites(user_id=int(user_id), people_id=int(people_id))
    db.session.add(favorites_people)
    db.session.commit()
    response_body = {"msg": "Persona agregado a favoritos correctamente"}
    
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed

#[GET] /people

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

#[GET] /people/<int:people_id>

@app.route('/people/<int:people_id>',methods=['GET'])
def get_person(people_id):
    person = People.query.filter_by(id=people_id).first()
    print(person.serialize())
  

    return jsonify(person.serialize()), 200

#[GET] /planets

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

# [GET] /planets/<int:planet_id>

@app.route('/planet/<int:planet_id>',methods=['GET'])
def get_planeta(planet_id):
    planeta = Planet.query.filter_by(id=planet_id).first()
    print(planeta.serialize())
  

    return jsonify(planeta.serialize()), 200
  
# [DELETE] /favorite/planet/<int:planet_id>


@app.route('/favorites_planet/<int:planet_id>/<int:user_id>',methods=['DELETE'])
def remove_favorites_planet(planet_id,user_id):
    #planet_query = Planet.query.delete(planet_id)
    favorites_planet = Favorites(user_id=int(user_id), planet_id=int(planet_id))
    db.session.delete(favorites_planet)
#  db.session.delete()
    response_body = {"msg": "Planeta borrado a favoritos correctamente"}
    
    return jsonify(response_body), 200

#[DELETE] /favorite/people/<int:people_id>

#@app.route('/favorites_people/<int:people_id>/<int:user_id>',methods=['DELETE'])
#def delete_favorites_people(people_id,user_id):
    #people_query = Favorites.query.filter(Favorites.user_id == user_id, Favorites.people_id == people_id).first()
    # favorites_people = Favorites(user_id=int(user_id), people_id=int(people_id))
    
    #if people_query != null:
    #    favorites_delete = Favorites(user_id=int(user_id), people_id=int(people_id)
    #    db.session.delete 
   # db.session.delete()
   # response_body = {"msg": "Persona borrada a favoritos correctamente"}
    
   #  return jsonify(response_body), 200

#@app.route('/favorites_people/<int:people_id>/<int:user_id>', methods=['DELETE'])
#def delete_favorites_people(people_id, user_id):
#    people_query = Favorites.query.filter(Favorites.user_id == user_id, Favorites.people_id ==people_id).first()

#    if people_query :
     #   favorites_delete = Favorites(people_query)
     #pasar unaquery al metodo DELETE
#        db.session.delete(people_query)
#        db.session.commit()
#        return jsonify({ "msg":"Favorito eliminado"}),200
#    else:
#        return jsonify({ "msg":"El favorito no existe"}),200

@app.route('/favorites_people/<int:people_id>', methods=['DELETE'])
@jwt_required()
def delete_favorites_persona(people_id):
    user_id = get_jwt_identity()
    people_query = Favorites.query.filter(Favorites.user_id == user_id, Favorites.people_id ==people_id).first()
    if people_query :
     #   favorites_delete = Favorites(people_query)
     #pasar unaquery al metodo DELETE
        db.session.delete(people_query)
        db.session.commit()
        return jsonify({ "msg":"Favorito eliminado"}),200
    else:
        return jsonify({ "msg":"El favorito no existe"}),200

@app.route('/favorites_planet/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_favorites_planeta(planet_id):
    user_id = get_jwt_identity()
    planet_query = Favorites.query.filter(Favorites.user_id == user_id, Favorites.planet_id == planet_id).first()
    if planet_query :
     #   favorites_delete = Favorites(planet_query)
     #pasar unaquery al metodo DELETE
        db.session.delete(planet_query)
        db.session.commit()
        return jsonify({ "msg":"Favorito eliminado"}),200
    else:
        return jsonify({ "msg":"El favorito no existe"}),200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
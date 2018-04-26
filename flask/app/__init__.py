# third-party imports
from flask import Flask
from flask_api import FlaskAPI
from flask import Flask, jsonify, abort, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from functools import wraps
import jwt
import datetime

from instance.config import app_config

from app.models import meals, users, orders, Meal, menu, User, allusers

list_users=[]



NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'






def create_app(config_name):
    from app.models import meals
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"


    def _get_meal(id):
      return [meal for meal in meals if meal['id'] == id]


    def _meal_exists(name):
      return [meal for meal in meals if meal["name"] == name]

    def _get_user(id):
      return [user for user in users if user['id'] == id]


    def _user_exists(email):
      return [user for user in users if user["email"] == email]

    def _get_order(id):
      return [order for order in orders if order[username] == username]



    @app.route('/api/v1/meals', methods=['GET'])
    def get_meals():
        return jsonify({'meals': meals})


    @app.route('/api/v1/meals/<int:id>', methods=['GET'])
    def get_meal(id):
        meal = _get_meal(id)
        if not meal:
            abort(404)
        return jsonify({'meal': meal})

    @app.route('/api/v1/meals', methods=['POST'])
    def create_meal():
        if not request.json or 'name' not in request.json or 'ingredients' not in request.json or 'price' not in request.json:
            abort(400)
        meal_id = meals[-1].get("id") + 1
        name = request.json.get('name')
        ingredients = request.json.get('ingredients')
        if _meal_exists(name):
            abort(400)
        price = request.json.get('price')
        if type(price) is not int:
            abort(400)
        meal = {"id": meal_id, "name": name,
                "ingredients": ingredients,"price": price}
        meals.append(meal)
        return jsonify({'meal': meal}), 201


    @app.route('/api/v1/meals/<int:id>', methods=['PUT'])
    def update_meal(id):
        meal = _get_meal(id)
        if len(meal) == 0:
            abort(404)
        if not request.json:
            abort(400)
        name = request.json.get('name', meal[0]['name'])
        ingredients = request.json.get('ingredients', meal[0]['ingredients'])
        price = request.json.get('price', meal[0]['price'])
        if type(price) is not int:
            abort(400)
        meal[0]['name'] = name
        meal[0]['ingredients'] = ingredients
        meal[0]['price'] = price
        return jsonify({'meal': meal[0]}), 200


    @app.route('/api/v1/meals/<int:id>', methods=['DELETE'])
    def delete_meal(id):
        meal = _get_meal(id)
        if len(meal) == 0:
            abort(404)
        meals.remove(meal[0])
        return jsonify({}), 204


    @app.route('/api/v1/orders', methods=['GET'])
    def get_orders():
        return jsonify({'orders': orders})



    @app.route('/api/v1/menu', methods=['GET'])
    def get_menu():
        return jsonify({'menu': menu})

    @app.route('/api/v1/orders/<username>', methods=['DELETE'])
    def delete_order(username):
        order = _get_order(username)
        if len(username) == 0:
            abort(404)
        orders.remove(order[0])
        return jsonify({}), 204

    
    @app.route('/auth/signup', methods=['POST'])
    def create_user():
        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(user_id=4, username=data['username'], email=data['email'], password=hashed_password, caterer=False)
        list_users.append(new_user)

        return jsonify({'message' : 'New user created!'})

    @app.route('/user/<user_id>', methods=['PUT'])
    def create_admin(user_id):
        user = (item for item in newusers if item['user_id'] == 'user_id').next

        if not user:
            return jsonify({'message' : 'No user found!'})

        user.caterer = True
        caterers=[]
        caterer.append(user)

        return jsonify({'message' : 'The user has been promoted!'})

    def get_by_email(email):
        
        for user in list_users:
            if user.email == email:
                return user

    @app.route('/auth/login')
    def login():
        user = {
                'user_id':3,
                'username': 'Ryan Tedder',
                'email':'tedder@gmail.com',
                'password': 'pass1234',
        }
        if user.get('password') == 'pass1234':
            token = jwt.encode({'user' : user['username'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, app.config['SECRET_KEY'])
            return jsonify({'token' : token.decode('UTF-8')},{'message': 'You have successfully logged in'})
        return make_response('Could not verify!', 401)
    



    
    return app

    
# third-party imports
from flask import Flask
from flask_api import FlaskAPI
from flask import Flask, jsonify, abort, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from functools import wraps
import jwt
import datetime

#local imports
from instance.config import app_config
from app.models import Meal, User


list_users=[]
meals=[]
orders=[]

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'


"""App starts here.. In this case contains routes and functions used in the routes"""
def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"


    #functions used in the routes below
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


    #Route returns list of all meals in database
    @app.route('/api/v1/meals', methods=['GET'])
    def get_meals():
        return jsonify({'meals': meals})

    #Get just one meal using its id
    @app.route('/api/v1/meals/<int:id>', methods=['GET'])
    def get_meal(id):
        meal = _get_meal(id)
        if not meal:
            abort(404)
        return jsonify({'meal': meal})

    #Add meals to list of meals already available
    @app.route('/api/v1/meals', methods=['POST'])
    def create_meal():
        if not request.json or 'name' not in request.json or 'ingredients' not in request.json or 'price' not in request.json:
            abort(400)
        meal_id = request.json.get('id')
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

    #Change values of an already existing meal
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

    #Delete meal using id
    @app.route('/api/v1/meals/<int:id>', methods=['DELETE'])
    def delete_meal(id):
        meal = _get_meal(id)
        if meal:
            del meal
        else:
            return jsonify({'message': 'Meal does not exist'})

    #Get orders from orders list
    @app.route('/api/v1/orders', methods=['GET'])
    def get_orders():
        return jsonify({'orders': orders})

    #Get menu from menu list
    @app.route('/api/v1/menu', methods=['GET'])
    def get_menu():
        return jsonify({'menu': menu})

    #Delete order using the username
    @app.route('/api/v1/orders/<username>', methods=['DELETE'])
    def delete_order(order_id):
        order = _get_order(order_id)
        if order:
            del order
        else:
            return jsonify ({'message': 'Order does not exist'})

    #Endpoint to register user/ sign up
    @app.route('/auth/signup', methods=['POST'])
    def create_user():
        data = request.get_json(force=True)
        caterer = data['caterer'] or False

        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(user_id=4, username=data['username'], email=data['email'], password=hashed_password, caterer=caterer)

        list_users.append(new_user)

        return jsonify({'message' : 'New user created!'}), 201

    #function to enable login
    # @app.route('/user/<user_id>', methods=['PUT'])
    # def create_admin(user_id):
    #     user = (item for item in newusers if item['user_id'] == 'user_id').next

    #     if not user:
    #         return jsonify({'message' : 'No user found!'})

    #     user.caterer = True
    #     caterers=[]
    #     caterer.append(user)

    #     return jsonify({'message' : 'The user has been promoted!'})

    def get_by_email(email):
        
        for user in list_users:
            if user.email == email:
                return user

    #Endpoint for login
    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']


        user = get_by_email(email)
        if user and check_password_hash(user.password, password):
            token = jwt.encode({'user' : user.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, str(app.config['SECRET_KEY']))
            return jsonify({'token' : token.decode('UTF-8'), 'message': 'Login successful!!'}), 200
        return make_response(jsonify({'message':'Invalid email or password, Please try again.'}), 401)
    
    return app

    
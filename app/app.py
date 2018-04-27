"""app.py is mainly used to run the tests"""
#third party imports
from flask_api import FlaskAPI
from flask import Flask, jsonify, abort, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from functools import wraps

#local imports
from app import create_app
from app.models import meals, users, orders, Meal, menu


meals = [
    {
        'id': 1,
        'name': 'Ugali and fish',
        'ingredients': 'Ugali, fish, vegetables, spices',
        'Price': 150,
    },
    {
        'id': 2,
        'name': 'Rice and beef',
        'ingredients': 'Cooked rice, salad, stewed beef',
        'price': 320,
    },
    {
        'id': 3,
        'name': 'Matoke and mutton',
        'ingredients': 'Unripe cooked banana, stew, mutton, appetizer',
        'price': 250,
    },
]

app = Flask(__name__)

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

#functions used in the routes below
def _get_meal(id):
      return [meal for meal in meals if meal['id'] == id]


def _meal_exists(name):
  return [meal for meal in meals if meal["name"] == name]

def _get_user(id):
  return [user for user in users if user['id'] == id]


def _user_exists(email):
  return [user for user in users if user["email"] == email]

def _get_order(order_id):
  return [order for order in orders if order["order_id"] == order_id]

def _order_exists(username):
	return [order for order in orders if order["username"] == username]




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
    if len(meal) == 0:
        abort(404)
    meals.remove(meal[0])
    return jsonify({}), 204

#Get orders from orders list
@app.route('/api/v1/orders', methods=['GET'])
def get_orders():
    return jsonify({'orders': orders})

#Get just one order using order_id
@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = _get_order(order_id)
    if not order:
        abort(404)
    return jsonify({'order': order})

#Add order to list of orders already available
@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    if not request.json or 'username' not in request.json or 'meal' not in request.json or 'quantity' not in request.json:
        abort(400)
    order_id = orders[-1].get("order_id") + 1
    username = request.json.get('username')
    meal = request.json.get('meal')
    if _order_exists(username):
        abort(400)
    quantity = request.json.get('quantity')
    if type(quantity) is not int:
        abort(400)
    order = {"order_id": order_id, "username": username,
            "meal": meal,"quantity": quantity}
    orders.append(order)
    return jsonify({'order': order}), 201

#Change values of an already existing order
@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = _get_order(order_id)
    if len(order) == 0:
        abort(404)
    if not request.json:
        abort(400)
    username = request.json.get('username', order[0]['username'])
    meal = request.json.get('meal', order[0]['meal'])
    quantity = request.json.get('quantity', order[0]['quantity'])
    if type(quantity) is not int:
        abort(400)
    order[0]['username'] = username
    order[0]['meal'] = meal
    order[0]['quantity'] = quantity
    return jsonify({'order': order[0]}), 200

#Delete order using order_id
@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = _get_order(order_id)
    if len(order) == 0:
        abort(404)
    orders.remove(order[0])
    return jsonify({}), 204

#Get menu from menu list
@app.route('/api/v1/menu', methods=['GET'])
def get_menu():
    return jsonify({'menu': menu})

#Endpoint to register user/ sign up
@app.route('/auth/signup', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(user_id=4, username=data['username'], email=data['email'], password=hashed_password, caterer=False)
    list_users.append(new_user)

    return jsonify({'message' : 'New user created!'})

#function to enable login
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

#Endpoint for login
@app.route('/auth/login', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True)
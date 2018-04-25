from flask_api import FlaskAPI
from flask import Flask, jsonify, abort, make_response, request






app = Flask(__name__)

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

from app.models import meals, users, orders, Meal, menu



def _get_meal(id):
      return [meal for meal in meals if meal[id] == id]


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

@app.route('/api/v1/orders', methods=['GET'])
def get_orders():
    return jsonify({'orders': orders})

@app.route('/api/v1/menu', methods=['GET'])
def get_menu():
    return jsonify({'menu': menu})





if __name__ == '__main__':
    app.run(debug=True)

from flask_api import FlaskAPI
from flask import Flask, jsonify, abort, make_response, request
# from flask_sqlalchemy import SQLAlchemy



# from instance.config import app_config

app = Flask(__name__)

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

from app.models import meals

# meals = [
#     {
#         'id': 1,
#         'name': 'Ugali and fish',
#         'ingredients': 'Ugali, fish, vegetables, spices',
#         'Price': 150,
#     },
#     {
#         'id': 2,
#         'name': 'Rice and beef',
#         'ingredients': 'Cooked rice, salad, stewed beef',
#         'price': 320,
#     },
#     {
#         'id': 3,
#         'name': 'Matoke and mutton',
#         'ingredients': 'Unripe cooked banana, stew, mutton, appetizer',
#         'price': 250,
#     },
# ]
def _get_meal(id):
    return [meal for meal in meals if meal[id] == id]


def _meal_exists(name):
    return [meal for meal in meals if meal["name"] == name]




if __name__ == '__main__':
    app.run(debug=True)

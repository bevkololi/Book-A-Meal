from flask_api import FlaskAPI
from flask import Flask, jsonify, abort, make_response, request






app = Flask(__name__)

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

from app.models import meals
from app.models import users


def _get_meal(id):
    return [meal for meal in meals if meal[id] == id]


def _meal_exists(name):
    return [meal for meal in meals if meal["name"] == name]




if __name__ == '__main__':
    app.run(debug=True)

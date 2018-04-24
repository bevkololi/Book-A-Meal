# third-party imports I'll need
from flask import Flask
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort
from flask import Flask, jsonify, abort, make_response, request
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta

from instance.config import app_config

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

def create_app(config_name):
    from app.models import meals
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    def _get_meal(id):
      return [meal for meal in meals if meal['id'] == id]


    def _meal_exists(name):
      return [meal for meal in meals if meal["name"] == name]


    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': NOT_FOUND}), 404)


    @app.errorhandler(400)
    def bad_request(error):
        return make_response(jsonify({'error': BAD_REQUEST}), 400)


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



    return app
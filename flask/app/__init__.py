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



    return app
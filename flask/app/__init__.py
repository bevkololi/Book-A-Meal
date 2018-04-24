# third-party imports
from flask import Flask
from flask_api import FlaskAPI

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
      return [meal for meal in meals if meal[id] == id]


    def _meal_exists(name):
      return [meal for meal in meals if meal["name"] == name]

    def _get_user(id):
      return [user for user in users if user['id'] == id]


    def _user_exists(email):
      return [user for user in users if user["email"] == email]


    
    



    
    return app

    
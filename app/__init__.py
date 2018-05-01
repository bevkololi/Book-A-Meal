from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import Meal
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/v1/meals/', methods=['POST', 'GET'])
    def meals():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            description = str(request.data.get('description', ''))
            price = str(request.data.get('price', ''))
            if price:
            	int(price)
            else:
            	{"message": "Price should be a number" 
         }, 200

            if name:
                meal = Meal(name=name, description=description, price=price)
                meal.save()
                response = jsonify({
                    'id': meal.id,
                    'name': meal.name,
                    'description': meal.description,
                    'price': meal.price
                })
                response.status_code = 201
                return response
        else:
            # GET
            meals = Meal.get_all()
            results = []

            for meal in meals:
                obj = {
                    'id': meal.id,
                    'name': meal.name,
                    'description': meal.description,
                    'price': meal.price
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/api/v1/meals/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def meal_manipulation(id, **kwargs):
     # retrieve a meal using it's ID
        meal = Meal.query.filter_by(id=id).first()
        if not meal:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            meal.delete()
            return {
            "message": "meal {} deleted successfully".format(meal.id) 
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            meal.name = name
            meal.save()
            response = jsonify({
                'id': meal.id,
                'name': meal.name,
                'description': meal.description,
                'price': meal.price
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': meal.id,
                'name': meal.name,
                'description': meal.description,
                'price': meal.price
            })
            response.status_code = 200
            return response

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    


    return app
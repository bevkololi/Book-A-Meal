from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

# local import
from instance.config import app_config


db = SQLAlchemy()

def create_app(config_name):
    from app.models import Meal, User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/v1/meals/', methods=['POST', 'GET'])
    def meals():
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
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

                        return make_response(response), 201

                else:
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

                    return make_response(jsonify(results)), 200
            else:
                response = {
                    'message': 'Please input access token'
                }
                return make_response(jsonify(response)), 401

    @app.route('/api/v1/meals/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def meals_manipulation(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                meal = Meal.query.filter_by(id=id).first()
                if not meal:
                    abort(404)

                if request.method == "DELETE":
                    meal.delete()
                    return {
                        "message": "meal {} deleted".format(meal.id)
                    }, 200
                elif request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    description = str(request.data.get('description', ''))
                    price = str(request.data.get('price', ''))
                    if price:
                        int(price)
                    else:
                        {"message": "Price should be a number" 
                 }, 200
                    meal.name = name
                    meal.description = description
                    meal.price = price
                    meal.save()
                    response = {
                        'id': meal.id,
                        'name': meal.name,
                        'description': meal.description,
                        'price': meal.price
                    }
                    return make_response(jsonify(response)), 200
                else:
                    response = jsonify({
                        'id': meal.id,
                        'name': meal.name,
                        'description': meal.description,
                        'price': meal.price
                    })
                    return make_response(response), 200
            else:
                              
                response = {
                    'message': 'Please input access token'
                }
                return make_response(jsonify(response)), 401

    
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    


    return app
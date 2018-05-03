from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

# local import
from instance.config import app_config

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'


db = SQLAlchemy()

def create_app(config_name):
    from app.models import Meal, User, Order
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': NOT_FOUND}), 404)


    @app.errorhandler(400)
    def bad_request(error):
        return make_response(jsonify({'error': BAD_REQUEST}), 400)


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

    @app.route('/api/v1/orders/', methods=['POST', 'GET'])
    def orders():
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                if request.method == "POST":
                    meal = str(request.data.get('meal', ''))
                    quantity = str(request.data.get('quantity', ''))
                    if meal:
                        order = Order(meal=meal, quantity=quantity, ordered_by=user_id)
                        order.save()
                        response = jsonify({
                            'id': order.id,
                            'meal': order.meal,
                            'time_ordered': order.time_ordered,
                            'quantity': order.quantity,
                            'ordered_by': user_id
                        })

                        return make_response(response), 201

                else:
                    orders = Order.get_all()
                    results = []

                    for order in orders:
                        obj = {
                            'id': order.id,
                            'meal': order.meal,
                            'time_ordered': order.time_ordered,
                            'quantity': order.quantity,
                            'ordered_by': user_id
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/api/v1/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def order_manipulation(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                order = Order.query.filter_by(id=id).first()
                if not order:
                    abort(404)

                if request.method == "DELETE":
                    order.delete()
                    return {
                        "message": "order {} deleted".format(order.id)
                    }, 200
                elif request.method == 'PUT':
                    meal = str(request.data.get('meal', ''))
                    quantity = str(request.data.get('quantity', ''))
                    order.meal = meal
                    order.quantity = quantity
                    order.save()
                    response = {
                        'id': order.id,
                        'meal': order.meal,
                        'time_ordered': order.time_ordered,
                        'quantity': order.quantity,
                        'ordered_by': user_id
                    }
                    return make_response(jsonify(response)), 200
                else:
                    # GET
                    response = jsonify({
                        'id': order.id,
                        'meal': order.meal,
                        'time_ordered': order.time_ordered,
                        'quantity': order.quantity,
                        'ordered_by': user_id
                })
                    return make_response(response), 200
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    


    return app
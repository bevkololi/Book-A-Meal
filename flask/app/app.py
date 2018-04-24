from flask_api import FlaskAPI
from flask import Flask, jsonify, abort, make_response, request

from app.models import meals


app = Flask(__name__)

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'


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



if __name__ == '__main__':
    app.run(debug=True)

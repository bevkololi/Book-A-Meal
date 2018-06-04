from . import auth_blueprint

from flask_restful import Resource, Api
from flask import Blueprint, make_response, request, jsonify
from app.models import User


class RegistrationView(Resource):
    """This class-based view registers a new user."""

    def post(self):
        # Query to see if the user already exists
        try:
            post_data = request.get_json(force=True)
            username = post_data['username']
            email = post_data['email']
            password = post_data['password']

            user = User.query.filter_by(email=email).first()

            if not user:
                # Register the user
                user = User(email=email, password=password, username=username)
                user.save()

                return {'message': 'You registered successfully. Please login.'}, 201
            else:
                return {'message': 'User already exists. Please login.'}, 202
        except Exception as e:
            return {'message': 'Registration not successful', 'error':str(e)}, 400

class LoginView(Resource):
    """This class-based view handles user login and access token generation."""

    def post(self):
        try:
            post_data = request.get_json(force=True)
            username = post_data['username']
            email = post_data['email']
            password = post_data['password']

            user = User.query.filter_by(email=email).first()

            if user and user.password_is_valid(password):
                # Generate the access token
                access_token = user.generate_token(user.id)
                if access_token:
                    return {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }, 200
            else:
                # User does not exist
                return {
                    'message': 'Invalid email or password, Please try again.'
                }, 401

        except Exception as e:
            return {
                'error': str(e),
                'message': 'login unsuccessful'
            }, 400


AUTH = Blueprint('app.auth.views', __name__)
API =Api(AUTH)
# Define the API resource
API.add_resource(RegistrationView, '/auth/signup', endpoint='signup')
API.add_resource(LoginView, '/auth/login', endpoint='login')

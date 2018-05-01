from app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta


class User(db.Model):
    """This class defines the users table """

    __tablename__ = 'users'

    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    

    def __init__(self, email, password):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """Generates the access token to be used as the Authorization header"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"


class Meal(db.Model):
    """This class defines the bucketlist table."""

    __tablename__ = 'meals'

    # define the columns of the table, starting with its primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    price = db.Column(db.Integer())
    

    def __init__(self, name, price, description):
        """Initialize the bucketlist with a name and its creator."""
        self.name = name
        self.description = description
        self.price = price
        

    def save(self):
        """Save a meal.
        This applies for both creating a new bucketlist
        and updating an existing onupdate
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Meal.query.all()

    

    def delete(self):
        """Deletes a given meal."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Return a representation of a meal instance."""
        return "<Meal: {}>".format(self.meal)

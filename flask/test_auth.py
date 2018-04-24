from copy import deepcopy
import unittest
import json

from app import app
from app.models import user1

class AuthTestCase(unittest.TestCase):
    """Test case for the authentication of users"""

    def setUp(self):
        """Set up test variables."""
        self.backup_users = deepcopy(app.users)
        self.app = app.app.test_client()
        self.app.testing = True
        self.user_data = {
            'email': 'bev@gmail.com',
            'password': 'pass1234'
        }
        """Test registration and test user already exists has an error i.e routes not available yet... expecting string"""
        

    def test_registration(self):
        """Test user registration works correcty."""
        res = self.app.post('api/v1/auth/signup', data=self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'], "Sign up successful. Please login.")
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res = self.app.post('api/v1/auth/signup', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('api/v1/auth/signup', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User already exists. Please login.")

    def test_user_login(self):
        """Test registered user can login."""
        res = self.app.post('api/v1/auth/login', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('api/v1/auth/login', data=self.user_data)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You logged in successfully.")
        self.assertEqual(login_res.status_code, 200)
        

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        not_a_user = {
            'email': 'emily20@gmail.com',
            'password': 'pass9876'
        }
        res = self.app.post('api/v1/auth/login', data=not_a_user)
        result = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again.")

if __name__ == "__main__":
    unittest.main()
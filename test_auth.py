#third party imports
from copy import deepcopy
import unittest
import json
import jwt

#local imports
from app import app


class AuthTestCase(unittest.TestCase):
    """Test case for the authentication of users"""

    def setUp(self):
        """Set up test variables."""
        self.backup_users = deepcopy(app.users)
        self.app = app.app.test_client()
        self.app.testing = True
        self.user_data = {
            'username': 'Bev Kololi',
            'email': 'bev@gmail.com',
            'password': 'pass1234'
        }
                

    def test_signup(self):
        """Test that the user signup works correcty."""
        res = self.app.post('auth/signup', data=self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'], "Sign up successful. Please login.")
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot sign up twice."""
        res = self.app.post('auth/signup', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('auth/signup', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "This user already exists! Kindly login")

    def test_user_login(self):
        """Test signed up user can login."""
        res = self.app.get('auth/login', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('api/v1/auth/login', data=self.user_data)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "Login successful!!")
        self.assertEqual(login_res.status_code, 200)
        

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        not_a_user = {
            'email': 'emily20@gmail.com',
            'password': 'pass9876'
        }
        res = self.app.post('auth/login', data=not_a_user)
        
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again.")

if __name__ == "__main__":
    unittest.main()
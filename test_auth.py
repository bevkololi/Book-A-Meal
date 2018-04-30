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
        self.app = app.app.test_client()
        self.app.testing = True
        self.user_data = {
            'username': 'Bev Kololi',
            'email': 'bev@gmail.com',
            'password': 'pass1234',
            'caterer': True
        }
                

    def test_signup(self):
        """Test that the user signup works correcty."""
        res = self.app.post('auth/signup', data=json.dumps(self.user_data))
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(
            result['message'], 'New user created!')
        self.assertEqual(res.status_code, 201)

   
    def test_user_login(self):
        """Test signed up user can login."""
        res = self.app.post('auth/signup', data=json.dumps(self.user_data))
        self.assertEqual(res.status_code, 201)
        login_res = self.app.post('/auth/login', data=json.dumps(self.user_data))
        result = json.loads(login_res.data.decode('utf-8'))
        self.assertEqual(result['message'], "Login successful!!")
        self.assertEqual(login_res.status_code, 200)
        

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        not_a_user = {
            'email': 'emily20@gmail.com',
            'password': 'pass9876'
        }
        res = self.app.post('auth/login', data=json.dumps(not_a_user))
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again.")

if __name__ == "__main__":
    unittest.main()
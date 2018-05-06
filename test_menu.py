# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db
from app.models import User

class MenuTestCase(unittest.TestCase):
    """This class represents the Menu test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        self.menu = [{'name': 'Ugali and sukuma wiki', 'description': 'This is ugali description', 'price': 20}]

        
        with self.app.app_context():
            #create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, username= 'Some user', email="user@gmail.com", password="pass1234"):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        return self.client().post('/auth/signup', data=user_data)

    def login_user(self, username= 'Some user', email="user@gmail.com", password="pass1234"):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        return self.client().post('/auth/login', data=user_data)

    def login_admin(self, username= 'Some user', email="user@gmail.com", password="pass1234", caterer=True):
        admin = User(username=username, email=email, password=password)
        admin.caterer =caterer
        admin.save()
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'caterer': True
        }
        return self.client().post('/auth/login', data=user_data)

    def test_non_admin_cannot_create_menu(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('api/v1/menu/', headers=dict(Authorization="Bearer " + access_token), data=self.menu)
        expected = {"message": "You are unauthorized to access this"}
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result, expected)

    def test_admin_can_creates_menu(self):
        """Test API can create a meal (POST request)"""
        result = self.login_admin()
        self.assertEqual(200, result.status_code)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('api/v1/meals/', headers=dict(Authorization="Bearer " + access_token), data=self.menu)
        expected = 'Todays menu has been updated'
        result = json.loads(res.data.decode('utf-8'))['message']
        self.assertEqual(res.status_code, 201)
        self.assertEqual(result, expected)
        

    def test_authorized user_can_get_menu(self):
        """Test API can get a meal (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('api/v1/meals/', headers=dict(Authorization="Bearer " + access_token), data=self.menu)
        self.assertEqual(res.status_code, 401)
        res = self.client().get('api/v1/meals/', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        

    
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            ##drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()

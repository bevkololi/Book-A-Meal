# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db

class MealTestCase(unittest.TestCase):
    """This class represents the Meal test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.meal = {'name': 'Ugali and sukuma wiki', 'description': 'This is ugali description', 'price': 20}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, username= 'Some user', email="user@test.com", password="test1234"):
        user_data = {
            'username': username,
            'email': email,
            'password': password
        }
        return self.client().post('/auth/signup', data=user_data)

    def login_user(self, username= 'Some user', email="user@test.com", password="test1234"):
        user_data = {
            'username': username,
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_meal_creation(self):
        """Test API can create a meal (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('api/v1/meals/', headers=dict(Authorization="Bearer " + access_token), data=self.meal)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Ugali', str(res.data))

    def test_api_can_get_all_meals(self):
        """Test API can get a meal (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('api/v1/meals/', headers=dict(Authorization="Bearer " + access_token), data=self.meal)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('api/v1/meals/', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Ugali', str(res.data))

    def test_api_can_get_meal_by_id(self):
        """Test API can get a single meal by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client().post('api/v1/meals/', headers=dict(Authorization="Bearer " + access_token), data=self.meal)
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/api/v1/meals/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Ugali', str(result.data))

    def test_meal_can_be_edited(self):
        """Test API can edit an existing meal. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client().post(
            'api/v1/meals/', headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Spaghetti and rice', 'description': 'This is a description of ugali and sukuma wiki', 'price': 40})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            'api/v1/meals/1', headers=dict(Authorization="Bearer " + access_token),
            data={
                'name': 'Spaghetti and rice and stewed meat', 'description': 'This is a description of ugali and sukuma wiki', 'price': 40
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('api/v1/meals/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('stewed meat', str(results.data))

    def test_meal_deletion(self):
        """Test API can delete an existing meal. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client().post(
            'api/v1/meals/', headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Spaghetti and rice', 'description': 'This is a description of ugali and sukuma wiki', 'price': 40})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('api/v1/meals/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('api/v1/meals/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

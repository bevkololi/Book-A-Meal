# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db

class OrderTestCase(unittest.TestCase):
    """This class represents the Meal test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.order = {'meal': 'Ugali and sukuma wiki', 'quantity':2}

        
        with self.app.app_context():
            # create all tables
            # db.session.close()
            # db.drop_all()
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

    def test_order_creation(self):
        """Test API can create an order (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('api/v1/orders/', headers=dict(Authorization="Bearer " + access_token), data=self.order)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Ugali', str(res.data))

    def test_api_can_get_all_orders(self):
        """Test API can get an order (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('api/v1/orders/', headers=dict(Authorization="Bearer " + access_token), data=self.order)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('api/v1/orders/', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Ugali', str(res.data))

    def test_api_can_get_order_by_id(self):
        """Test API can get a single order by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client().post('api/v1/orders/', headers=dict(Authorization="Bearer " + access_token), data=self.order)
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/api/v1/orders/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Ugali', str(result.data))

    def test_order_can_be_edited(self):
        """Test API can edit an existing order. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client().post(
            'api/v1/orders/', headers=dict(Authorization="Bearer " + access_token),
            data={'meal': 'Spaghetti and rice', 'quantity': 3})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            'api/v1/orders/1', headers=dict(Authorization="Bearer " + access_token),
            data={
                'meal': 'Spaghetti and rice and stewed meat', 'quantity': 2
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('api/v1/orders/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('stewed meat', str(results.data))

    def test_order_deletion(self):
        """Test API can delete an existing order. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client().post(
            'api/v1/orders/', headers=dict(Authorization="Bearer " + access_token),
            data={'meal': 'Spaghetti and rice', 'quantity': 3})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('api/v1/orders/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        result = self.client().get('api/v1/orders/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()

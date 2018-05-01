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
        self.meal = {'name': 'Ugali and sukuma wiki'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_meal_creation(self):
        """Test API can create a meal (POST request)"""
        res = self.client().post('api/v1/meals/', data=self.meal)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Ugali', str(res.data))

    def test_api_can_get_all_meals(self):
        """Test API can get a meal (GET request)."""
        res = self.client().post('api/v1/meals/', data=self.meal)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('api/v1/meals/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Ugali', str(res.data))

    def test_api_can_get_meal_by_id(self):
        """Test API can get a single meal by using it's id."""
        rv = self.client().post('api/v1/meals/', data=self.meal)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            'api/v1/meals/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Ugali', str(result.data))

    def test_meal_can_be_edited(self):
        """Test API can edit an existing meal. (PUT request)"""
        rv = self.client().post(
            'api/v1/meals/',
            data={'name': 'Spaghetti and rice'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            'api/v1/meals/1',
            data={
                "name": "Spaghetti, rice and stewed meat"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('api/v1/meals/1')
        self.assertIn('stewed meat', str(results.data))

    def test_meal_deletion(self):
        """Test API can delete an existing meal. (DELETE request)."""
        rv = self.client().post(
            'api/v1/meals/',
            data={'name': 'Spaghetti and rice'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('api/v1/meals/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('api/v1/meals/1')
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

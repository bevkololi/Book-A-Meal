# third party importd
from copy import deepcopy
import unittest
import json

# local imports
from app import app
# from app.models import meals

# defining URLs to avoid repitition
BASE_URL = 'http://127.0.0.1:5000/api/v1/meals'
# redirects url in case of bad requests so app doesn't crash
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)


class TestMeals(unittest.TestCase):
    def setUp(self):
        """Set up test variables"""
        meals = [{'id': 1,
                  'name': 'Ugali and fish',
                  'ingredients': 'Ugali, fish, vegetables, spices',
                  'price': 150},
                 {'id': 2,
                  'name': 'Rice and beef',
                  'ingredients': 'Cooked rice, salad, stewed beef',
                  'price': 320},
                 {'id': 3,
                  'name': 'Matoke and mutton',
                  'ingredients': 'Unripe cooked banana, stew, mutton, appetizer',
                  'price': 250}]
        self.backup_meals = deepcopy(meals)
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_all(self):
        """Test that user can get all meals"""
        meals = {
            'id': 1,
            'name': 'Ugali and fish',
            'ingredients': 'Ugali, fish, vegetables, spices',
            'price': 150}
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 200)

    def test_get_one(self):
        """Test that user can get just one meal"""
        meals = {
            'id': 1,
            'name': 'Ugali and fish',
            'ingredients': 'Ugali, fish, vegetables, spices',
            'price': 150}
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['meals'][0]['name'], 'Ugali and fish')

    def test_post(self):
        """Test that user can add meal"""
        meal = {"name": "Some meal"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(meal),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        #price field cannot take str#
        meal = {"name": "A meal", "price": 'string'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(meal),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # valid: both required fields, price takes int
        meal = {
            "id": 5,
            "name": "A meal",
            "ingredients": "Banana, pawpaw, pineaple",
            "price": 70}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(meal),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(data['meal']['id'], 5)
        self.assertEqual(data['meal']['name'], 'A meal')
        # cannot add meal with same name again
        meal = {"name": "A meal", "price": 70}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(meal),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update(self):
        """Test that user can modify existing meal"""
        meal = {"ingredients": "Pork and spaghetti"}
        response = self.app.put(GOOD_ITEM_URL,
                                data=json.dumps(meal),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(data['meal']['ingredients'], "Pork and spaghetti")
        self.assertEqual(
            self.backup_meals[0]['ingredients'],
            'Ugali, fish, vegetables, spices')

    def test_update_error(self):
        """Test that user cannot modify a nonexisting meal"""
        meal = {"price": "900"}
        response = self.app.put(BAD_ITEM_URL,
                                data=json.dumps(meal),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)
        # price field cannot take str
        meal = {"price": 'string'}
        response = self.app.put(GOOD_ITEM_URL,
                                data=json.dumps(meal),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        """Test that user can delete meal"""
        response = self.app.delete(GOOD_ITEM_URL)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """reset app.meals to initial state"""
        app.meals = self.backup_meals


if __name__ == "__main__":
    unittest.main()

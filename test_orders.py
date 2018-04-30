# third party imports
from copy import deepcopy
import unittest
import json

# local imports
from app import app

BASE_URL = 'http://127.0.0.1:5000/api/v1/orders'
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)


class TestOrders(unittest.TestCase):
    """Set up test variables"""

    def setUp(self):
        orders = [{"order_id": 1,
                   "username": "Angie Kihara",
                   'meal': 'Pilau and chicken',
                   'quantity': 2},
                  {"order_id": 2,
                   'username': 'Victor Kubo',
                   'meal': 'Ugali, fish, vegetables and spices',
                   'quantity': 1},
                  {"order_id": 3,
                   'username': 'Charles Ngara',
                   'meal': 'Unripe cooked banana, stew, mutton, appetizer',
                   'quantity': 4}]

        self.backup_orders = deepcopy(orders)
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_all(self):
        """Test that user can get all orders"""
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['orders']), 3)

    def test_get_one(self):
        """Test that user can get just one customer's orders"""
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['orders'][0]['username'], 'Angie Kihara')

    def test_post(self):
        """Test that user can add order"""
        order = {"meal": "Some meal"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        #quantity field cannot take str#
        order = {"meal": "A meal", "quantity": 'string'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # valid: both required fields, quantity takes int
        order = {
            "order_id": 5,
            "username": "Kim Chan",
            "meal": "A meal",
            "quantity": 8}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(data['order']['order_id'], 4)
        self.assertEqual(data['order']['meal'], 'A meal')
        # cannot add order with same order again
        order = {"meal": "A meal", "quantity": 8}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update(self):
        """Test that user can modify existing order"""
        order = {"meal": "Pork and spaghetti"}
        response = self.app.put(GOOD_ITEM_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(data['order']['meal'], "Pork and spaghetti")
        self.assertEqual(
            self.backup_orders[2]['meal'],
            "Unripe cooked banana, stew, mutton, appetizer")

    def test_update_error(self):
        """Test that user cannot modify a nonexisting order"""
        order = {"quantity": "10"}
        response = self.app.put(BAD_ITEM_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)
        # quantity field cannot take str
        order = {"quantity": 'string'}
        response = self.app.put(GOOD_ITEM_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        """Test that user can get delete orders"""
        response = self.app.delete(GOOD_ITEM_URL)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """reset app.orders to initial state"""
        app.orders = self.backup_orders


if __name__ == "__main__":
    unittest.main()

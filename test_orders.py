#third party imports
from copy import deepcopy
import unittest
import json

#local imports
from app import app

BASE_URL = 'http://127.0.0.1:5000/api/v1/orders'
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)


class TestOrders(unittest.TestCase):
    """Set up test variables"""
    def setUp(self):
        self.backup_orders = deepcopy(app.orders)  
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

    
    def test_delete(self):
        """Test that user can get delete orders"""
        response = self.app.delete(GOOD_ITEM_URL)
        self.assertEqual(response.status_code, 204)
        response = self.app.delete(BAD_ITEM_URL)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        """reset app.orders to initial state"""
        app.orders = self.backup_orders


if __name__ == "__main__":
    unittest.main()
from copy import deepcopy
import unittest
import json

from app import app





BASE_URL = 'http://127.0.0.1:5000/api/v1/orders'
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)


class TestFlaskApi(unittest.TestCase):

    

if __name__ == "__main__":
    unittest.main()
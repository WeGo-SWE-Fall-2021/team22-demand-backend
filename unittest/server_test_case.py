import unittest
import sys
import time
import requests
import json
import jwt

sys.path.insert(1, sys.path[0] + "/../")

from threading import Thread
from utils.mongoutils import initMongoFromCloud
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
from plugintype import PluginType
from os import getenv


# Global variables used in the unittest
port = 4001

# Defined data

customer_data_one = {
    "_id": "1515646454",
    "firstName": "test_firstName",
    "lastName": "test_lastName",
    "phoneNumber": "test_phoneNumber",
    "email": "test@test.com",
    "username": "test_username",
    "password": "test_password"
}

order_one = {
    "_id": "123",
    "customerId": customer_data_one["_id"],
    "pluginType": PluginType.MEDICATION.name,
    "timeStamp": "23244",
    "paymentType": "CARD",
    "orderDestination": "3001 S Congress Ave, Austin, TX 78704"
}

client = initMongoFromCloud("demand")
db = client["team22_demand"]

# This is a demo that unittests the python endpoints. Beware, order matters in this case since we are
# dealing witht the database, might vary depending on how you're tesing

# TEST METHOD ORDER STRUCTURE $
# def test_(number here)_(subject here):

class ServerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up server
        cls._server = HTTPServer(('', port), SimpleHTTPRequestHandler)
        cls._server_thread = Thread(None, cls._server.serve_forever)
        cls._server_thread.start()

        db.Customer.remove({})
        db.Order.remove({})
        db.Customer.insert_one(customer_data_one)
        db.Order.insert_one(order_one)

    # Cannot test case since when requesting order information it has to communicate with supply
    def test_get_order_failed_communicating_supply(self):
        # Generate a jwt token
        token_secret = getenv("TOKEN_SECRET")
        token = jwt.encode({ 
            "user_id": customer_data_one["_id"]
            }, token_secret, algorithm="HS256")
        cookies = {
            'token': token
         }

        response = requests.get("http://localhost:4001/orders", cookies=cookies, timeout=10)
        self.assertEqual(response.status_code, 404) # Data is not found

    # Cannot test case since when requesting order information it has to communicate with supply
    def test_get_order_failed_none_in_database(self):
        # Generate a jwt token
        token_secret = getenv("TOKEN_SECRET")
        token = jwt.encode({ 
            "user_id": customer_data_one["_id"]
            }, token_secret, algorithm="HS256")
        cookies = {
            'token': token
         }

        db.Order.remove({})
        response = requests.get("http://localhost:4001/orders", cookies=cookies, timeout=10)
        self.assertEqual(response.status_code, 404) # Data is not found
        db.Order.insert_one(order_one)

    @classmethod
    def tearDownClass(cls):
        # tear down server
        cls._server.shutdown()
        cls._server_thread.join()

        db.Customer.remove({})
        db.Order.remove({})
        client.close()

if __name__ == '__main__':
    unittest.main()
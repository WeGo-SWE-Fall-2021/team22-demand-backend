import unittest
import sys
import time
import requests
import json

sys.path.insert(1, sys.path[0] + "/../")

from threading import Thread
from utils.mongoutils import initMongoFromCloud
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
from plugintype import PluginType

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
    "password": "test_password",
    "token": "tokennnnn"
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
    def test_get_order(self):
        order_data = db.Order.find_one({ "_id": order_one["_id"]})
        self.assertEqual(order_data["_id"], order_one["_id"])

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
import unittest
import sys
import time
import requests
import json

from threading import Thread

sys.path.insert(1, "../")
sys.path.insert(2, "../../team22-common-services-backend")
sys.path.insert(2, "../../common-services-backend")
from mongoutils import initMongoFromCloud
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler

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
    "token": "tokennnnn",
}

order_one = {
    "_id": "123",
    "customerId": customer_data_one["_id"],
    "pluginName ": "medication",
    "timeStamp": "23244",
    "paymentType": "card",
    "orderDestination": "Austin"
}

client = initMongoFromCloud("demand")
db = client["team22_supply"]

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

        db.Customer.insert_one(customer_data_one)
        db.Order.insert_one(order_one)

    # Commenting out since supply has not set up Fleet class yet
    # def test_create_order_request(self):
    #     order_one = {
    #         "_id": "123",
    #         "customerId": "34645",
    #         "pluginName ": "medication",
    #         "timeStamp": "23244",
    #         "paymentType": "card",
    #         "orderDestination": "Austin"
    #     }
    #     response = requests.post(f"http://localhost:{port}/order", json=order_one, timeout=5)
    #     self.assertEqual(response.status_code, 201)

    @classmethod
    def tearDownClass(cls):
        # tear down server
        cls._server.shutdown()
        cls._server_thread.join()

if __name__ == '__main__':
    unittest.main()

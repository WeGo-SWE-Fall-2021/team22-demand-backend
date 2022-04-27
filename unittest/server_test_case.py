import unittest
import sys
import time
import requests
import json
import jwt
import uuid

sys.path.insert(1, sys.path[0] + "/../")

from threading import Thread
from utils.mongoutils import initMongo
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
from plugintype import PluginType
from os import getenv


# Global variables used in the unittest
port = 4001

# Defined data

plugin_type_one = {
    "_id": str(uuid.uuid4()),
    "name": PluginType.MEDICATION.name,
    "available": True,
    "vType": "refrigerated"
}

plugin_type_one_item_one = {
    "_id": str(uuid.uuid4()),
    "name": "Ibuprofen",
    "pluginId": plugin_type_one["_id"],
    "options": {
        "size": ["24mg", "500mg"]   
    }
}

plugin_type_two = {
    "_id": str(uuid.uuid4()),
    "name": PluginType.PIZZA.name,
    "available": True,
    "vType": "food"
}

plugin_type_two_item_one = {
    "_id": str(uuid.uuid4()),
    "name": "Large Pizza",
    "pluginId": plugin_type_two["_id"],
    "options": [{
        "toppings": ["Pepperoni"]
    }]
}

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
    "timeStamp": "23244",
    "paymentType": "CARD",
    "orderDestination": "3001 S Congress Ave, Austin, TX 78704",
    "plugin": PluginType.MEDICATION.name,
    "items": [{
        "name": plugin_type_one_item_one["name"],
        "option": plugin_type_one_item_one["options"]["size"][0]
    }]
}

client = initMongo("demand")
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
        db.Plugin.remove({})
        db.Item.remove({})
        db.Customer.insert_one(customer_data_one)
        db.Order.insert_one(order_one)
        db.Plugin.insert([plugin_type_one, plugin_type_two])
        db.Item.insert([plugin_type_one_item_one, plugin_type_two_item_one])

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
        self.assertEqual(response.status_code, 200) # Data is not found
        db.Order.insert_one(order_one)

    def test_get_all_plugins(self):
        response = requests.get("http://localhost:4001/plugins?name=all", timeout=10)
        self.assertEqual(response.status_code, 200)
        json_body = json.loads(response.text)
        plugins_data = json_body["plugins"]
        self.assertEqual(len(plugins_data), 2)

    def test_get_food_plugin(self):
        response = requests.get("http://localhost:4001/plugins?name=PIZZA", timeout=10)
        self.assertEqual(response.status_code, 200)
        json_body = json.loads(response.text)
        plugin_data = json_body["plugin"]
        self.assertEqual(plugin_data["name"], plugin_type_two["name"])

    def test_get_plugin_not_in_db(self):
        response = requests.get("http://localhost:4001/plugins?name=no", timeout=10)
        self.assertEqual(response.status_code, 200)
        json_body = json.loads(response.text)
        plugin_data = json_body["plugin"]
        self.assertEqual(plugin_data, {})

    def test_get_plugin_no_args(self):
        response = requests.get("http://localhost:4001/plugins", timeout=10)
        self.assertEqual(response.status_code, 400)

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
    
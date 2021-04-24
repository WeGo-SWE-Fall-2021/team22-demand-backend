import sys
import json
import requests
import jwt

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from order import Order
from customer import Customer
from utils.mongoutils import initMongoFromCloud
from plugintype import PluginType
from urllib import parse
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    version = '0.1.0'

    # Reads the POST data from the HTTP header
    def extract_POST_Body(self):
        postBodyLength = int(self.headers['content-length'])
        postBodyString = self.rfile.read(postBodyLength)
        postBodyDict = json.loads(postBodyString)
        return postBodyDict

    # handle post requests
    def do_POST(self):
        status = 401  # HTTP Request: Not found
        postData = self.extract_POST_Body()  # store POST data into a dictionary
        path = self.path
        cloud = 'demand'
        client = initMongoFromCloud(cloud)
        db = client['team22_' + cloud]
        responseBody = {
            'status': 'failed',
            'message': 'Request not found'
        }

        customer = self.fetch_customer_from_token(db)

        if '/order' in path:
            if customer is not None:
                postData["customerId"] = customer.id
                order = Order(postData)

                dispatch_response = order.dispatchOrder("FOOD")
                if dispatch_response["status"] == 201:
                    data = {
                        "_id": order.id,
                        "customerId": order.customerId,
                        "pluginType": order.pluginType.name,
                        "timeStamp": order.timeStamp,
                        "paymentType": order.paymentType,
                        "orderDestination": order.orderDestination
                    }
                    db.Order.insert_one(data)
                    status = 201
                    responseBody = {
                        'status': 'success',
                        'message': 'successfully created order',
                        'tracking': dispatch_response["data"]["vehicleId"],
                        'location': dispatch_response["data"]["location"]
                    }
            else:
                status = 403 # Unauthorized
                responseBody["message"] = "No user logged in"

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        responseString = json.dumps(responseBody).encode('utf-8')
        self.wfile.write(responseString)
        client.close()

    def do_GET(self):
        path = self.path
        status = 400
        cloud = 'demand'
        client = initMongoFromCloud(cloud)
        db = client['team22_' + cloud]
        responseBody = {
            'status': 'failed',
            'message': 'request not found'
        }

        # Parse values after path and get it as dictionary
        parameters = dict(parse.parse_qsl(parse.urlsplit(path).query))

        customer = self.fetch_customer_from_token(db)


        if '/orders' in path:
            status = 401 # Unauthorized, not known to user
            if customer is not None:
                if parameters is False: # If argumets empty then return all items in dictionary
                    orders = list(db.Order.find({ "customerId": customer.id }, {
                        "_id": 1,
                        "pluginType": 1,
                        "timeStamp": 1,
                        "paymentType": 1,
                        "orderDestination": 1
                    }))
                    for order in orders:
                        response = requests.get(f"https://supply.team22.sweispring21.tk/api/v1/supply/status?orderId={order['_id']}", timeout=5)
                        if response.status_code == 200:
                            data = json.load(response.text)
                            order["status"] = data["order_status"]
                            order["starting_coordinates"] = data["vehicle_starting_coordinate"]
                            order["destination_coordinates"] = data["destination_coordinate"]
                            order["geometry"] = data["geometry"]

                    status = 200
                    responseBody["status"] = "success"
                    responseBody["message"] = "successfully got orders"
                    responseBody["orders"] = orders
                else:
                    order_id = parameters["orderId"]
                    order_data = db.Order.find_one({ "_id": order_id })
                    if order_data is not None:
                        order = Order(order_data)
                        response = requests.get(f"https://supply.team22.sweispring21.tk/api/v1/supply/status?orderId={order.id}", timeout=5)
                        if response.status_code == 200:
                            data = json.load(response.text)
                            status = 200
                            responseBody["order"] = {
                                "_id": order.id,
                                "pluginType": order.pluginType.name,
                                "timeStamp": order.timeStamp,
                                "paymentType": order.paymentType,
                                "orderDestination": order.orderDestination
                            }
                            responseBody["status"] = "success"
                            responseBody["message"] = "successfully got order from id"
                            responseBody["order"]["status"] = data["order_status"]
                            responseBody["order"]["vehicle"]["starting_coordinates"] = data["vehicle_starting_coordinate"]
                            responseBody["order"]["vehicle"]["destination_coordinates"] = data["destination_coordinate"]
                            responseBody["order"]["vehicle"]["geometry"] = data["geometry"]
                        else:
                            pass
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        responseString = json.dumps(responseBody).encode('utf-8')
        self.wfile.write(responseString)
        client.close()

    def fetch_customer_from_token(self, db):
        try:
            tokenStr = self.headers["Cookie"]
            if tokenStr is not None:
                token = tokenStr.split('token=')[1].split(";")[0]
                if token != "":
                    token_secret = getenv("TOKEN_SECRET")
                    token_decoded = jwt.decode(token, token_secret, algorithms="HS256")
                    user_data = db.Customer.find_one({ "_id": token_decoded["user_id"]})
                    return Customer(user_data)
        except:
            pass
        return None

def main():
    port = 4001
    server = HTTPServer(('', port), SimpleHTTPRequestHandler)
    print('Server is starting... Use <Ctrl+C> to cancel. Running on Port 8080')
    server.serve_forever()


if __name__ == "__main__":
    main()

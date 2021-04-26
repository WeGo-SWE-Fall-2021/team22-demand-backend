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
from orderstatus import OrderStatus

load_dotenv()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    version = '0.3.0'

    # Reads the POST data from the HTTP header
    def extract_POST_Body(self):
        try:
            postBodyLength = int(self.headers['content-length'])
            postBodyString = self.rfile.read(postBodyLength)
            postBodyDict = json.loads(postBodyString)
            return postBodyDict
        except:
            print("There was an error parsing POST body")
            return {}

    # handle post requests
    def do_POST(self):
        status = 400  # HTTPS: Bad request
        postData = self.extract_POST_Body()  # store POST data into a dictionary
        path = self.path
        cloud = 'demand'
        client = initMongoFromCloud(cloud)
        db = client['team22_' + cloud]
        responseBody = {
            'status': 'failed',
            'message': 'Bad request'
        }

        customer = self.fetch_customer_from_token(db)

        if '/order' in path:
            status = 401 # HTTPS: Unauthenticated
            responseBody["message"] = "No user authenticated"

            if customer is not None:
                postData["customerId"] = customer.id
                try:
                    order = Order(postData)
                except:
                    order = None

                status = 400
                responseBody["message"] = "Invalid order data."
                if order is not None:
                    status = 403 # Forbitten to change
                    responseBody["message"] = "Order cannot be added since the specified plugin is unavailable."
                    plugin_data = db.Plugin.find_one({"name": order.plugin.name, "available": True})
                    if plugin_data is not None:
                        vType = plugin_data["vType"]

                        dispatch_request_data = {
                            "orderId": order.id,
                            "orderDestination": order.orderDestination,
                            "vehicleType": vType
                        }

                        dispatch_response = requests.post("https://supply.team22.sweispring21.tk/api/v1/supply/dispatch", json=dispatch_request_data, timeout=10)
                        dispatch_response_body = json.loads(dispatch_response.text)

                        if dispatch_response.status_code == 201:
                            data = {
                                "_id": order.id,
                                "customerId": order.customerId,
                                "plugin": order.plugin.name,
                                "timeStamp": order.timeStamp,
                                "paymentType": order.paymentType,
                                "orderDestination": order.orderDestination,
                                "items": order.items
                            }
                            db.Order.insert_one(data)
                            status = 201
                            responseBody = {
                                'status': 'success',
                                'message': 'successfully created order',
                                'orderId': order.id,
                                'tracking': dispatch_response["data"]["vehicleId"],
                                'location': dispatch_response["data"]["location"]
                            }
                        elif dispatch_response.status_code == 409:
                            # if user resubmitting order
                            status = 409
                            responseBody["message"] = "Order has already been submitted."

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
            responseBody["message"] = "No user authenticated."
            if customer is not None:
                single_order_id = parameters.get("orderId", None)
                orders_data = list(db.Order.find({ "customerId": customer.id }))

                if single_order_id is not None:
                    orders_data = list(filter(lambda x: x.get("_id") == single_order_id, orders_data))

                status = 404 # Not found, yes it's used in file server but I also need to identify if there are no orders for this user
                responseBody["message"] = "No orders found."
                if len(orders_data) != 0:
                    orders = list(map(lambda x: Order(x), orders_data))
                    url_order_ids = ""
                    for order in orders:
                        if url_order_ids != "":
                            url_order_ids += "&"
                        url_order_ids += f"orderId={order.id}"

                    order_dispatch_response = requests.get(f"https://supply.team22.sweispring21.tk/api/v1/supply/status?orderId={url_order_ids}", timeout=10)
                    if order_dispatch_response.status_code == 200:
                        dispatches_data = json.loads(order_dispatch_response.text).get("dispatches")
                        orders_array = []

                        for order in orders:
                            dispatch_data = list(filter(lambda x: x.get("orderId"), dispatches_data)).get(0)
                            dispatch_status = dispatch_data.get("dispatchStatus")

                            if dispatch_status == "processing":
                                order_status = OrderStatus.PROCESSING
                            elif dispatch_status == "in progress":
                                order_status = OrderStatus.SHIPPED
                            elif dispatch_status == "complete":
                                order_status == OrderStatus.DELIVERED
                            else:
                                order_status == OrderStatus.ERROR

                            orders_array.append({
                                "orderId": order.id,
                                "orderStatus": order_status.name,
                                "plugin": order.plugin.name,
                                "paymentType": order.paymentType,
                                "timeStamp": order.timeStamp,
                                "items": order.items,
                                "orderDestination": order.orderDestination,
                                "vehicleLocation": dispatch_data["vehicleLocation"],
                                "destinationCoordinate": dispatches_data["destinationCoordinate"],
                                "geometry": dispatch_data["geometry"]
                            })

                        status = 200
                        responseBody["status"] = "success"
                        responseBody["message"] = "Successfully got orders"
                        responseBody["orders"] = orders_array
                    elif order_dispatch_response.status_code == 400:
                        status = 400
                        responseBody["message"] = "There was an error getting order statuses."

        elif '/plugins':
            # Returns plugins with availability
            plugin_name = parameters.get("name", None)
            if plugin_name is not None:
                if plugin_name == "all":
                    plugins = list(db.Plugin.find({}, {
                        "_id": 1,
                        "name": 1,
                        "available": 1,
                    }))
                    plugins_array = []
                    for plugin in plugins:
                        items = list(db.Item.find({ "pluginId": plugin["_id"] }, {
                            "options": 1,
                            "name": 1,
                        }))
                        plugins_array.append({
                            "_id": plugin["_id"],
                            "name": plugin["name"],
                            "available": plugin["available"],
                            "items": items
                        })
                    status = 200
                    responseBody = {
                        'status': 'successful',
                        'plugins': plugins_array
                    }
                else:
                    plugin = db.Plugin.find_one({ "name": plugin_name }, {
                        "name": 1,
                        "items": 1,
                        "available": 1,
                    })
                    if plugin is None:
                        plugin = {}
                    else:
                        items = list(db.Item.find({ "pluginId": plugin["_id"] }, {
                            "options": 1,
                            "name": 1,
                        }))
                        plugin["items"] = items
                    status = 200
                    responseBody = {
                        'status': 'successful',
                        'plugin': plugin
                    }

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

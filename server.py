import sys
# Allow importing files from other directories
sys.path.insert(1, '../team22-common-services-backend')
sys.path.insert(1, '../common-services-backend')
import json
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from order import Order
from customer import Customer
from mongoutils import initMongoFromCloud



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    version = '0.0.2'

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
        cloud = postData['cloud']
        client = initMongoFromCloud(cloud)
        db = client['team22_' + cloud]
        responseBody = {
            'status': 'failed',
            'message': 'Request not found'
        }

        if '/order' in path:
            order = Order(postData)
            # TODO in the future will call user.requestVehicle, get a vehicleID back, then add it to the database
            data = {
                "_id": order.id,
                "customerId": order.customerId,
                "pluginName": order.pluginName,
                "timeStamp": order.timeStamp,
                "paymentType": order.paymentType,
                "orderDestination": order.orderDestination
            }
            db.Order.insert_one(data)
            response = order.requestVehicle()
            if response["status"] == 201:
                status = 201
                responseBody = {
                    'status': 'success',
                    'message': 'successfully created order',
                    'tracking': response["tracking"] 
                }

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        responseString = json.dumps(responseBody).encode('utf-8')
        self.wfile.write(responseString)
        client.close()

    def do_GET(self):
        pass


def main():
    port = 4001
    server = HTTPServer(('', port), SimpleHTTPRequestHandler)
    print('Server is starting... Use <Ctrl+C> to cancel. Running on Port 8080')
    server.serve_forever()


if __name__ == "__main__":
    main()

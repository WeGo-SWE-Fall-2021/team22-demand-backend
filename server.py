import sys
# Allow importing files from other directories
sys.path.insert(1, '../team22-common-services-backend')
sys.path.insert(1, '../common-services-backend')
import json
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from Order import Order
from MongoUtils import initMongoFromCloud



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
        status = 404  # HTTP Request: Not found
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
            db.order.insert_one(order.__dict__)

            ##### TEMPORARY just sending the order number back from the supply side as a response
            temporaryResponse = order.requestVehicle()
            if (temporaryResponse == 0000):
                status = 200
                responseBody = {
                    'status': 'success',
                    'message': str(temporaryResponse)
                }
            else:
                status = 500
                print(temporaryResponse)

        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        responseString = json.dumps(responseBody).encode('utf-8')
        self.wfile.write(responseString)
        client.close()

    def do_GET(self):
        return


def main():
    port = 4001
    server = HTTPServer(('', port), SimpleHTTPRequestHandler)
    print('Server is starting... Use <Ctrl+C> to cancel. Running on Port 8080')
    server.serve_forever()


if __name__ == "__main__":
    main()

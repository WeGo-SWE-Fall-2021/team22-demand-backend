import json
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from pymongo import MongoClient

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Reads the POST data from the HTTP header
    def extract_POST_Body(self):
        postBodyLength = int(self.headers['content-length'])
        postBodyString = self.rfile.read(postBodyLength)
        postBodyDict = json.loads(postBodyString)
        return postBodyDict

    # handle post requests
    def do_POST(self):
        # status = 200
        # self.send_response(status)
        # self.send_header("Content-type", "text/html")
        # self.end_headers()

        # store POST data into a dictionary
        postData = self.extract_POST_Body()
        path = self.path

        # receiving registration requests and writing their data to the demand database
        if '/register' in path:
            client = MongoClient('localhost:27017', username="developer", password="team22_developer")
            db = client.team22_demand
            db.user.insert_one({"username": postData["username"],
                                "fname": postData["fname"],
                                "lname": postData["lname"],
                                "address": postData["address"],
                                "password": postData["password"]})
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

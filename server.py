import json
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler


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
        # store POST data into a dictionary
        postData = self.extract_POST_Body()
        path = self.path

        # Handle request here usinf if and elif
        if 'request' in path:
            pass

    def do_GET(self):
        return


def main():
    port = 4001
    server = HTTPServer(('', port), SimpleHTTPRequestHandler)
    print('Server is starting... Use <Ctrl+C> to cancel. Running on Port 8080')
    server.serve_forever()


if __name__ == "__main__":
    main()

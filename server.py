from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        return

    def do_GET(self):
        return

def main():
    # This is a demo port. Once we start adding things, like creating users, ect..., we can define different
    # servers based on port number
    port = 4001
    server = HTTPServer(('', port), SimpleHTTPRequestHandler)
    print('Server is starting... Use <Ctrl+C> to cancel. Running on Port 8080')
    server.serve_forever()

if __name__ == "__main__":
    main()

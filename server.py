from http.server import BaseHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler

Handler = SimpleHTTPRequestHandler

if __name__ == '__main__':
	from http.server import HTTPServer
	server = HTTPServer(('localhost', 8080),Handler)
	print('Server is starting... Use <Ctrl+C> to cancel. Running on Port 8080')
	server.serve_forever()

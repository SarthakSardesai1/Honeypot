import http.server
import socketserver
import logging
from urllib.parse import parse_qs, urlparse
import os
import json

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='http_honeypot.log')
logger = logging.getLogger('http_honeypot')

# Add a file handler to ensure logs are written to the file
file_handler = logging.FileHandler('http_honeypot.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

class WordPressHoneypot(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="template", **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/" or parsed_path.path == "/wp-login.php":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(os.path.join(self.directory, "login.html"), "rb") as f:
                self.wfile.write(f.read())
        elif parsed_path.path.endswith('.css'):
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            with open(os.path.join(self.directory, parsed_path.path.lstrip('/')), "rb") as f:
                self.wfile.write(f.read())
        elif parsed_path.path.endswith('.js'):
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.end_headers()
            with open(os.path.join(self.directory, parsed_path.path.lstrip('/')), "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)
        
        logger.info(f"GET request from {self.client_address[0]} for {self.path}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)
        
        username = parsed_data.get('log', [''])[0]
        password = parsed_data.get('pwd', [''])[0]
        
        log_message = f"Login attempt - IP: {self.client_address[0]}, Username: {username}, Password: {password}"
        logger.info(log_message)
        
        self.send_response(302)
        self.send_header('Location', '/wp-login.php?err=1')
        self.end_headers()

def start_http_server(port=8080):
    with socketserver.TCPServer(("", port), WordPressHoneypot) as httpd:
        logger.info(f"HTTP Honeypot serving on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_http_server()
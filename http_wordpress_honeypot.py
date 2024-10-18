import http.server
import socketserver
import logging
from urllib.parse import parse_qs, urlparse
import os
import json
from logger_config import http_logger
# Set up logging
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "asctime": self.formatTime(record, self.datefmt),
            "name": record.name,
            "levelname": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_record)

logging.basicConfig(
    level=logging.INFO,
    filename='http_honeypot.log')
logger = logging.getLogger('http_honeypot')

# Remove any existing handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Add a file handler with JSON formatter
file_handler = logging.FileHandler('http_honeypot.log')
file_handler.setFormatter(JsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# List of default credentials that will redirect to blank page
DEFAULT_CREDENTIALS = [
    ('admin', 'admin'),
    ('root', 'admin'),
    ('administrator', 'password'),
]


class WordPressHoneypot(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="template", **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/" or parsed_path.path == "/wp-login.php":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(os.path.join(self.directory, "wp-admin.html"), "rb") as f:
                self.wfile.write(f.read())
        elif parsed_path.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(os.path.join(self.directory, "index.html"), "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)
        
        http_logger.info(f"GET,{self.client_address[0]},{self.path}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)
        
        username = parsed_data.get('log', [''])[0]
        password = parsed_data.get('pwd', [''])[0]
        
        http_logger.info(f"LOGIN_ATTEMPT,{self.client_address[0]},{username},{password}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if (username, password) in DEFAULT_CREDENTIALS:
            response = json.dumps({"status": "success", "redirect": "/index.html"})
        else:
            response = json.dumps({"status": "error", "message": "Invalid username or password."})

        self.wfile.write(response.encode())


import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "asctime": self.formatTime(record, self.datefmt),
            "name": record.name,
            "levelname": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_record)



# Remove all other logging configurations and imports

# Replace all instances of logger.info, logger.debug, etc. with:
http_logger.info('Your log message here')
http_logger.debug('Your debug message here')
# ... and so on for other log levels

# Add handlers to the logger
# http_logger.addHandler(http_file_handler)

def start_http_server(port=8080):
    with socketserver.TCPServer(("", port), WordPressHoneypot) as httpd:
        http_logger.info(f"HTTP_SERVER_START,{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_http_server()

from flask import Flask, request, render_template, jsonify
import logging
import traceback
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='http_honeypot.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# List of default credentials that will be accepted
DEFAULT_CREDENTIALS = [
    ('root', 'admin'),
    ('admin', 'admin'),
    ('administrator', 'password'),
]

@app.route('/')
@app.route('/wp-login.php')
def login():
    logging.debug("Rendering login page")
    return render_template('login.html')

@app.route('/wp-login.php', methods=['POST'])
def handle_login():
    logging.debug("Received POST request to /wp-login.php")
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        
        logging.debug(f"Login attempt - Username: {username}, Password: {password}")
        
        if (username, password) in DEFAULT_CREDENTIALS:
            logging.info(f"Successful login - Username: {username}")
            response = jsonify({"status": "success", "redirect": "/wp-admin"})
        else:
            logging.info(f"Failed login - Username: {username}")
            response = jsonify({"status": "error", "message": "Invalid username or password."})
        
        logging.debug(f"Sending response: {response.get_data(as_text=True)}")
        return response
    except Exception as e:
        logging.error(f"Error in handle_login: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/wp-admin')
def blank_page():
    return "Welcome to wp-admin"

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled exception: {str(e)}")
    logging.error(traceback.format_exc())
    return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500

@app.after_request
def log_response(response):
    logging.debug(f"Response status: {response.status}")
    logging.debug(f"Response headers: {response.headers}")
    logging.debug(f"Response body: {response.get_data(as_text=True)}")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
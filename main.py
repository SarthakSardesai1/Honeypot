import argparse
import subprocess
import threading
import time
import os

from basic_ssh_honeypot import start_server as start_ssh_server
from http_wordpress_honeypot import start_http_server

def run_streamlit():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    streamlit_script = os.path.join(current_dir, "streamlit_log_viewer.py")
    process = subprocess.Popen(["streamlit", "run", streamlit_script])
    return process

def main():
    parser = argparse.ArgumentParser(description='Run SSH honeypot, HTTP honeypot, and Streamlit log viewer')
    parser.add_argument("--ssh-port", help="The port to bind the SSH server to (default 2222)", default=2222, type=int)
    parser.add_argument("--http-port", help="The port to bind the HTTP server to (default 8080)", default=8080, type=int)
    parser.add_argument("--bind", "-b", help="The address to bind the servers to", default="", type=str)
    args = parser.parse_args()

    # Start Streamlit app
    streamlit_process = run_streamlit()
    time.sleep(2)
    print("Streamlit server started. You can view the logs at http://localhost:8501")

    # Start HTTP honeypot in a separate thread
    http_thread = threading.Thread(target=start_http_server, args=(args.http_port,))
    http_thread.start()
    print(f"HTTP Honeypot started on port {args.http_port}")

    try:
        # Run SSH honeypot in the main thread
        start_ssh_server(args.ssh_port, args.bind)
    finally:
        # Ensure Streamlit process is terminated when the script ends
        streamlit_process.terminate()
        # Stop the HTTP server (this won't work as is, you'd need to modify the HTTP server to be stoppable)
        # http_thread.join()

if __name__ == "__main__":
    main()
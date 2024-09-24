import streamlit as st
import pandas as pd
import time
from datetime import datetime
import re
import os
import json

def parse_log_line(line):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (\w+) - (.+)'
    match = re.match(pattern, line)
    if match:
        timestamp, name, level, message = match.groups()
        return {
            'timestamp': timestamp,
            'name': name,
            'level': level,
            'message': message
        }
    return None

def load_logs(filename):
    try:
        if not os.path.exists(filename):
            return [], f"Log file {filename} not found."
        
        with open(filename, 'r') as f:
            logs = f.readlines()
        
        parsed_logs = [parse_log_line(log.strip()) for log in logs if log.strip()]
        parsed_logs = [log for log in parsed_logs if log is not None]  # Filter out None values
        
        if not parsed_logs:
            return [], f"No valid log entries found in {filename}."
        
        return parsed_logs, None
    except Exception as e:
        return [], f"Error reading {filename}: {str(e)}"

def main():
    st.title("Honeypot Log Viewer")

    # Create placeholders for the tables
    ssh_table_placeholder = st.empty()
    http_table_placeholder = st.empty()

    while True:
        # Load SSH logs
        ssh_logs, ssh_error = load_logs('ssh_honeypot.log')
        if ssh_logs:
            try:
                ssh_df = pd.DataFrame(ssh_logs)
                ssh_df['timestamp'] = pd.to_datetime(ssh_df['timestamp'])
                ssh_df = ssh_df.sort_values('timestamp', ascending=False)
                
                st.subheader("SSH Honeypot Logs")
                ssh_table_placeholder.dataframe(ssh_df)
            except Exception as e:
                ssh_table_placeholder.error(f"Error processing SSH logs: {str(e)}")
        else:
            ssh_table_placeholder.error(ssh_error or "No SSH logs available")

        # Load HTTP logs
        http_logs, http_error = load_logs('http_honeypot.log')
        if http_logs:
            try:
                http_df = pd.DataFrame(http_logs)
                http_df['timestamp'] = pd.to_datetime(http_df['timestamp'])
                http_df = http_df.sort_values('timestamp', ascending=False)
                
                st.subheader("HTTP Honeypot Logs")
                http_table_placeholder.dataframe(http_df)
            except Exception as e:
                http_table_placeholder.error(f"Error processing HTTP logs: {str(e)}")
        else:
            http_table_placeholder.error(http_error or "No HTTP logs available")

        # Wait for 5 seconds before refreshing
        time.sleep(5)

if __name__ == "__main__":
    main()
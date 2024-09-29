import streamlit as st
import pandas as pd
import time
from datetime import datetime
import re
import os

def parse_ssh_log(line):
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

def parse_http_log(line):
    parts = line.split(' - ')
    if len(parts) >= 3:
        timestamp = ' - '.join(parts[:2])
        log_type, *log_data = parts[2].split(',')
        if log_type == 'LOGIN_ATTEMPT' and len(log_data) >= 3:
            return {
                'timestamp': timestamp,
                'type': log_type,
                'ip': log_data[0],
                'username': log_data[1],
                'password': log_data[2]
            }
        elif log_type in ['GET request', 'HTTP_SERVER_START']:
            return {
                'timestamp': timestamp,
                'type': log_type,
                'data': ','.join(log_data)
            }
    return None

def load_logs(filename, parser):
    if not os.path.exists(filename):
        return pd.DataFrame()
    
    with open(filename, 'r') as f:
        logs = f.readlines()
    
    parsed_logs = [parser(log.strip()) for log in logs if log.strip()]
    parsed_logs = [log for log in parsed_logs if log is not None]
    
    if not parsed_logs:
        return pd.DataFrame()
    
    df = pd.DataFrame(parsed_logs)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df.sort_values('timestamp', ascending=False)

def main():
    st.title("Honeypot Log Viewer")

    # Create placeholders for the tables and refresh time
    ssh_table = st.empty()
    http_table = st.empty()
    refresh_placeholder = st.empty()

    while True:
        # Load SSH logs
        ssh_df = load_logs('ssh_honeypot.log', parse_ssh_log)
        
        # Load HTTP logs
        http_df = load_logs('http_honeypot.log', parse_http_log)

        # Update SSH table
        with ssh_table.container():
            st.subheader("SSH Honeypot Logs")
            if not ssh_df.empty:
                st.dataframe(ssh_df)
            else:
                st.write("No SSH logs available")

        # Update HTTP table
        with http_table.container():
            st.subheader("HTTP Honeypot Logs")
            if not http_df.empty:
                st.dataframe(http_df)
            else:
                st.write("No HTTP logs available")

        # Update the refresh time
        refresh_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        refresh_placeholder.text(f"Last refreshed: {refresh_time}")

        # Wait for 5 seconds before the next refresh
        time.sleep(5)

if __name__ == "__main__":
    main()

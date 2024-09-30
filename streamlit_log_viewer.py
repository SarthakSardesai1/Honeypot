import streamlit as st
import pandas as pd

def load_logs(file_path):
    try:
        with open(file_path, 'r') as f:
            logs = f.readlines()
        return [log.strip() for log in logs]
    except FileNotFoundError:
        return []

def parse_log(log):
    # Implement parsing logic based on your log format
    # This is a placeholder implementation
    parts = log.split(' - ')
    if len(parts) >= 2:
        timestamp = parts[0]
        message = ' - '.join(parts[1:])
        return pd.to_datetime(timestamp), message
    return None, None

st.title('Honeypot Logs')

# Load SSH logs
ssh_logs = load_logs('ssh_honeypot.log')
ssh_data = [parse_log(log) for log in ssh_logs]
ssh_df = pd.DataFrame(ssh_data, columns=['Timestamp', 'Message'])
ssh_df = ssh_df.dropna()

# Load HTTP logs
http_logs = load_logs('http_honeypot.log')
http_data = [parse_log(log) for log in http_logs]
http_df = pd.DataFrame(http_data, columns=['Timestamp', 'Message'])
http_df = http_df.dropna()

# Display SSH logs
st.header('SSH Logs')
st.dataframe(ssh_df)

# Display HTTP logs
st.header('HTTP Logs')
st.dataframe(http_df)

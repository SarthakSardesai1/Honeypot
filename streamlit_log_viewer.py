import streamlit as st
import pandas as pd
import json
from datetime import datetime

def load_logs(file_path):
    try:
        with open(file_path, 'r') as f:
            logs = f.readlines()
        return [log.strip() for log in logs]
    except FileNotFoundError:
        return []

def parse_ssh_log(log):
    try:
        parts = log.split(' - ')
        if len(parts) >= 4:
            timestamp = parts[0]
            level = parts[2]
            message = ' - '.join(parts[3:])
            return pd.to_datetime(timestamp), level, message, 'SSH'
    except:
        pass
    return None, None, None, None

def parse_http_log(log):
    try:
        log_data = json.loads(log)
        timestamp = datetime.strptime(log_data['asctime'], '%Y-%m-%d %H:%M:%S,%f')
        level = log_data['levelname']
        message = log_data['message']
        
        if message.startswith('LOGIN_ATTEMPT'):
            _, ip, username, password = message.split(',')
            message = f"Login attempt - IP: {ip}, Username: {username}, Password: {password}"
        
        return timestamp, level, message, 'HTTP'
    except:
        return None, None, None, None

st.title('Honeypot Logs')

# Load SSH logs
ssh_logs = load_logs('ssh_honeypot.log')
ssh_data = [parse_ssh_log(log) for log in ssh_logs]

# Load HTTP logs
http_logs = load_logs('http_honeypot.log')
http_data = [parse_http_log(log) for log in http_logs]

# Combine SSH and HTTP logs
all_logs = ssh_data + http_data
df = pd.DataFrame([log for log in all_logs if log[0] is not None], 
                  columns=['Timestamp', 'Level', 'Message', 'Type'])

# Sort the dataframe by timestamp
df = df.sort_values('Timestamp', ascending=False)

# Add a filter for log type
log_type_filter = st.selectbox('Filter by log type:', ['All', 'SSH', 'HTTP'])

# Apply the filter
if log_type_filter != 'All':
    filtered_df = df[df['Type'] == log_type_filter]
else:
    filtered_df = df

# Display the filtered logs
st.header('Honeypot Logs')
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.write("No logs found for the selected filter.")

# Removed the "Login Attempts" section

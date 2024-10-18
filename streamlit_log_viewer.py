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

st.set_page_config(layout="wide")
st.title('Honeypot Logs')

# Load SSH logs
ssh_logs = load_logs('ssh_honeypot.log')
ssh_data = [log for log in (parse_ssh_log(log) for log in ssh_logs) if log[0] is not None]

# Load HTTP logs
http_logs = load_logs('http_honeypot.log')
http_data = [log for log in (parse_http_log(log) for log in http_logs) if log[0] is not None]

# Create separate DataFrames for SSH and HTTP logs
ssh_df = pd.DataFrame(ssh_data, columns=['Timestamp', 'Level', 'Message', 'Type'])
http_df = pd.DataFrame(http_data, columns=['Timestamp', 'Level', 'Message', 'Type'])

# Add a filter for log type
log_type_filter = st.selectbox('Filter by log type:', ['All', 'SSH', 'HTTP'])

# Apply the filter
if log_type_filter == 'SSH':
    filtered_df = ssh_df
elif log_type_filter == 'HTTP':
    filtered_df = http_df
else:
    filtered_df = pd.concat([ssh_df, http_df])

# Sort the dataframe by timestamp
filtered_df = filtered_df.sort_values('Timestamp', ascending=False)

# Display the filtered logs
st.header('Honeypot Logs')
if not filtered_df.empty:
    st.dataframe(
        filtered_df,
        column_config={
            "Timestamp": st.column_config.DatetimeColumn(
                "Timestamp",
                format="DD/MM/YYYY HH:mm:ss",
                width="medium"
            ),
            "Level": st.column_config.TextColumn(
                "Level",
                width="small"
            ),
            "Message": st.column_config.TextColumn(
                "Message",
                width="large"
            ),
            "Type": st.column_config.TextColumn(
                "Type",
                width="small"
            )
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.write("No logs found for the selected filter.")

# Add CSS to make the dataframe scrollable and adjust column widths
st.markdown("""
    <style>
    .stDataFrame {
        min-height: 400px;
        max-height: 600px;
        overflow: auto;
    }
    .dataframe {
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

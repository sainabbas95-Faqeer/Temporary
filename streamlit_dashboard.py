import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="RMS Offline Summary",
    layout="wide"
)

# Load data from CSV
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('DB.csv', encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv('DB.csv', encoding='latin1')
        except UnicodeDecodeError:
            df = pd.read_csv('DB.csv', encoding='cp1252')
    return df

# Function to get current date and time in required format
def get_current_datetime():
    now = datetime.now()
    day = now.strftime("%A")[:3].upper()  # Get day abbreviation (MON, TUE, etc.)
    date_time = now.strftime("| %d-%b-%y | %H:%M:%S")
    return f"{day} {date_time}"

# Load the data
df = load_data()

# Calculate card values
# Card 01: Total Offline on Enfra Domain
total_enfra = len(df[df['Domain'] == 'Enfra'])

# Card 02: Total Offline on SMS LD Domain
total_sms_ld = len(df[df['Domain'] == 'SMS LD'])

# Card 03: Total RMS Offline (Sum of Card 01 + Card 02)
total_rms_offline = total_enfra + total_sms_ld

# Card 04: Total RMS Sites (count all non-empty cells in Site Id column)
total_rms_sites = df['Site Id'].count()

# Create main card with green background
with st.container():
    st.markdown(
        """
        <div style="background-color: #28a745; padding: 25px; border-radius: 15px; margin-bottom: 25px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="text-align: center; flex-grow: 1;">
                    <h1 style="color: white; margin-bottom: 15px; font-weight: 700;">RMS OFFLINE SUMMARY</h1>
                    <h3 style="color: #e8f5e9; margin-bottom: 10px; font-weight: 500;">REMOTE MONITORING SYSTEM - DATA ANALYSIS DASHBOARD</h3>
                    <h5 style="color: #c8e6c9; margin-bottom: 15px; font-weight: 400;">COMPREHENSIVE DATA MANAGEMENT AND MONITORING SYSTEMS</h5>
                    <hr style="border: 0.5px solid #a5d6a7; margin: 15px 0;">
                    <p style="color: #e0f2f1; font-weight: 500; letter-spacing: 0.5px;">SMS LD - A PROJECT OF ENGRO ENFRASHARE</p>
                </div>
                <div style="margin-left: 20px;">
                    <h3 style="color: white; text-align: right; font-weight: 600; min-width: 200px;" id="current-time"></h3>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Create 4 blue color cards below main header card
st.markdown(
    f"""
    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 30px;">
        <div style="flex: 1; min-width: 200px; background-color: #2196F3; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: white; margin-top: 0; margin-bottom: 15px;">TOTAL OFFLINE ON ENFRA DOMAIN</h4>
            <h2 style="color: white; font-size: 2.5em; margin: 0;">{total_enfra}</h2>
        </div>
        <div style="flex: 1; min-width: 200px; background-color: #2196F3; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: white; margin-top: 0; margin-bottom: 15px;">TOTAL OFFLINE ON SMS LD DOMAIN</h4>
            <h2 style="color: white; font-size: 2.5em; margin: 0;">{total_sms_ld}</h2>
        </div>
        <div style="flex: 1; min-width: 200px; background-color: #2196F3; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: white; margin-top: 0; margin-bottom: 15px;">TOTAL RMS OFFLINE</h4>
            <h2 style="color: white; font-size: 2.5em; margin: 0;">{total_rms_offline}</h2>
        </div>
        <div style="flex: 1; min-width: 200px; background-color: #2196F3; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: white; margin-top: 0; margin-bottom: 15px;">TOTAL RMS SITES</h4>
            <h2 style="color: white; font-size: 2.5em; margin: 0;">{total_rms_sites}</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Display current time with auto-refresh
current_time = get_current_datetime()
st.markdown(f"""
    <script>
        document.getElementById('current-time').innerHTML = '{current_time}';
        setInterval(function() {{
            const now = new Date();
            const day = now.toLocaleString('en-US', {{ weekday: 'short' }}).toUpperCase();
            const date = now.toLocaleString('en-US', {{ day: '2-digit', month: 'short', year: '2-digit' }}).replace(/\\//g, '-');
            const time = now.toLocaleString('en-US', {{ hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }});
            document.getElementById('current-time').innerHTML = day + ' | ' + date + ' | ' + time;
        }}, 1000);
    </script>
""", unsafe_allow_html=True)
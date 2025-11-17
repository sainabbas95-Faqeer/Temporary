import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="RMS Offline Summary",
    layout="wide"
)

# Function to get current date and time in required format
def get_current_datetime():
    now = datetime.now()
    day = now.strftime("%A")[:3].upper()  # Get day abbreviation (MON, TUE, etc.)
    date_time = now.strftime("| %d-%b-%y | %H:%M:%S")
    return f"{day} {date_time}"

# Create main card with green background
with st.container():
    st.markdown(
        """
        <div style="background-color: #28a745; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="color: white; margin-bottom: 10px;">RMS OFFLINE SUMMARY</h1>
                    <h3 style="color: #e0e0e0; margin-bottom: 5px;">Remote Monitoring System - Data Analysis Dashboard</h3>
                    <h5 style="color: #e0e0e0; margin-bottom: 10px;">Comprehensive Data Management And Monitoring Systems</h5>
                    <p style="color: #f0f0f0;">SMS LD - A Project Of Engro Enfrashare</p>
                </div>
                <div>
                    <h3 style="color: white; text-align: right;" id="current-time"></h3>
                </div>
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

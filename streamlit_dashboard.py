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

# Create the header section
col1, col2 = st.columns([10, 2])

with col1:
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>RMS OFFLINE SUMMARY</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #17becf;'>Remote Monitoring System - Data Analysis Dashboard</h4>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: white;'>Comprehensive Data Management And Monitoring Systems</h6>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6c757d;'>SMS LD - A Project Of Engro Enfrashare</p>", unsafe_allow_html=True)

with col2:
    # Display current time
    current_time = get_current_datetime()
    st.markdown(f"<h3 style='text-align: right; color: white;'>{current_time}</h3>", unsafe_allow_html=True)
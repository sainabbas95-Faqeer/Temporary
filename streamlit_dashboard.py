import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go

# Set the page configuration
st.set_page_config(
    page_title="RMS Offline Summary",
    page_icon="📊",
    layout="wide"
)

# Display the main headers
st.markdown("<h1 style='text-align: center;'>RMS OFFLINE SUMMARY</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Remote Monitoring System - Data Analysis Dashboard</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Comprehensive Data Management And Monitoring Systems</h5>", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('DB.csv')
        return df
    except FileNotFoundError:
        st.error("DB.csv file not found. Please make sure the file exists in the current directory.")
        return pd.DataFrame()

# Load data
df = load_data()

if not df.empty:
    # Data preprocessing
    df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces from column names
    
    # Convert 'Offline Date' to datetime
    df['Offline Date'] = pd.to_datetime(df['Offline Date'], errors='coerce')
    
    # Fill NaN values in 'Days Passed' with 0
    df['Days Passed'] = df['Days Passed'].fillna(0)
    
    # Create Aging categories for better visualization
    df['Aging Category'] = df['Aging'].fillna('Unknown')
    
    # Create summary dataframes for visualizations
    device_counts_brand = df['Device Brand'].value_counts().reset_index()
    device_counts_brand.columns = ['Device Brand', 'Count']
    
    device_counts_region = df['Sub Region'].value_counts().reset_index()
    device_counts_region.columns = ['Sub Region', 'Count']
    
    device_counts_reason = df['Reason'].fillna('Unknown').value_counts().reset_index()
    device_counts_reason.columns = ['Reason', 'Count']
    
    device_counts_aging = df['Aging Category'].value_counts().reset_index()
    device_counts_aging.columns = ['Aging Category', 'Count']
    
    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Devices", len(df))
    
    with col2:
        avg_days = round(df['Days Passed'].mean(), 1)
        st.metric("Avg. Days Offline", avg_days)
    
    with col3:
        critical_count = len(df[df['Aging Category'] == '100+ Days'])
        st.metric("Critical (>100 Days)", critical_count)
    
    with col4:
        most_common_reason = df['Reason'].fillna('Unknown').mode()
        if not most_common_reason.empty:
            st.metric("Most Common Issue", most_common_reason.iloc[0])
        else:
            st.metric("Most Common Issue", "N/A")
    
    # Create visualizations
    st.markdown("---")
    
    # Row 1: Device Brand Distribution and Aging Category Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig_brand = px.pie(device_counts_brand, values='Count', names='Device Brand', 
                          title='Distribution of Offline Devices by Brand')
        st.plotly_chart(fig_brand, use_container_width=True)
    
    with col2:
        fig_aging = px.bar(device_counts_aging, x='Aging Category', y='Count',
                          title='Distribution of Devices by Aging Category',
                          color='Aging Category')
        st.plotly_chart(fig_aging, use_container_width=True)
    
    # Row 2: Top Reasons for Offline Status
    st.markdown("---")
    top_reasons = device_counts_reason.head(10)
    fig_reasons = px.bar(top_reasons, x='Count', y='Reason', orientation='h',
                        title='Top 10 Reasons for Device Offline Status')
    st.plotly_chart(fig_reasons, use_container_width=True)
    
    # Row 3: Devices by Region
    st.markdown("---")
    fig_region = px.bar(device_counts_region, x='Sub Region', y='Count',
                       title='Offline Devices by Region',
                       color='Sub Region')
    st.plotly_chart(fig_region, use_container_width=True)
    
    # Row 4: 3D Scatter Plot
    st.markdown("---")
    fig_3d = px.scatter_3d(df, x='Days Passed', y='Device Brand', z='Sub Region',
                          color='Aging Category', size='Days Passed',
                          title='3D View of Offline Devices by Days, Brand, and Region',
                          hover_data=['Site Id', 'Reason'])
    st.plotly_chart(fig_3d, use_container_width=True)

# Get current date and time
now = datetime.now()
day = now.strftime("%A")[:3].upper()  # Get day abbreviation (MON, TUE, etc.)
date_time = now.strftime("| %d-%b-%y | %H:%M:%S")
current_time = f"{day} {date_time}"

# Display the time
st.markdown(f"<h4 style='text-align: right; color: #1f77b4;'>{current_time}</h4>", unsafe_allow_html=True)

# Display the footer
st.markdown("<p style='text-align: center; margin-top: 50px; color: #888;'>SMS LD - A Project Of Engro Enfrashare</p>", unsafe_allow_html=True)
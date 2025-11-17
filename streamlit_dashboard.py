import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="Welcome to RMS Interactive Dashboard",
    layout="wide"
)

# Load data from CSV files
@st.cache_data
def load_data():
    try:
        # Load all CSV files
        db_data = pd.read_csv('DB.csv', encoding='utf-8')
        dse_data = pd.read_csv('DSE.csv', encoding='utf-8')
        locations_data = pd.read_csv('Locations.csv', encoding='utf-8')
        rectifier_data = pd.read_csv('Rectifier.csv', encoding='utf-8')
        spd_data = pd.read_csv('SPD.csv', encoding='utf-8')
        events_data = pd.read_csv('events.csv', encoding='utf-8')
        tenant_data = pd.read_csv('tenant.csv', encoding='utf-8')
        dc_cts_data = pd.read_csv('DC CTs and SPDs.csv', encoding='utf-8')
        
        return {
            'db': db_data,
            'dse': dse_data,
            'locations': locations_data,
            'rectifier': rectifier_data,
            'spd': spd_data,
            'events': events_data,
            'tenant': tenant_data,
            'dc_cts': dc_cts_data
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Function to get current date and time in required format
def get_current_datetime():
    now = datetime.now()
    day = now.strftime("%A")[:3].upper()  # Get day abbreviation (MON, TUE, etc.)
    date_time = now.strftime("| %d-%b-%y | %H:%M:%S")
    return f"{day} {date_time}"

# Load the data
data = load_data()

# Custom CSS for the dashboard
st.markdown("""
<style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #1a2a6c, #b21f1f, #1a2a6c);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #fff;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Time display in top right corner */
    .current-time {
        position: fixed;
        top: 15px;
        right: 15px;
        background: rgba(0, 0, 0, 0.3);
        padding: 12px 20px;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: bold;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        color: white;
    }

    /* Welcome header */
    .welcome-header {
        text-align: center;
        padding: 30px 10px 20px 10px;
        margin-bottom: 20px;
    }

    .welcome-header h1 {
        font-size: 2.8rem;
        margin-bottom: 12px;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
        color: white;
        animation: colorShift 8s infinite alternate;
    }

    @keyframes colorShift {
        0% { color: #ffffff; }
        50% { color: #f0f0f0; }
        100% { color: #e0e0e0; }
    }

    .welcome-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        max-width: 800px;
        margin: 0 auto 15px;
        color: white;
    }

    /* SMS LD project text */
    .project-text {
        font-size: 1.2rem;
        font-weight: bold;
        color: rgba(255, 255, 255, 0.8);
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.3);
        animation: float 4s ease-in-out infinite;
        margin-top: 8px;
        letter-spacing: 1px;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }

    /* Buttons grid */
    .buttons-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-auto-rows: auto;
        gap: 15px;
        padding: 10px;
        max-width: 1200px;
        margin: 0 auto 20px;
        justify-items: center;
        align-items: center;
    }

    /* Interactive button */
    .interactive-button {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        animation: floating 3s ease-in-out infinite;
        min-height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-decoration: none;
    }

    .interactive-button:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        background: rgba(255, 255, 255, 0.2);
    }

    .button-icon {
        font-size: 1.8rem;
        margin-bottom: 12px;
        filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.3));
    }

    .button-text {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .button-description {
        font-size: 0.8rem;
        opacity: 0.9;
        margin-bottom: 12px;
    }

    .construction-badge {
        display: inline-block;
        background: rgba(255, 215, 0, 0.2);
        color: gold;
        padding: 2px 6px;
        border-radius: 12px;
        font-size: 0.65rem;
        font-weight: bold;
        border: 1px solid gold;
    }

    /* Floating animation */
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }

    /* Staggered animation delays */
    .button-1 { animation-delay: 0s; }
    .button-2 { animation-delay: 0.1s; }
    .button-3 { animation-delay: 0.2s; }
    .button-4 { animation-delay: 0.3s; }
    .button-5 { animation-delay: 0.4s; }
    .button-6 { animation-delay: 0.5s; }
    .button-7 { animation-delay: 0.6s; }
    .button-8 { animation-delay: 0.7s; }
    .button-9 { animation-delay: 0.8s; }
    .button-10 { animation-delay: 0.9s; }
    .button-11 { animation-delay: 1.0s; }
    .button-12 { animation-delay: 1.1s; }

    /* Under construction section */
    .under-construction {
        text-align: center;
        padding: 20px;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        margin: 20px auto;
        max-width: 700px;
    }

    .under-construction h2 {
        font-size: 1.5rem;
        margin-bottom: 12px;
        color: gold;
    }

    .construction-icon {
        font-size: 2.5rem;
        color: gold;
        margin-bottom: 12px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 20px;
        font-size: 0.8rem;
        opacity: 0.7;
        color: white;
    }

    /* Mobile responsiveness */
    @media (max-width: 1024px) {
        .buttons-grid {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    @media (min-width: 1025px) {
        .buttons-grid {
            grid-template-columns: repeat(4, 1fr);
        }
    }

    @media (max-width: 768px) {
        .buttons-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }
        
        .welcome-header h1 {
            font-size: 2rem;
        }
        
        .welcome-header p {
            font-size: 0.9rem;
        }
        
        .project-text {
            font-size: 1rem;
        }
        
        .interactive-button {
            min-height: 110px;
        }
        
        .button-text {
            font-size: 0.9rem;
        }
        
        .button-description {
            font-size: 0.65rem;
        }
    }

    @media (max-width: 480px) {
        .buttons-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .welcome-header h1 {
            font-size: 1.7rem;
        }
        
        .welcome-header p {
            font-size: 0.8rem;
        }
        
        .project-text {
            font-size: 0.9rem;
        }
        
        .button-text {
            font-size: 0.8rem;
        }
        
        .button-description {
            font-size: 0.6rem;
        }
    }
    
    /* Fix for Streamlit's column layout */
    .stMarkdown div[data-testid="stMarkdownContainer"] {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Current time display
current_time_placeholder = st.empty()
current_time_placeholder.markdown(f'<div class="current-time" id="currentTime">{get_current_datetime()}</div>', unsafe_allow_html=True)

# Welcome header
st.markdown("""
<div class="welcome-header">
    <h1>Welcome To The Interactive World</h1>
    <p>Your Gateway To Comprehensive Data Management And Monitoring Systems</p>
    <div class="project-text">SMS LD - A Project Of Engro Enfrashare</div>
</div>
""", unsafe_allow_html=True)

# Create buttons using Streamlit columns for better compatibility
st.markdown("### Available Databases", unsafe_allow_html=True)

# Create a grid using Streamlit columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <a href="#" class="interactive-button button-1" onclick="alert('RMS data base will be available soon!')">
        <div class="button-icon">
            <i class="fas fa-database"></i>
        </div>
        <div class="button-text">RMS data base</div>
        <div class="button-description">Access the main Remote Monitoring System database</div>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="#" class="interactive-button button-2" onclick="alert('All Active Alarms Database will be available soon!')">
        <div class="button-icon">
            <i class="fas fa-bell"></i>
        </div>
        <div class="button-text">All Active Alarms Database</div>
        <div class="button-description">View all current active system alarms</div>
    </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <a href="#" class="interactive-button button-3" onclick="alert('🚧 Gallery is currently under construction.\\n\\nData for this module will be available soon.\\nPlease check back later.')">
        <div class="button-icon">
            <i class="fas fa-images"></i>
        </div>
        <div class="button-text">Gallery</div>
        <div class="button-description">View system images and diagrams</div>
        <div class="construction-badge">Under Construction</div>
    </a>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <a href="#" class="interactive-button button-4" onclick="alert('RMS Brands Site wise will be available soon!')">
        <div class="button-icon">
            <i class="fas fa-map-marker-alt"></i>
        </div>
        <div class="button-text">RMS Brands Site wise</div>
        <div class="button-description">View RMS brands organized by site locations</div>
    </a>
    """, unsafe_allow_html=True)

# Second row
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown("""
    <a href="#" class="interactive-button button-5" onclick="alert('🚧 Site SIMs is currently under construction.\\n\\nData for this module will be available soon.\\nPlease check back later.')">
        <div class="button-icon">
            <i class="fas fa-sim-card"></i>
        </div>
        <div class="button-text">Site SIMs</div>
        <div class="button-description">Manage SIM cards assigned to different sites</div>
        <div class="construction-badge">Under Construction</div>
    </a>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <a href="#" class="interactive-button button-6" onclick="alert('Tasks / Activities will be available soon!')">
        <div class="button-icon">
            <i class="fas fa-tasks"></i>
        </div>
        <div class="button-text">Tasks / Activities</div>
        <div class="button-description">Manage and track all system tasks and activities</div>
    </a>
    """, unsafe_allow_html=True)

with col7:
    st.markdown("""
    <a href="#" class="interactive-button button-7" onclick="alert('Mapping will be available soon!')">
        <div class="button-icon">
            <i class="fas fa-map-marked-alt"></i>
        </div>
        <div class="button-text">Mapping</div>
        <div class="button-description">View site locations on interactive map</div>
    </a>
    """, unsafe_allow_html=True)

with col8:
    st.markdown("""
    <a href="#" class="interactive-button button-8" onclick="alert('Tenants Information will be available soon!')">
        <div class="button-icon">
            <i class="fas fa-mobile-alt"></i>
        </div>
        <div class="button-text">Tenants Information</div>
        <div class="button-description">View mobile operators mapping data</div>
    </a>
    """, unsafe_allow_html=True)

# Under construction notice
st.markdown("""
<div class="under-construction">
    <div class="construction-icon">
        <i class="fas fa-hard-hat"></i>
    </div>
    <h2>Under Construction</h2>
    <p>Additional database modules are currently being developed and will be available soon.</p>
    <p>Please check back later for updates.</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>RMS Interactive Dashboard &copy; 2025 Abbas Enterprises</p>
</div>
""", unsafe_allow_html=True)

# Font Awesome for icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Update time every second
def update_time():
    while True:
        time.sleep(1)
        current_time_placeholder.markdown(f'<div class="current-time" id="currentTime">{get_current_datetime()}</div>', unsafe_allow_html=True)

# Run the time update in a separate thread
import threading
time_thread = threading.Thread(target=update_time, daemon=True)
time_thread.start()
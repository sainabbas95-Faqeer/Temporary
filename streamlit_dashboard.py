try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from datetime import datetime, timedelta
import time

# Check if required packages are available
if not STREAMLIT_AVAILABLE:
    print("Streamlit is not installed. Please install it using:")
    print("pip install streamlit")
    print("\nAfter installing, run the dashboard with:")
    print("streamlit run streamlit_dashboard.py")
else:
    def run_dashboard():
        # Set the page configuration
        st.set_page_config(
            page_title="Welcome to RMS Interactive Dashboard",
            page_icon="📊",
            layout="wide"
        )

        # Add custom CSS for styling
        st.markdown("""
        <style>
            .main-header {
                text-align: center;
                padding: 30px 10px 20px 10px;
                margin-bottom: 20px;
            }
            
            .main-header h1 {
                font-size: 2.8rem;
                margin-bottom: 12px;
                color: white;
                text-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
            }
            
            .main-header p {
                font-size: 1.1rem;
                opacity: 0.9;
                max-width: 800px;
                margin: 0 auto 15px;
            }
            
            .project-text {
                font-size: 1.2rem;
                font-weight: bold;
                color: rgba(255, 255, 255, 0.8);
                text-shadow: 0 0 8px rgba(255, 255, 255, 0.3);
                margin-top: 8px;
                letter-spacing: 1px;
            }
            
            .buttons-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                padding: 10px;
                max-width: 1200px;
                margin: 0 auto 20px;
            }
            
            .interactive-button {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 15px;
                text-align: center;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                border: 1px solid rgba(255, 255, 255, 0.1);
                position: relative;
                overflow: hidden;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
                min-height: 130px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            
            .button-icon {
                font-size: 1.8rem;
                margin-bottom: 12px;
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
            
            .under-construction {
                text-align: center;
                padding: 20px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 12px;
                margin: 20px auto;
                max-width: 700px;
            }
            
            .construction-icon {
                font-size: 2.5rem;
                color: gold;
                margin-bottom: 12px;
            }
            
            .footer {
                text-align: center;
                padding: 20px;
                margin-top: 20px;
                font-size: 0.8rem;
                opacity: 0.7;
            }
            
            .setup-instructions {
                max-width: 800px;
                margin: 30px auto;
                padding: 20px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 12px;
                border-left: 4px solid #1f77b4;
            }
            
            .setup-instructions h2 {
                color: #1f77b4;
                margin-bottom: 15px;
            }
            
            .setup-instructions code {
                background: rgba(0, 0, 0, 0.3);
                padding: 2px 6px;
                border-radius: 4px;
                font-family: monospace;
            }
            
            .setup-instructions pre {
                background: rgba(0, 0, 0, 0.3);
                padding: 15px;
                border-radius: 8px;
                overflow-x: auto;
            }
            
            /* Mobile responsiveness */
            @media (max-width: 1024px) {
                .buttons-grid {
                    grid-template-columns: repeat(3, 1fr);
                }
            }
            
            @media (max-width: 768px) {
                .buttons-grid {
                    grid-template-columns: repeat(2, 1fr);
                    gap: 12px;
                }
                
                .main-header h1 {
                    font-size: 2rem;
                }
                
                .main-header p {
                    font-size: 0.9rem;
                }
            }
            
            @media (max-width: 480px) {
                .buttons-grid {
                    grid-template-columns: 1fr;
                }
                
                .main-header h1 {
                    font-size: 1.7rem;
                }
            }
        </style>
        """, unsafe_allow_html=True)

        # Display the main header
        st.markdown("""
        <div class="main-header">
            <h1>Welcome To The Interactive World</h1>
            <p>Your Gateway To Comprehensive Data Management And Monitoring Systems</p>
            <div class="project-text">SMS LD - A Project Of Engro Enfrashare</div>
        </div>
        """, unsafe_allow_html=True)

        # Check for missing packages and display instructions
        missing_packages = []
        if not PANDAS_AVAILABLE:
            missing_packages.append("pandas")
        if not PLOTLY_AVAILABLE:
            missing_packages.append("plotly")

        if missing_packages:
            st.warning(f"The following required packages are not installed: {', '.join(missing_packages)}")
            st.info("Some features may not work correctly. Please install the missing packages.")

        # Create buttons grid
        st.markdown('<div class="buttons-grid">', unsafe_allow_html=True)

        # Create columns for the buttons
        col1, col2, col3, col4 = st.columns(4)

        # Button 01: RMS data base
        with col1:
            st.markdown("""
            <div class="interactive-button" style="border-top: 3px solid linear-gradient(90deg, #ff8a00, #da1b60);">
                <div class="button-icon">📊</div>
                <div class="button-text">RMS data base</div>
                <div class="button-description">Access the main Remote Monitoring System database</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Button 02: All Active Alarms Database
        with col2:
            st.markdown("""
            <div class="interactive-button" style="border-top: 3px solid linear-gradient(90deg, #00c9ff, #92fe9d);">
                <div class="button-icon">🔔</div>
                <div class="button-text">All Active Alarms Database</div>
                <div class="button-description">View all current active system alarms</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Button 03: Gallery
        with col3:
            st.markdown("""
            <div class="interactive-button" style="border-top: 3px solid linear-gradient(90deg, #f857a6, #ff5858);">
                <div class="button-icon">🖼️</div>
                <div class="button-text">Gallery</div>
                <div class="button-description">View system images and diagrams</div>
                <div class="construction-badge">Under Construction</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Button 04: RMS Brands Site wise
        with col4:
            st.markdown("""
            <div class="interactive-button" style="border-top: 3px solid linear-gradient(90deg, #3a7bd5, #00d2ff);">
                <div class="button-icon">📍</div>
                <div class="button-text">RMS Brands Site wise</div>
                <div class="button-description">View RMS brands organized by site locations</div>
            </div>
            """, unsafe_allow_html=True)

        # Second row of buttons
        col5, col6, col7, col8 = st.columns(4)

        # Button 05: Site SIMs
        with col5:
            st.markdown("""
            <div class="interactive-button" style="border-top: 3px solid linear-gradient(90deg, #56ab2f, #a8e063);">
                <div class="button-icon">📱</div>
                <div class="button-text">Site SIMs</div>
                <div class="button-description">Manage SIM cards assigned to different sites</div>
                <div class="construction-badge">Under Construction</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Button 06: Tasks / Activities
        with col6:
            st.markdown("""
            <div class="interactive-button" style="border-top: 3px solid linear-gradient(90deg, #6a11cb, #2575fc);">
                <div class="button-icon">✅</div>
                <div class="button-text">Tasks / Activities</div>
                <div class="button-description">Manage and track all system tasks and activities</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Button 07: Mapping
        with col7:
            st.markdown("""
            <div class="interactive-button" style="border-top: 3px solid linear-gradient(90deg, #ff416c, #ff4b2b);">
                <div class="button-icon">🗺️</div>
                <div class="button-text">Mapping</div>
                <div class="button-description">View site locations on interactive map</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Button 08: Tenants Information
        with col8:
            st.markdown("""
            <div class="interactive-button" style="border-top: 3px solid linear-gradient(90deg, #8e2de2, #4a00e0);">
                <div class="button-icon">📞</div>
                <div class="button-text">Tenants Information</div>
                <div class="button-description">View mobile operators mapping data</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Under construction notice
        st.markdown("""
        <div class="under-construction">
            <div class="construction-icon">🚧</div>
            <h2>Under Construction</h2>
            <p>Additional database modules are currently being developed and will be available soon.</p>
            <p>Please check back later for updates.</p>
        </div>
        """, unsafe_allow_html=True)

        # Setup instructions
        st.markdown("""
        <div class="setup-instructions">
            <h2>Setup Instructions</h2>
            <p>To run this dashboard properly, please ensure you have all required packages installed:</p>
            <pre>pip install streamlit pandas plotly</pre>
            <p>After installing the packages, run the dashboard with:</p>
            <pre>streamlit run streamlit_dashboard.py</pre>
            <p>If you're using a virtual environment, make sure it's activated before installing packages.</p>
        </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div class="footer">
            <p>RMS Interactive Dashboard &copy; 2025 Abbas Enterprises</p>
        </div>
        """, unsafe_allow_html=True)

        # Display current time
        current_time = datetime.now().strftime("%A, %B %d, %Y | %I:%M:%S %p")
        st.sidebar.markdown(f"<div style='text-align: right; font-weight: bold; padding: 12px; background: rgba(0,0,0,0.3); border-radius: 12px;'>{current_time}</div>", unsafe_allow_html=True)
    
    # Run the dashboard
    run_dashboard()
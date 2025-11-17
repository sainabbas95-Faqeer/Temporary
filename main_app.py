import streamlit as st

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# Page routing
if st.session_state.page == 'main':
    # Run the main dashboard
    exec(open('streamlit_dashboard.py').read())
elif st.session_state.page == 'rms_database':
    # Run the RMS database page
    exec(open('rms_database.py').read())
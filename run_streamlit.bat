@echo off
echo Installing required packages...
pip install -r requirements.txt
echo.
echo Starting Streamlit dashboard...
echo.
echo Open your browser to http://localhost:8501
echo.
streamlit run streamlit_dashboard.py
pause
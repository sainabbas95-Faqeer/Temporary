@echo off
echo Installing/updating required Python packages for RMS Dashboard...
echo.

echo Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Installing core packages...
python -m pip install streamlit pandas plotly toml cachetools tornado
echo.

echo Starting Streamlit dashboard...
echo.
echo Open your browser to http://localhost:8501
echo.
streamlit run streamlit_dashboard.py
echo.

pause
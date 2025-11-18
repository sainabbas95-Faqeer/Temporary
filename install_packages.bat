@echo off
echo Installing required Python packages for RMS Dashboard...
echo.

echo Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Installing pandas...
python -m pip install pandas
echo.

echo Installing plotly...
python -m pip install plotly
echo.

echo Installing dash...
python -m pip install dash
echo.

echo Installing dash-bootstrap-components...
python -m pip install dash-bootstrap-components
echo.

echo Installing numpy...
python -m pip install numpy
echo.

echo Installing additional Streamlit dependencies...
python -m pip install toml cachetools tornado
echo.

echo Installation complete!
echo.
echo To run the dashboard, execute:
echo streamlit run streamlit_dashboard.py
echo.
echo Then open your browser to http://localhost:8501
echo.
pause
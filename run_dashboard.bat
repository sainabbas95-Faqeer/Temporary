@echo off
echo Starting RMS Offline Devices Dashboard...
echo.
echo Make sure you have installed all required packages first:
echo pip install pandas plotly dash dash-bootstrap-components numpy
echo.
echo Starting dashboard server...
echo.
echo Open your browser to http://localhost:8050
echo.
echo Press CTRL+C to stop the server
echo.
python rms_dashboard.py
pause
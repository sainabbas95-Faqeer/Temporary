# RMS Offline Devices Dashboard

A 3D, colorful, highly interactive dashboard for monitoring RMS (Remote Monitoring System) offline devices with multi-variation analysis reports and graphs.

## Features

- **3D Visualizations**: Interactive 3D scatter plots showing device distribution by days offline, brand, and region
- **Real-time Filtering**: Filter data by region, device brand, and aging category
- **Key Performance Indicators**: Dashboard widgets showing total devices, average days offline, most common issues, and critical devices
- **Multi-variation Analysis**: Charts and graphs showing device distribution across different categories
- **Responsive Design**: Works on desktop and mobile devices
- **Colorful Interface**: Modern dark theme with vibrant data visualizations

## Data Source

The dashboard uses data from `DB.csv` which contains information about RMS offline devices including:
- Site ID
- Device Brand
- Sub Region
- Cluster
- Team Lead
- ES POC
- Offline Date
- Days Passed
- Aging Category
- Reason for Offline Status

## Installation

### Method 1: Using the Installation Script (Windows)

1. Double-click on `install_packages.bat` to automatically install all required packages
2. Wait for the installation to complete

### Method 2: Manual Installation

1. Open a terminal/command prompt
2. Run the following command:
   ```
   pip install pandas plotly dash dash-bootstrap-components numpy
   ```
   OR
   ```
   python -m pip install pandas plotly dash dash-bootstrap-components numpy
   ```

## Running the Dashboard

### Method 1: Using the Run Script (Windows)

1. Double-click on `run_dashboard.bat` to start the dashboard
2. Open your web browser and go to `http://localhost:8050`

### Method 2: Manual Execution

1. Open a terminal/command prompt
2. Navigate to the project directory
3. Run the following command:
   ```
   python dashboard_fixed.py
   ```
4. Open your web browser and go to `http://localhost:8050`

## Dashboard Components

1. **Filters Panel** (Left side):
   - Sub Region filter
   - Device Brand filter
   - Aging Category filter

2. **KPI Cards** (Top):
   - Total Devices
   - Average Days Offline
   - Most Common Issue
   - Critical Devices (>100 Days)

3. **Visualizations**:
   - 3D Scatter Plot: Shows device distribution in 3D space
   - Device Brand Pie Chart: Distribution of devices by brand
   - Aging Category Histogram: Distribution by aging categories
   - Top 10 Reasons Bar Chart: Most common reasons for offline status

## Customization

You can customize the dashboard by modifying `dashboard_fixed.py`:
- Change color schemes
- Modify filters
- Add new visualizations
- Adjust layout components

## Troubleshooting

If you encounter issues:

1. Make sure all required packages are installed
2. Check that `DB.csv` is in the same directory as the script
3. Ensure you're using Python 3.7 or higher
4. Check the terminal output for any error messages
5. If `rms_dashboard.py` doesn't work, use `dashboard_fixed.py` instead

## Requirements

- Python 3.7+
- pandas >= 1.3.0
- plotly >= 5.0.0
- dash >= 2.0.0
- dash-bootstrap-components >= 1.0.0
- numpy >= 1.20.0
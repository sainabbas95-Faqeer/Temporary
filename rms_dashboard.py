import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from datetime import datetime
import numpy as np

# Load the data with proper encoding
try:
    df = pd.read_csv('DB.csv', encoding='utf-8', on_bad_lines='skip')
except UnicodeDecodeError:
    try:
        df = pd.read_csv('DB.csv', encoding='latin1', on_bad_lines='skip')
    except UnicodeDecodeError:
        df = pd.read_csv('DB.csv', encoding='cp1252', on_bad_lines='skip')

# Data preprocessing
df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces from column names

# Convert 'Offline Date' to datetime
df['Offline Date'] = pd.to_datetime(df['Offline Date'], errors='coerce')

# Fill NaN values in 'Days Passed' with 0
df['Days Passed'] = df['Days Passed'].fillna(0)

# Create Aging categories for better visualization
df['Aging Category'] = df['Aging'].fillna('Unknown')

# Initialize the Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Function to get current date and time in required format
def get_current_datetime():
    now = datetime.now()
    day = now.strftime("%A")[:3].upper()  # Get day abbreviation (MON, TUE, etc.)
    date_time = now.strftime("| %d-%b-%y | %H:%M:%S")
    return f"{day} {date_time}"

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("RMS OFFLINE SUMMARY", className="text-center text-primary mb-0"),
            html.H4("Remote Monitoring System - Data Analysis Dashboard", className="text-center text-info mb-0"),
            html.H6("Comprehensive Data Management And Monitoring Systems", className="text-center text-light mb-0"),
            html.Hr(className="my-2"),
            html.P("SMS LD - A Project Of Engro Enfrashare", className="text-center text-muted mb-0")
        ], width=10),
        dbc.Col([
            html.Div(id='current-time', className="text-right text-light font-weight-bold")
        ], width=2)
    ]),
    
    # Interval component to update time every second
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Update every second
        n_intervals=0
    )
], fluid=True)

# Callback to update the current time
@callback(
    Output('current-time', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_time(n):
    return get_current_datetime()

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
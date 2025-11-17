import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from datetime import datetime
import numpy as np

try:
    # Load the data
    df = pd.read_csv('DB.csv')
    
    # Data preprocessing
    df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces from column names
    
    # Convert 'Offline Date' to datetime
    df['Offline Date'] = pd.to_datetime(df['Offline Date'], errors='coerce')
    
    # Fill NaN values in 'Days Passed' with 0
    df['Days Passed'] = df['Days Passed'].fillna(0)
    
    # Create Aging categories for better visualization
    df['Aging Category'] = df['Aging'].fillna('Unknown')
    
    # Create a summary dataframe for device counts by various categories
    device_counts_brand = df['Device Brand'].value_counts().reset_index()
    device_counts_brand.columns = ['Device Brand', 'Count']
    
    device_counts_region = df['Sub Region'].value_counts().reset_index()
    device_counts_region.columns = ['Sub Region', 'Count']
    
    device_counts_reason = df['Reason'].fillna('Unknown').value_counts().reset_index()
    device_counts_reason.columns = ['Reason', 'Count']
    
    device_counts_aging = df['Aging Category'].value_counts().reset_index()
    device_counts_aging.columns = ['Aging Category', 'Count']
    
    # Initialize the Dash app with Bootstrap theme
    app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
    
    # App layout
    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("RMS Offline Devices Dashboard", className="text-center text-primary mb-4"), width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                html.H5("Filters"),
                html.Label("Select Sub Region:"),
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': region, 'value': region} for region in df['Sub Region'].dropna().unique()],
                    value=df['Sub Region'].dropna().unique().tolist(),
                    multi=True
                ),
                html.Br(),
                html.Label("Select Device Brand:"),
                dcc.Dropdown(
                    id='brand-dropdown',
                    options=[{'label': brand, 'value': brand} for brand in df['Device Brand'].dropna().unique()],
                    value=df['Device Brand'].dropna().unique().tolist(),
                    multi=True
                ),
                html.Br(),
                html.Label("Select Aging Category:"),
                dcc.Dropdown(
                    id='aging-dropdown',
                    options=[{'label': aging, 'value': aging} for aging in df['Aging Category'].dropna().unique()],
                    value=df['Aging Category'].dropna().unique().tolist(),
                    multi=True
                )
            ], width=3),
            
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Total Devices", className="card-title"),
                                html.H2(id="total-devices", className="card-text text-success")
                            ])
                        ], color="dark", inverse=True)
                    ], width=3),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Avg. Days Offline", className="card-title"),
                                html.H2(id="avg-days", className="card-text text-warning")
                            ])
                        ], color="dark", inverse=True)
                    ], width=3),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Most Common Issue", className="card-title"),
                                html.H2(id="common-issue", className="card-text text-danger")
                            ])
                        ], color="dark", inverse=True)
                    ], width=3),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Critical (>100 Days)", className="card-title"),
                                html.H2(id="critical-count", className="card-text text-info")
                            ])
                        ], color="dark", inverse=True)
                    ], width=3)
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='3d-scatter-plot')
                    ], width=12)
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='device-brand-pie')
                    ], width=6),
                    
                    dbc.Col([
                        dcc.Graph(id='aging-category-histogram')
                    ], width=6)
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='reason-bar-chart')
                    ], width=12)
                ])
            ], width=9)
        ])
    ], fluid=True)
    
    # Callbacks for interactivity
    @callback(
        [Output('total-devices', 'children'),
         Output('avg-days', 'children'),
         Output('common-issue', 'children'),
         Output('critical-count', 'children'),
         Output('3d-scatter-plot', 'figure'),
         Output('device-brand-pie', 'figure'),
         Output('aging-category-histogram', 'figure'),
         Output('reason-bar-chart', 'figure')],
        [Input('region-dropdown', 'value'),
         Input('brand-dropdown', 'value'),
         Input('aging-dropdown', 'value')]
    )
    def update_dashboard(selected_regions, selected_brands, selected_aging):
        # Filter the dataframe based on selections
        filtered_df = df.copy()
        
        if selected_regions:
            if isinstance(selected_regions, str):
                selected_regions = [selected_regions]
            filtered_df = filtered_df[filtered_df['Sub Region'].isin(selected_regions)]
        
        if selected_brands:
            if isinstance(selected_brands, str):
                selected_brands = [selected_brands]
            filtered_df = filtered_df[filtered_df['Device Brand'].isin(selected_brands)]
        
        if selected_aging:
            if isinstance(selected_aging, str):
                selected_aging = [selected_aging]
            filtered_df = filtered_df[filtered_df['Aging Category'].isin(selected_aging)]
        
        # Calculate KPIs
        total_devices = len(filtered_df)
        avg_days_offline = round(filtered_df['Days Passed'].mean(), 1) if not filtered_df.empty else 0
        critical_count = len(filtered_df[filtered_df['Aging Category'] == '100+ Days'])
        
        # Most common issue
        common_issue = filtered_df['Reason'].fillna('Unknown').mode()
        if not common_issue.empty:
            common_issue = common_issue.iloc[0]
        else:
            common_issue = "N/A"
        
        # 3D Scatter Plot
        fig_3d = go.Figure()
        
        if not filtered_df.empty:
            # Create a 3D scatter plot with Days Passed, Device Brand, and Reason
            fig_3d = px.scatter_3d(
                filtered_df,
                x='Days Passed',
                y='Device Brand',
                z='Sub Region',
                color='Aging Category',
                size='Days Passed',
                hover_data=['Site Id', 'Reason'],
                title="3D View of Offline Devices by Days, Brand, and Region"
            )
            
            fig_3d.update_layout(
                scene=dict(
                    xaxis_title='Days Passed',
                    yaxis_title='Device Brand',
                    zaxis_title='Sub Region'
                ),
                height=600
            )
        else:
            fig_3d = go.Figure()
            fig_3d.update_layout(
                title="No Data Available",
                height=600
            )
        
        # Device Brand Pie Chart
        brand_counts = filtered_df['Device Brand'].value_counts().reset_index()
        brand_counts.columns = ['Device Brand', 'Count']
        
        fig_pie = px.pie(
            brand_counts,
            values='Count',
            names='Device Brand',
            title='Distribution of Offline Devices by Brand',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        
        # Aging Category Histogram
        aging_counts = filtered_df['Aging Category'].value_counts().reset_index()
        aging_counts.columns = ['Aging Category', 'Count']
        
        fig_hist = px.bar(
            aging_counts,
            x='Aging Category',
            y='Count',
            color='Aging Category',
            title='Distribution of Devices by Aging Category',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig_hist.update_layout(
            xaxis_title='Aging Category',
            yaxis_title='Number of Devices'
        )
        
        # Reason Bar Chart
        reason_counts = filtered_df['Reason'].fillna('Unknown').value_counts().head(10).reset_index()
        reason_counts.columns = ['Reason', 'Count']
        
        fig_bar = px.bar(
            reason_counts,
            x='Count',
            y='Reason',
            orientation='h',
            title='Top 10 Reasons for Device Offline Status',
            color='Count',
            color_continuous_scale='viridis'
        )
        
        fig_bar.update_layout(
            xaxis_title='Number of Devices',
            yaxis_title='Reason'
        )
        
        return (
            f"{total_devices}",
            f"{avg_days_offline}",
            f"{common_issue}",
            f"{critical_count}",
            fig_3d,
            fig_pie,
            fig_hist,
            fig_bar
        )
    
    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True, host='0.0.0.0', port=8050)

except ImportError as e:
    print(f"Required package not installed: {e}")
    print("Please install the required packages using:")
    print("pip install pandas plotly dash dash-bootstrap-components numpy")
    print("\nOr run the following command:")
    print("python -m pip install pandas plotly dash dash-bootstrap-components numpy")
    
    # Create a simple HTML file as an alternative
    with open("dashboard_instructions.html", "w") as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RMS Dashboard Setup Instructions</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f0f0; }
                .container { max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; }
                .step { background-color: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
                code { background-color: #34495e; color: #ecf0f1; padding: 2px 5px; border-radius: 3px; }
                .note { background-color: #fef9e7; border-left: 5px solid #f1c40f; padding: 10px; margin: 15px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>RMS Offline Devices Dashboard - Setup Instructions</h1>
                
                <p>It looks like you're missing some required Python packages to run the interactive dashboard. Please follow these steps to set up your environment:</p>
                
                <div class="step">
                    <h3>Step 1: Install Required Packages</h3>
                    <p>Open a terminal/command prompt and run one of these commands:</p>
                    <code>pip install pandas plotly dash dash-bootstrap-components numpy</code>
                    <p>OR</p>
                    <code>python -m pip install pandas plotly dash dash-bootstrap-components numpy</code>
                </div>
                
                <div class="step">
                    <h3>Step 2: Run the Dashboard</h3>
                    <p>After installing the packages, run the dashboard with:</p>
                    <code>python rms_dashboard.py</code>
                </div>
                
                <div class="step">
                    <h3>Step 3: Access the Dashboard</h3>
                    <p>Open your web browser and go to:</p>
                    <code>http://localhost:8050</code>
                </div>
                
                <div class="note">
                    <strong>Note:</strong> The dashboard will provide interactive 3D visualizations, filtering options, and real-time data analysis of your RMS offline devices.
                </div>
                
                <h2>Dashboard Features</h2>
                <ul>
                    <li>3D scatter plot showing device distribution by days offline, brand, and region</li>
                    <li>Interactive filters for regions, brands, and aging categories</li>
                    <li>Real-time KPIs (Total Devices, Average Days Offline, etc.)</li>
                    <li>Pie charts, bar graphs, and histograms for data visualization</li>
                    <li>Colorful, responsive design that works on all devices</li>
                </ul>
            </div>
        </body>
        </html>
        """)
    
    print("Created setup instructions in 'dashboard_instructions.html'")
    print("Open this file in your browser for detailed installation instructions.")
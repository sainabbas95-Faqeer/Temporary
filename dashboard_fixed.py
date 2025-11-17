import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
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
df['Days Passed'] = pd.to_numeric(df['Days Passed'], errors='coerce').fillna(0)

# Create Aging categories for better visualization
df['Aging Category'] = df['Aging'].fillna('Unknown')

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
    
    # Convert to list if single value
    if selected_regions:
        if isinstance(selected_regions, str):
            selected_regions = [selected_regions]
        # Filter by regions
        region_mask = df['Sub Region'].isin(selected_regions)
        filtered_df = filtered_df[region_mask]
    
    if selected_brands:
        if isinstance(selected_brands, str):
            selected_brands = [selected_brands]
        # Filter by brands
        brand_mask = df['Device Brand'].isin(selected_brands)
        filtered_df = filtered_df[brand_mask]
    
    if selected_aging:
        if isinstance(selected_aging, str):
            selected_aging = [selected_aging]
        # Filter by aging
        aging_mask = df['Aging Category'].isin(selected_aging)
        filtered_df = filtered_df[aging_mask]
    
    # Calculate KPIs
    total_devices = len(filtered_df)
    
    # Calculate average days offline
    if len(filtered_df) > 0:
        avg_days_offline = round(filtered_df['Days Passed'].mean(), 1)
    else:
        avg_days_offline = 0
    
    critical_count = len(filtered_df[filtered_df['Aging Category'] == '100+ Days'])
    
    # Most common issue
    if len(filtered_df) > 0:
        reason_series = filtered_df['Reason'].fillna('Unknown')
        mode_result = reason_series.mode()
        if len(mode_result) > 0:
            common_issue = mode_result.iloc[0]
        else:
            common_issue = "N/A"
    else:
        common_issue = "N/A"
    
    # 3D Scatter Plot
    if len(filtered_df) > 0:
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
    if len(filtered_df) > 0:
        brand_counts = filtered_df['Device Brand'].value_counts().reset_index()
        brand_counts.columns = ['Device Brand', 'Count']
        
        fig_pie = px.pie(
            brand_counts,
            values='Count',
            names='Device Brand',
            title='Distribution of Offline Devices by Brand',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
    else:
        fig_pie = go.Figure()
        fig_pie.update_layout(title="No Data Available")
    
    # Aging Category Histogram
    if len(filtered_df) > 0:
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
    else:
        fig_hist = go.Figure()
        fig_hist.update_layout(title="No Data Available")
    
    # Reason Bar Chart
    if len(filtered_df) > 0:
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
    else:
        fig_bar = go.Figure()
        fig_bar.update_layout(title="No Data Available")
    
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
    app.run(debug=True, host='0.0.0.0', port=8050)
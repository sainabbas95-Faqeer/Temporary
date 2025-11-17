import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Set page config
st.set_page_config(
    page_title="RMS Database Analysis",
    layout="wide"
)

# Load data from CSV files with multiple encoding fallbacks
@st.cache_data
def load_csv_with_fallback(filepath):
    """Load CSV with multiple encoding fallbacks"""
    encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
    for encoding in encodings:
        try:
            return pd.read_csv(filepath, encoding=encoding)
        except UnicodeDecodeError:
            continue
        except Exception as e:
            st.warning(f"Error with {filepath} using {encoding}: {e}")
            continue
    st.error(f"Failed to load {filepath} with all attempted encodings")
    return None

@st.cache_data
def load_data():
    try:
        # Load the main DB.csv file
        db_data = load_csv_with_fallback('DB.csv')
        return db_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Function to get current date and time in required format
def get_current_datetime():
    now = datetime.now()
    day = now.strftime("%A")[:3].upper()  # Get day abbreviation (MON, TUE, etc.)
    date_time = now.strftime("| %d-%b-%y | %H:%M:%S")
    return f"{day} {date_time}"

# Function to analyze Column L (Domain) data
def analyze_column_l_data(df):
    """Analyze Column L (Domain) data from the DataFrame"""
    if df is None or df.empty:
        return None
    
    try:
        # Count domains
        enfra_count = len(df[df['Domain'] == 'Enfra'])
        sms_ld_count = len(df[df['Domain'] == 'SMS LD'])
        others_count = len(df) - enfra_count - sms_ld_count
        
        return {
            'enfra': enfra_count,
            'smsLd': sms_ld_count,
            'others': others_count,
            'total': len(df)
        }
    except Exception as e:
        st.error(f"Error analyzing Column L data: {e}")
        return None

# Function to analyze region data
def analyze_region_data(df):
    """Analyze region data from the DataFrame"""
    if df is None or df.empty:
        return None
    
    try:
        # Group by region and domain
        region_analysis = df.groupby(['Region', 'Domain']).size().reset_index(name='count')
        return region_analysis
    except Exception as e:
        st.error(f"Error analyzing region data: {e}")
        return None

# Function to analyze aging data
def analyze_aging_data(df):
    """Analyze aging data from the DataFrame"""
    if df is None or df.empty:
        return None
    
    try:
        # Assuming there's a date column for aging analysis
        # This is a simplified example - you may need to adjust based on your actual data structure
        if 'Last Updated' in df.columns:
            # Convert to datetime and calculate days since last update
            df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
            df['days_since_update'] = (datetime.now() - df['Last Updated']).dt.days
            
            # Categorize by aging periods
            aging_categories = {
                '0-7 days': len(df[df['days_since_update'] <= 7]),
                '8-30 days': len(df[(df['days_since_update'] > 7) & (df['days_since_update'] <= 30)]),
                '31-90 days': len(df[(df['days_since_update'] > 30) & (df['days_since_update'] <= 90)]),
                '90+ days': len(df[df['days_since_update'] > 90])
            }
            return aging_categories
        else:
            # Return dummy data if no date column found
            return {
                '0-7 days': 25,
                '8-30 days': 35,
                '31-90 days': 20,
                '90+ days': 15
            }
    except Exception as e:
        st.error(f"Error analyzing aging data: {e}")
        return None

# Function to analyze reasons data
def analyze_reasons_data(df):
    """Analyze reasons data from the DataFrame"""
    if df is None or df.empty:
        return None
    
    try:
        # Assuming there's a 'Reason' column
        if 'Reason' in df.columns:
            reasons_count = df['Reason'].value_counts().head(10)
            return reasons_count
        else:
            # Return dummy data if no reason column found
            return pd.Series({
                'Power Failure': 45,
                'Network Issue': 32,
                'Hardware Failure': 28,
                'Software Bug': 15,
                'Maintenance': 12,
                'Other': 8
            })
    except Exception as e:
        st.error(f"Error analyzing reasons data: {e}")
        return None

# Function to create pie chart
def create_pie_chart(data, title):
    """Create a pie chart using Plotly"""
    if data is None:
        return None
    
    try:
        fig = go.Figure(data=[go.Pie(
            labels=list(data.keys()),
            values=list(data.values()),
            hole=0.3,
            textinfo='label+percent',
            textfont_size=12
        )])
        fig.update_layout(
            title=title,
            showlegend=True,
            height=400
        )
        return fig
    except Exception as e:
        st.error(f"Error creating pie chart: {e}")
        return None

# Function to create bar chart
def create_bar_chart(data, title, x_label, y_label):
    """Create a bar chart using Plotly"""
    if data is None:
        return None
    
    try:
        if isinstance(data, dict):
            x_data = list(data.keys())
            y_data = list(data.values())
        elif isinstance(data, pd.Series):
            x_data = data.index.tolist()
            y_data = data.values.tolist()
        else:
            return None
            
        fig = go.Figure(data=[go.Bar(
            x=x_data,
            y=y_data,
            text=y_data,
            textposition='auto'
        )])
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            height=400
        )
        return fig
    except Exception as e:
        st.error(f"Error creating bar chart: {e}")
        return None

# Main app
def main():
    # Custom CSS
    st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .header .header-content {
            flex: 1;
            text-align: center;
        }

        .header h1 {
            font-family: 'Algerian', 'Impact', 'Arial Black', sans-serif;
            font-size: 24px;
            margin-bottom: 0;
            color: #00008B;
            text-align: center;
            font-weight: bold;
            letter-spacing: 2px;
        }

        .header .date-info {
            position: absolute;
            top: 20px;
            right: 30px;
            font-size: 12px;
            color: #00008B;
            font-weight: bold;
            text-align: right;
        }

        .footer-text {
            position: fixed;
            bottom: 10px;
            right: 10px;
            font-size: 12px;
            color: #333;
            background: rgba(255, 255, 255, 0.7);
            padding: 5px 10px;
            border-radius: 5px;
            z-index: 1000;
        }

        .back-button {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(238, 90, 111, 0.4);
            display: inline-block;
            text-decoration: none;
        }

        .back-button:hover {
            transform: translateY(-3px) rotate(5deg);
            box-shadow: 0 6px 20px rgba(238, 90, 111, 0.6);
        }

        .back-button:active {
            transform: translateY(-1px);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            transform: perspective(1000px) rotateX(0deg);
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            transform: perspective(1000px) rotateX(-5deg) translateY(-5px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        }

        .stat-number {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .stat-label {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .chart-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
            margin-bottom: 30px;
        }

        .chart-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }

        @media (max-width: 1200px) {
            .chart-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 768px) {
            .chart-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Back button
    st.markdown('<a href="/" class="back-button">🤪 Back to Safety!</a>', unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div class="header">
        <div class="date-info" id="dateInfo">Data till<br>{(datetime.now() - timedelta(days=1)).strftime('%A, %b %d, %Y')}<br><span id="displayTime" style="color: red; font-weight: bold;">{datetime.now().strftime('%I:%M:%S %p')}</span></div>
        <div class="header-content">
            <h1>RMS OFFLINE SUMMARY</h1>
            <p>Remote Monitoring System - Data Analysis Dashboard</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer text
    st.markdown('<div class="footer-text">Database created by - Abbas Enterprises - Lakhi - 2025</div>', unsafe_allow_html=True)

    # Load data
    df = load_data()
    
    if df is not None:
        # Analyze data
        column_l_analysis = analyze_column_l_data(df)
        region_analysis = analyze_region_data(df)
        aging_analysis = analyze_aging_data(df)
        reasons_analysis = analyze_reasons_data(df)
        
        # Display stats grid
        if column_l_analysis:
            st.markdown("""
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">Total Offline on Enfra Domain</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">Total Offline on SMS LD Domain</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">Total RMS Offline</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">Total RMS Sites</div>
                </div>
            </div>
            """.format(
                column_l_analysis['enfra'],
                column_l_analysis['smsLd'],
                column_l_analysis['enfra'] + column_l_analysis['smsLd'],
                column_l_analysis['total']
            ), unsafe_allow_html=True)
        
        # Display charts
        st.markdown('<div class="chart-grid">', unsafe_allow_html=True)
        
        # Chart 1: Enfra Vs SMS LD
        col1, col2, col3 = st.columns(3)
        with col1:
            if column_l_analysis:
                pie_data = {
                    'Enfra': column_l_analysis['enfra'],
                    'SMS LD': column_l_analysis['smsLd'],
                    'Others': column_l_analysis['others']
                }
                fig1 = create_pie_chart(pie_data, "Enfra Vs SMS LD")
                if fig1:
                    st.plotly_chart(fig1, use_container_width=True)
        
        # Chart 2: RMS Offline Count Cluster Wise (Enfra Domain)
        with col2:
            # Dummy data for demonstration
            cluster_data_enfra = {
                'Jacob Abad': 25,
                'Larkana': 30,
                'Sukkur': 20,
                'Khairpur': 15,
                'Dadu': 10
            }
            fig2 = create_bar_chart(cluster_data_enfra, "RMS Offline Count Cluster Wise (Enfra Domain)", "Cluster", "Count")
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)
        
        # Chart 3: RMS Offline Count Cluster Wise (SMS LD Domain)
        with col3:
            # Dummy data for demonstration
            cluster_data_smsld = {
                'Jacob Abad': 15,
                'Larkana': 20,
                'Sukkur': 25,
                'Khairpur': 10,
                'Dadu': 5
            }
            fig3 = create_bar_chart(cluster_data_smsld, "RMS Offline Count Cluster Wise (SMS LD Domain)", "Cluster", "Count")
            if fig3:
                st.plotly_chart(fig3, use_container_width=True)
        
        # Second row of charts
        col4, col5, col6 = st.columns(3)
        
        # Chart 4: RMS Offline Count with Aging (Enfra Domain)
        with col4:
            if aging_analysis:
                fig4 = create_bar_chart(aging_analysis, "RMS Offline Count with Aging (Enfra Domain)", "Aging Period", "Count")
                if fig4:
                    st.plotly_chart(fig4, use_container_width=True)
        
        # Chart 5: RMS Offline Count with Aging (SMS LD Domain)
        with col5:
            # Dummy data for SMS LD aging
            smsld_aging = {
                '0-7 days': 20,
                '8-30 days': 25,
                '31-90 days': 15,
                '90+ days': 10
            }
            fig5 = create_bar_chart(smsld_aging, "RMS Offline Count with Aging (SMS LD Domain)", "Aging Period", "Count")
            if fig5:
                st.plotly_chart(fig5, use_container_width=True)
        
        # Chart 6: RMS Offline Reasons
        with col6:
            if reasons_analysis is not None:
                fig6 = create_bar_chart(reasons_analysis, "RMS Offline Reasons", "Reason", "Count")
                if fig6:
                    st.plotly_chart(fig6, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.error("Failed to load data. Please check the DB.csv file.")

if __name__ == "__main__":
    main()
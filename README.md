# RMS Dashboard

## Setup Instructions

To run this dashboard properly, please ensure you have all required packages installed:

```bash
pip install streamlit pandas plotly
```

After installing the packages, run the dashboard with:

```bash
streamlit run streamlit_dashboard.py
```

If you're using a virtual environment, make sure it's activated before installing packages.

## Running the Dashboard

You can run the dashboard using one of these methods:

1. **Direct method**:
   ```bash
   streamlit run streamlit_dashboard.py
   ```

2. **Using the batch file**:
   ```bash
   run_streamlit.bat
   ```

3. **Install packages first, then run**:
   ```bash
   install_packages.bat
   streamlit run streamlit_dashboard.py
   ```

## Troubleshooting

If you encounter any "missing package" errors:

1. Make sure all packages in `requirements.txt` are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Install additional dependencies:
   ```bash
   pip install toml cachetools tornado
   ```

3. If problems persist, try upgrading pip first:
   ```bash
   python -m pip install --upgrade pip
   ```

The dashboard should be accessible at http://localhost:8501 after successful startup.
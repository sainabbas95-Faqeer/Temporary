import requests
import time

try:
    # Wait a moment for the server to start
    time.sleep(2)
    
    # Try to access the dashboard
    response = requests.get('http://localhost:8050', timeout=5)
    
    if response.status_code == 200:
        print("SUCCESS: Dashboard is running and accessible!")
        print(f"Status Code: {response.status_code}")
        print("You can now open your browser and go to http://localhost:8050")
    else:
        print(f"WARNING: Received status code {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect to the dashboard.")
    print("Please make sure the dashboard is running by executing 'python dashboard_fixed.py'")
    
except requests.exceptions.Timeout:
    print("ERROR: Request timed out. The dashboard might still be starting up.")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
#!/usr/bin/env python3
"""
Simple script to start the Open-A.G.I monitoring dashboard
"""

import sys
import os

if __name__ == "__main__":
    # Change to the Open-A.G.I directory
    open_agi_path = os.path.join(os.path.dirname(__file__), 'Open-A.G.I')
    os.chdir(open_agi_path)
    
    # Add current directory to Python path
    sys.path.insert(0, '.')
    
    # Import and start the monitoring dashboard
    from monitoring_dashboard import start_dashboard
    
    print("Starting Open-A.G.I monitoring dashboard on localhost:8090")
    server = start_dashboard({'host': 'localhost', 'dashboard_port': 8090})
    print("Dashboard started. Press Ctrl+C to stop.")
    
    try:
        # Keep the script running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping dashboard...")
        if server and hasattr(server, 'stop_server'):
            server.stop_server()
        print("Dashboard stopped.")
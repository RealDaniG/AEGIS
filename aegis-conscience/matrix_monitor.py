"""
Matrix Monitor for AEGIS-Conscience Network
Real-time monitoring of node matrix connectivity
"""

import asyncio
import json
import time
import os
import sys
from typing import Dict, List

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.node_matrix import NodeMatrixManager
from tools.matrix_visualizer import MatrixVisualizer


class MatrixMonitor:
    """Monitors and displays real-time matrix connectivity"""
    
    def __init__(self, refresh_interval: int = 5):
        self.refresh_interval = refresh_interval
        self.visualizer = MatrixVisualizer()
        self.running = False
    
    def load_matrix_data(self, filepath: str = "./matrix_data.json") -> Dict:
        """Load matrix data from file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading matrix data: {e}")
            return {}
    
    def display_matrix_status(self, matrix_data: Dict):
        """Display current matrix status"""
        # Clear screen (works on most terminals)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print("AEGIS-CONSCIENCE NETWORK - REAL-TIME MATRIX MONITOR")
        print("=" * 80)
        print(f"Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Load data into visualizer
        self.visualizer.load_matrix_data(matrix_data)
        
        # Display matrix
        self.visualizer.visualize_matrix()
        self.visualizer.print_statistics()
        
        print(f"\n🔄 Refreshing every {self.refresh_interval} seconds...")
        print("Press Ctrl+C to stop monitoring")
    
    async def monitor(self, filepath: str = "./matrix_data.json"):
        """Monitor matrix connectivity in real-time"""
        self.running = True
        print("🔍 Starting matrix monitor...")
        
        try:
            while self.running:
                # Load current matrix data
                matrix_data = self.load_matrix_data(filepath)
                
                if matrix_data:
                    # Display matrix status
                    self.display_matrix_status(matrix_data)
                else:
                    print("⚠️  No matrix data available")
                    print(f"Looking for data file: {filepath}")
                
                # Wait before next refresh
                await asyncio.sleep(self.refresh_interval)
                
        except KeyboardInterrupt:
            print("\n⏹️  Stopping matrix monitor...")
            self.running = False
        except Exception as e:
            print(f"Error in monitor: {e}")
            self.running = False


async def main():
    """Main monitor function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor AEGIS-Conscience Network Matrix Connectivity")
    parser.add_argument("--file", "-f", default="./matrix_data.json", 
                       help="Path to matrix data JSON file")
    parser.add_argument("--interval", "-i", type=int, default=5,
                       help="Refresh interval in seconds")
    
    args = parser.parse_args()
    
    monitor = MatrixMonitor(refresh_interval=args.interval)
    await monitor.monitor(args.file)


if __name__ == "__main__":
    asyncio.run(main())
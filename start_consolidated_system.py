#!/usr/bin/env python3
"""
Consolidated system launcher for AEGIS - Runs all components in a single terminal
with proper process management and web UI auto-launch.
"""

import asyncio
import sys
import time
import os
import signal
import webbrowser
import subprocess
import threading

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class ConsolidatedLauncher:
    def __init__(self):
        self.running = True
        self.unified_process = None
        self.web_server_process = None
        
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n🛑 Shutting down AEGIS system...")
        self.running = False
        self.terminate_processes()
        sys.exit(0)
        
    def terminate_processes(self):
        """Terminate all child processes"""
        try:
            if self.unified_process and self.unified_process.poll() is None:
                self.unified_process.terminate()
                self.unified_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            if self.unified_process:
                self.unified_process.kill()
        except Exception as e:
            print(f"Error terminating unified process: {e}")
            
        try:
            if self.web_server_process and self.web_server_process.poll() is None:
                self.web_server_process.terminate()
                self.web_server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            if self.web_server_process:
                self.web_server_process.kill()
        except Exception as e:
            print(f"Error terminating web server process: {e}")
                
    def start_unified_system(self):
        """Start the unified system coordinator"""
        try:
            print("\n🚀 Starting AEGIS System Coordinator...")
            self.unified_process = subprocess.Popen(
                [sys.executable, "start_unified_system.py"],
                cwd=".",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ AEGIS System Coordinator started (PID: {self.unified_process.pid})")
            return True
        except Exception as e:
            print(f"❌ Error starting AEGIS System Coordinator: {e}")
            return False
            
    def start_web_server(self):
        """Start the Metatron web server"""
        try:
            print("\n🚀 Starting Metatron Integrated Web Server...")
            self.web_server_process = subprocess.Popen(
                [sys.executable, "Metatron-ConscienceAI/scripts/metatron_web_server.py"],
                cwd=".",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ Metatron Web Server started (PID: {self.web_server_process.pid})")
            return True
        except Exception as e:
            print(f"❌ Error starting Metatron Web Server: {e}")
            return False
            
    def launch_web_ui(self):
        """Launch the web UI after a delay"""
        def open_browser():
            time.sleep(8)  # Wait for servers to start (reduced from 15 seconds)
            try:
                webbrowser.open("http://localhost:8003")
                print("🌐 Web UI opened in default browser: http://localhost:8003")
            except Exception as e:
                print(f"⚠️  Could not auto-open browser: {e}")
                print("   Please manually open: http://localhost:8003")
                
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
    def monitor_processes(self):
        """Monitor processes in separate threads"""
        def monitor_unified():
            if self.unified_process and self.unified_process.stdout:
                try:
                    # Read output in a non-blocking way
                    while self.running and self.unified_process.poll() is None:
                        output = self.unified_process.stdout.readline()
                        if output:
                            print(f"[AEGIS Coordinator] {output.strip()}")
                        time.sleep(0.1)
                        
                    # Print any remaining output
                    stdout, stderr = self.unified_process.communicate()
                    if stdout:
                        print(f"[AEGIS Coordinator] {stdout}")
                    if stderr:
                        print(f"[AEGIS Coordinator] ERROR: {stderr}")
                except Exception as e:
                    print(f"Error monitoring AEGIS Coordinator: {e}")
                    
        def monitor_web_server():
            if self.web_server_process and self.web_server_process.stdout:
                try:
                    # Read output in a non-blocking way
                    while self.running and self.web_server_process.poll() is None:
                        output = self.web_server_process.stdout.readline()
                        if output:
                            print(f"[Metatron Web Server] {output.strip()}")
                        time.sleep(0.1)
                        
                    # Print any remaining output
                    stdout, stderr = self.web_server_process.communicate()
                    if stdout:
                        print(f"[Metatron Web Server] {stdout}")
                    if stderr:
                        print(f"[Metatron Web Server] ERROR: {stderr}")
                except Exception as e:
                    print(f"Error monitoring Metatron Web Server: {e}")
        
        # Start monitoring threads
        unified_thread = threading.Thread(target=monitor_unified, daemon=True)
        web_thread = threading.Thread(target=monitor_web_server, daemon=True)
        
        unified_thread.start()
        web_thread.start()
        
        return [unified_thread, web_thread]
        
    def run(self):
        """Main execution method"""
        print("=" * 80)
        print("🤖 AEGIS - Autonomous Governance and Intelligent Systems")
        print("🔄 Starting consolidated system with single terminal interface")
        print("=" * 80)
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        if os.name != 'nt':  # Not Windows
            signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Start the unified system coordinator
            if not self.start_unified_system():
                print("❌ Failed to start AEGIS System Coordinator")
                return
                
            # Start the Metatron web server
            if not self.start_web_server():
                print("❌ Failed to start Metatron Web Server")
                return
            
            # Launch web UI
            self.launch_web_ui()
            
            # Monitor processes
            print("\n📊 System is running. Press Ctrl+C to stop all components.\n")
            
            # Start monitoring threads
            monitor_threads = self.monitor_processes()
            
            # Keep main thread alive
            while self.running:
                time.sleep(1)
                
                # Check if any process has died
                if self.unified_process and self.unified_process.poll() is not None and self.running:
                    print(f"⚠️  AEGIS Coordinator process has terminated unexpectedly (PID: {self.unified_process.pid})")
                    self.running = False
                    break
                    
                if self.web_server_process and self.web_server_process.poll() is not None and self.running:
                    print(f"⚠️  Metatron Web Server process has terminated unexpectedly (PID: {self.web_server_process.pid})")
                    self.running = False
                    break
                        
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"❌ Error running system: {e}")
        finally:
            self.terminate_processes()
            print("\n👋 AEGIS system shutdown complete.")

def main():
    """Main entry point"""
    launcher = ConsolidatedLauncher()
    try:
        launcher.run()
    except KeyboardInterrupt:
        print("\n🛑 System interrupted by user")
    except Exception as e:
        print(f"❌ Unhandled error: {e}")

if __name__ == "__main__":
    main()
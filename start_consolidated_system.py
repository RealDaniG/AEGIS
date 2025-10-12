#!/usr/bin/env python3
"""
Consolidated system launcher for AEGIS - Runs all components in a single terminal
with proper process management and web UI auto-launch.
"""

import subprocess
import sys
import time
import os
import signal
import webbrowser
from threading import Thread

class ConsolidatedLauncher:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n🛑 Shutting down AEGIS system...")
        self.running = False
        self.terminate_processes()
        sys.exit(0)
        
    def terminate_processes(self):
        """Terminate all child processes"""
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(f"Error terminating process: {e}")
                
    def start_process(self, cmd, cwd=None, name="Process"):
        """Start a subprocess and track it"""
        try:
            process = subprocess.Popen(
                cmd, 
                cwd=cwd, 
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid if os.name != 'nt' else None
            )
            self.processes.append(process)
            print(f"✅ {name} started (PID: {process.pid})")
            return process
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
            return None
            
    def monitor_process(self, process, name):
        """Monitor a process and print its output"""
        if process is None:
            return
            
        try:
            # Read output in a non-blocking way
            while self.running and process.poll() is None:
                output = process.stdout.readline()
                if output:
                    print(f"[{name}] {output.strip()}")
                time.sleep(0.1)
                
            # Print any remaining output
            stdout, stderr = process.communicate()
            if stdout:
                print(f"[{name}] {stdout}")
            if stderr:
                print(f"[{name}] ERROR: {stderr}")
                
        except Exception as e:
            print(f"Error monitoring {name}: {e}")
            
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
                
        browser_thread = Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
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
            print("\n🚀 Starting AEGIS System Coordinator...")
            unified_process = self.start_process(
                "python start_unified_system.py",
                cwd=".",
                name="AEGIS Coordinator"
            )
            
            # Start the Metatron web server
            print("\n🚀 Starting Metatron Integrated Web Server...")
            web_process = self.start_process(
                "python Metatron-ConscienceAI/scripts/metatron_web_server.py",
                cwd=".",
                name="Metatron Web Server"
            )
            
            # Launch web UI
            self.launch_web_ui()
            
            # Monitor processes
            print("\n📊 System is running. Press Ctrl+C to stop all components.\n")
            
            # Monitor outputs in separate threads
            threads = []
            
            if unified_process:
                unified_thread = Thread(
                    target=self.monitor_process, 
                    args=(unified_process, "AEGIS Coordinator")
                )
                unified_thread.daemon = True
                unified_thread.start()
                threads.append(unified_thread)
                
            if web_process:
                web_thread = Thread(
                    target=self.monitor_process, 
                    args=(web_process, "Metatron Web Server")
                )
                web_thread.daemon = True
                web_thread.start()
                threads.append(web_thread)
            
            # Keep main thread alive
            while self.running:
                time.sleep(1)
                
                # Check if any process has died
                for process in self.processes:
                    if process.poll() is not None and self.running:
                        print(f"⚠️  A process has terminated unexpectedly (PID: {process.pid})")
                        self.running = False
                        break
                        
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"❌ Error running system: {e}")
        finally:
            self.terminate_processes()
            print("\n👋 AEGIS system shutdown complete.")

if __name__ == "__main__":
    launcher = ConsolidatedLauncher()
    launcher.run()
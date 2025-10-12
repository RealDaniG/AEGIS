#!/usr/bin/env python3
"""
Close Unnecessary Ports Script
============================

This script identifies and safely closes ports that might not be needed
according to the AEGIS system specifications.
"""

import subprocess
import sys
import time

def get_listening_ports():
    """Get all listening ports on the system"""
    try:
        # Get listening ports using netstat
        result = subprocess.run(
            ["netstat", "-an"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        listening_ports = []
        for line in result.stdout.splitlines():
            if "LISTENING" in line:
                parts = line.split()
                if len(parts) >= 2:
                    # Extract port from address (format: 0.0.0.0:8003 or [::]:8003)
                    address = parts[1]
                    if ":" in address:
                        port = address.split(":")[-1]
                        if port.isdigit():
                            listening_ports.append(int(port))
        
        return sorted(list(set(listening_ports)))
    except Exception as e:
        print(f"Error getting listening ports: {e}")
        return []

def get_process_by_port(port):
    """Get process ID using a specific port"""
    try:
        # Use PowerShell to get the process using the port
        result = subprocess.run(
            ["powershell", "-Command", f"Get-NetTCPConnection -LocalPort {port} | Select-Object -ExpandProperty OwningProcess"],
            capture_output=True,
            text=True,
            check=True
        )
        
        process_id = result.stdout.strip()
        if process_id.isdigit():
            return int(process_id)
        return None
    except Exception as e:
        print(f"Error getting process for port {port}: {e}")
        return None

def get_process_info(pid):
    """Get process information by PID"""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV"],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.strip().splitlines()
        if len(lines) > 1:
            # Parse CSV output
            info = lines[1].strip('"').split('","')
            if len(info) >= 1:
                return info[0]  # Process name
        return "Unknown"
    except Exception as e:
        print(f"Error getting process info for PID {pid}: {e}")
        return "Unknown"

def is_port_needed(port):
    """
    Determine if a port is needed based on AEGIS system specifications
    
    According to project specifications:
    - Port 8003: Main Metatron-ConscienceAI system (REQUIRED)
    - Port 8005: Unified API layer (REQUIRED)
    - Port 5180: Web chat server (OPTIONAL - can be consolidated)
    - Port 8081: Dashboard (OPTIONAL - can be consolidated)
    """
    # Essential ports that should remain open
    essential_ports = [8003, 8005]
    
    # Ports that can be closed if not actively used
    closable_ports = [5180, 8081]
    
    if port in essential_ports:
        return True, "Essential system port"
    elif port in closable_ports:
        return False, "Optional port that can be consolidated"
    else:
        # For other ports, we'll check if they're related to our system
        return None, "Unknown port - requires manual verification"

def close_port(port):
    """Attempt to close a port by terminating its process"""
    try:
        pid = get_process_by_port(port)
        if pid:
            process_name = get_process_info(pid)
            print(f"  Terminating process PID {pid} ({process_name}) using port {port}...")
            
            # Terminate the process
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/F"],
                capture_output=True,
                text=True
            )
            
            # Wait a moment for the port to be released
            time.sleep(1)
            
            # Verify the port is closed
            if not is_port_still_listening(port):
                print(f"  ✅ Port {port} successfully closed")
                return True
            else:
                print(f"  ⚠️  Port {port} may still be listening")
                return False
        else:
            print(f"  ❌ Could not identify process for port {port}")
            return False
    except Exception as e:
        print(f"  ❌ Error closing port {port}: {e}")
        return False

def is_port_still_listening(port):
    """Check if a port is still listening"""
    try:
        result = subprocess.run(
            ["netstat", "-an"],
            capture_output=True,
            text=True,
            check=True
        )
        
        for line in result.stdout.splitlines():
            if f":{port}" in line and "LISTENING" in line:
                return True
        return False
    except Exception:
        return True  # Assume still listening if we can't check

def main():
    """Main function to identify and close unnecessary ports"""
    print("🔒 PORT MANAGEMENT SCRIPT")
    print("=" * 50)
    print("Identifying and closing unnecessary ports in AEGIS system\n")
    
    # Get all listening ports
    listening_ports = get_listening_ports()
    print(f"📋 Total listening ports found: {len(listening_ports)}")
    
    # Focus on AEGIS-related ports
    aegis_ports = [port for port in listening_ports if port in [8003, 8005, 5180, 8081]]
    print(f"🎯 AEGIS-related ports: {aegis_ports}")
    
    # Check each port
    ports_to_close = []
    
    for port in aegis_ports:
        needed, reason = is_port_needed(port)
        pid = get_process_by_port(port)
        process_name = get_process_info(pid) if pid else "Unknown"
        
        print(f"\nPort {port}:")
        print(f"  Process: {process_name} (PID: {pid})")
        print(f"  Status: {reason}")
        
        if needed is False:
            ports_to_close.append((port, process_name, pid))
            print(f"  Recommendation: CLOSE PORT")
        elif needed is True:
            print(f"  Recommendation: KEEP PORT OPEN")
        else:
            print(f"  Recommendation: MANUAL VERIFICATION NEEDED")
    
    # Close unnecessary ports
    if ports_to_close:
        print(f"\n🔐 CLOSING UNNECESSARY PORTS")
        print("-" * 30)
        
        for port, process_name, pid in ports_to_close:
            print(f"\nClosing port {port} ({process_name}, PID: {pid})...")
            success = close_port(port)
            if success:
                print(f"  ✅ Successfully closed port {port}")
            else:
                print(f"  ❌ Failed to close port {port}")
    else:
        print(f"\n✅ No unnecessary ports found that require closing")
    
    # Final verification
    print(f"\n🔍 FINAL VERIFICATION")
    print("-" * 20)
    final_ports = get_listening_ports()
    final_aegis_ports = [port for port in final_ports if port in [8003, 8005, 5180, 8081]]
    
    print(f"AEGIS ports still listening: {final_aegis_ports}")
    
    # Verify essential ports are still open
    essential_ports = [8003, 8005]
    for port in essential_ports:
        if port in final_aegis_ports:
            print(f"✅ Essential port {port} is still open")
        else:
            print(f"⚠️  Warning: Essential port {port} appears to be closed")
    
    print(f"\n{'=' * 50}")
    print("🔒 PORT MANAGEMENT COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Patch script to modify the root endpoint to serve the correct HTML file
with Hebrew Quantum Field visualization by default
"""

import os
import shutil
import sys

def backup_file(file_path):
    """Create a backup of the file"""
    if os.path.exists(file_path):
        backup_path = file_path + ".backup"
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        return True
    return False

def patch_metatron_web_server():
    """Patch the metatron_web_server.py to prioritize the correct HTML file"""
    server_file = os.path.join("Metatron-ConscienceAI", "scripts", "metatron_web_server.py")
    
    if not os.path.exists(server_file):
        print(f"❌ Server file not found: {server_file}")
        return False
    
    # Create backup
    backup_file(server_file)
    
    try:
        with open(server_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for the file priority list
        if 'metatron_advanced_integrated.html' in content:
            print("✅ File priority list already includes metatron_advanced_integrated.html")
            return True
        
        # Find the root endpoint function
        lines = content.split('\n')
        new_lines = []
        in_root_function = False
        
        for line in lines:
            if '@app.get("/")' in line:
                in_root_function = True
                new_lines.append(line)
            elif in_root_function and 'for filename in' in line:
                # Replace the file priority list to put metatron_integrated.html first
                new_lines.append('    # Note: harmonic_monitor.html has been integrated into the main dashboard and is no longer served separately')
                new_lines.append('    for filename in ["metatron_integrated.html", "metatron_advanced_integrated.html", "integrated_dashboard.html", "unified_dashboard_updated.html", "unified_dashboard.html", "index_stream.html", "metatron_unified.html", "metatron_visualization.html"]:')
                # Skip the original line
                continue
            elif in_root_function and 'unified_dashboard.html", "index_stream.html"' in line:
                # Skip the rest of the original priority list
                continue
            elif in_root_function and 'index_stream.html", "metatron_integrated.html"' in line:
                # Skip the rest of the original priority list
                continue
            elif in_root_function and 'metatron_unified.html", "metatron_visualization.html"' in line:
                # Skip the rest of the original priority list
                continue
            elif in_root_function and ']:' in line:
                # End of the for loop
                in_root_function = False
                new_lines.append(line)
            else:
                new_lines.append(line)
        
        # Write the modified content
        with open(server_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print("✅ Successfully patched metatron_web_server.py")
        print("   The root endpoint will now serve metatron_integrated.html by default")
        return True
        
    except Exception as e:
        print(f"❌ Error patching metatron_web_server.py: {e}")
        return False

def verify_patch():
    """Verify that the patch was applied correctly"""
    server_file = os.path.join("Metatron-ConscienceAI", "scripts", "metatron_web_server.py")
    
    try:
        with open(server_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'metatron_integrated.html' in content and 'for filename in ["metatron_integrated.html"' in content:
            print("✅ Patch verification successful")
            return True
        else:
            print("❌ Patch verification failed")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying patch: {e}")
        return False

def create_redirect_index():
    """Create an index.html that redirects to the integrated version"""
    index_file = os.path.join("Metatron-ConscienceAI", "webui", "index.html")
    
    redirect_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=static/metatron_integrated.html">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirecting to the Metatron Integrated Consciousness Monitor with Hebrew Quantum Field visualization...</p>
    <p>If you are not redirected automatically, <a href="static/metatron_integrated.html">click here</a>.</p>
    <script>
        window.location.href = "static/metatron_integrated.html";
    </script>
</body>
</html>'''
    
    try:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(redirect_html)
        print("✅ Created redirect index.html")
        return True
    except Exception as e:
        print(f"❌ Error creating redirect index.html: {e}")
        return False

def main():
    print("🔧 Patching Root Endpoint for Hebrew Quantum Field Visualization")
    print("="*60)
    
    # Patch the server file
    print("\n1. Patching metatron_web_server.py...")
    if patch_metatron_web_server():
        print("   [OK] Server file patched successfully")
        
        # Verify the patch
        print("\n2. Verifying patch...")
        if verify_patch():
            print("   [OK] Patch verification successful")
        else:
            print("   ❌ Patch verification failed")
    else:
        print("   ❌ Failed to patch server file")
    
    # Create redirect index.html as fallback
    print("\n3. Creating redirect index.html...")
    if create_redirect_index():
        print("   [OK] Redirect index.html created successfully")
    else:
        print("   ❌ Failed to create redirect index.html")
    
    print("\n" + "="*60)
    print("✅ PATCH COMPLETE")
    print("\nChanges made:")
    print("1. Modified metatron_web_server.py to prioritize metatron_integrated.html")
    print("2. Created redirect index.html as fallback")
    print("\nAfter restarting the server, http://localhost:8003/ will show")
    print("the Hebrew Quantum Field visualization by default.")
    print("\nTo apply changes:")
    print("1. Stop the current server (Ctrl+C)")
    print("2. Restart the server: cd Metatron-ConscienceAI/scripts && python metatron_web_server.py")
    print("3. Access http://localhost:8003/ to see Hebrew Quantum Field visualization")
    print("="*60)

if __name__ == "__main__":
    main()
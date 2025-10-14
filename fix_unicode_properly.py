#!/usr/bin/env python3
"""
Script to properly fix all Unicode characters in memory_matrix.py
"""

def fix_unicode_characters():
    file_path = r'd:\metatronV2\Metatron-ConscienceAI\nodes\memory_matrix.py'
    
    # Read the file with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all Unicode characters with ASCII equivalents
    # Unicode characters and their ASCII replacements
    unicode_replacements = {
        '⚠️': '[WARN]',
        '🧠': '[MEMORY]',
        '📡': '[NETWORK]',
        '🔄': '[RESET]',
        '✅': '[OK]',
        '❌': '[ERROR]',
        '💾': '[DISK]',
        '📂': '[FOLDER]',
        '🔔': '[NOTIFY]',
        '\u26a0\ufe0f': '[WARN]',  # Warning sign
        '\U0001f9e0': '[MEMORY]',  # Brain
        '\U0001f4e1': '[NETWORK]', # Satellite antenna
        '\U0001f504': '[RESET]',   # Clockwise rightwards and leftwards open circle arrows
        '\U0001f7e2': '[OK]',      # Green circle
        '\U0001f198': '[ERROR]',   # SOS
        '\U0001f4be': '[DISK]',    # Floppy disk
        '\U0001f4c2': '[FOLDER]',  # Open file folder
        '\U0001f514': '[NOTIFY]',  # Bell
    }
    
    # Apply all replacements
    for unicode_char, ascii_replacement in unicode_replacements.items():
        content = content.replace(unicode_char, ascii_replacement)
    
    # Write the fixed content back to the file with UTF-8 encoding
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("All Unicode characters fixed successfully!")

if __name__ == "__main__":
    fix_unicode_characters()
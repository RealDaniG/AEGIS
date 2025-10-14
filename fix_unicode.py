#!/usr/bin/env python3
"""
Script to fix Unicode characters in memory_matrix.py
"""

import os

def fix_unicode_characters():
    file_path = r'd:\metatronV2\Metatron-ConscienceAI\nodes\memory_matrix.py'
    
    # Read the file with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace Unicode characters with ASCII equivalents
    replacements = {
        '⚠️': '[WARN]',
        '🧠': '[MEMORY]',
        '📡': '[NETWORK]',
        '🔄': '[RESET]',
        '✅': '[OK]',
        '❌': '[ERROR]',
        '💾': '[DISK]',
        '📂': '[FOLDER]',
        '🔔': '[NOTIFY]',
        ' onion': ' [TOR]'
    }
    
    for unicode_char, ascii_replacement in replacements.items():
        content = content.replace(unicode_char, ascii_replacement)
    
    # Write the fixed content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Unicode characters fixed successfully!")

if __name__ == "__main__":
    fix_unicode_characters()
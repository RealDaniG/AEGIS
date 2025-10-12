#!/usr/bin/env python3
"""
Script to add legacy ConscienceAI files as context to METATRONV2 memory system

This script provides two methods for integrating legacy data:
1. Direct memory import (for chat histories, consciousness states)
2. RAG corpus integration (for knowledge base documents)
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Simple flag to indicate if memory system is available
MEMORY_SYSTEM_AVAILABLE = False

def convert_text_to_rag_jsonl(input_file: str, output_file: str, source_name: Optional[str] = None):
    """
    Convert a text file to RAG corpus format (JSONL)
    
    Args:
        input_file (str): Path to the input text file
        output_file (str): Path to the output JSONL file
        source_name (str, optional): Optional source name for metadata
    """
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create RAG entry
        rag_entry = {
            "text": content,
            "source": source_name or os.path.basename(input_file),
            "language": "en"
        }
        
        # Append to JSONL file
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rag_entry, ensure_ascii=False) + '\n')
        
        print(f"✅ Converted {input_file} to RAG format in {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error converting {input_file} to RAG format: {e}")
        return False

def import_legacy_memory_json(legacy_memory_file: str, memory_path: str = "ai_chat_es_pdf_full/memory.json"):
    """
    Import legacy memory JSON file into the new memory system
    
    Args:
        legacy_memory_file (str): Path to the legacy memory JSON file
        memory_path (str): Path to the new memory system file
    """
    print("❌ Memory system integration requires manual setup. Please run this script from within the Metatron-ConscienceAI directory.")
    print("   You can manually copy the memory entries from the legacy file to the new memory system.")
    return False

def process_legacy_directory(legacy_dir: str, method: str = "rag"):
    """
    Process all files in a legacy directory
    
    Args:
        legacy_dir (str): Path to directory containing legacy files
        method (str): Method to use ("rag" or "memory")
    """
    legacy_path = Path(legacy_dir)
    if not legacy_path.exists():
        print(f"❌ Legacy directory {legacy_dir} does not exist")
        return False
    
    processed_count = 0
    
    # Process all .txt and .json files
    for file_path in legacy_path.rglob("*"):
        if file_path.suffix.lower() in [".txt", ".md"]:
            if method == "rag":
                convert_text_to_rag_jsonl(
                    str(file_path), 
                    "datasets/rss_research.jsonl",
                    file_path.name
                )
                processed_count += 1
        elif file_path.suffix.lower() == ".json" and method == "memory":
            if "session" in file_path.name or "memory" in file_path.name:
                print(f"ℹ️  Found legacy memory file: {file_path}")
                print("   Manual import required. Please use the memory system directly to import this file.")
                processed_count += 1
    
    print(f"✅ Processed {processed_count} legacy files using {method} method")
    return True

if __name__ == "__main__":
    # Example usage
    print("METATRONV2 Legacy Context Integration Script")
    print("=" * 50)
    
    # Example 1: Convert a text file to RAG format
    # convert_text_to_rag_jsonl("legacy_knowledge.txt", "datasets/rss_research.jsonl", "Legacy Knowledge")
    
    # Example 2: Import a legacy memory file
    # import_legacy_memory_json("legacy_memory.json")
    
    # Example 3: Process a directory of legacy files
    # process_legacy_directory("legacy_data", "rag")
    
    print("\nTo use this script:")
    print("1. For text documents: convert_text_to_rag_jsonl(input_file, output_file, source_name)")
    print("2. For memory files: Manual import required - run from within Metatron-ConscienceAI directory")
    print("3. For directories: process_legacy_directory(legacy_dir, method)")
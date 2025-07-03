#!/usr/bin/env python3
"""
Debug script to check what's actually stored in memory
"""

from memory_storage import memory_storage
import json

def debug_storage():
    print("=== MEMORY STORAGE DEBUG ===")
    
    # Get all data
    data = memory_storage.get_all_data()
    
    print(f"Data keys: {list(data.keys())}")
    
    for key, value in data.items():
        if isinstance(value, list):
            print(f"{key}: {len(value)} items")
            if value and len(value) > 0:
                print(f"  First item: {type(value[0])}")
                if isinstance(value[0], dict) and 'filename' in value[0]:
                    print(f"  Has filename: {value[0]['filename']}")
        elif isinstance(value, dict):
            print(f"{key}: {len(value)} items")
            if key == 'files':
                print(f"  Files stored: {list(value.keys())}")
                for filename, file_data in list(value.items())[:3]:  # Show first 3 files
                    print(f"    {filename}: {file_data.get('size', 0)} bytes, type: {file_data.get('content_type', 'unknown')}")
        else:
            print(f"{key}: {type(value)} - {str(value)[:50]}...")
    
    print(f"\nTotal data size estimation: {len(json.dumps(data, default=str))} characters")

if __name__ == "__main__":
    debug_storage()
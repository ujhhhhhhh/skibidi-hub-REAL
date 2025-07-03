#!/usr/bin/env python3
"""
Test script to verify file uploads are being stored in memory
"""

import requests
import io
import json

def test_file_upload():
    # Create a small test image (1x1 pixel PNG)
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Upload file to the app
    files = {'file': ('test.png', io.BytesIO(test_image_data), 'image/png')}
    data = {
        'username': 'TestUser',
        'content': 'Testing file upload to memory storage'
    }
    
    print("Uploading test file...")
    response = requests.post('http://localhost:5000/create', files=files, data=data)
    print(f"Upload response: {response.status_code}")
    
    if response.status_code == 302:  # Redirect after successful upload
        print("Upload successful!")
        
        # Now check what's in memory
        from memory_storage import memory_storage
        
        all_data = memory_storage.get_all_data()
        files_stored = all_data.get('files', {})
        posts = all_data.get('posts', [])
        
        print(f"Files in memory: {len(files_stored)}")
        for filename, file_data in files_stored.items():
            print(f"  {filename}: {file_data.get('size', 0)} bytes, type: {file_data.get('content_type', 'unknown')}")
        
        print(f"Posts created: {len(posts)}")
        for post in posts:
            if post.get('filename'):
                print(f"  Post has attachment: {post.get('filename')}")
        
        return len(files_stored) > 0
    else:
        print(f"Upload failed: {response.text}")
        return False

if __name__ == "__main__":
    success = test_file_upload()
    print(f"\nFile upload to memory test: {'PASSED' if success else 'FAILED'}")
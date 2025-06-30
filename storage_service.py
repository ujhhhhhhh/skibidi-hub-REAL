"""
Vercel Blob Storage Service for Skibidi Hub

This module provides abstraction over Vercel blob storage for both data files (JSON)
and uploaded media files. It handles the migration from local file storage to 
cloud-based blob storage.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
import vercel_blob
from io import BytesIO


class VercelBlobStorage:
    """Vercel Blob Storage abstraction layer"""
    
    def __init__(self):
        """Initialize storage service with environment token"""
        self.token = os.environ.get("BLOB_READ_WRITE_TOKEN")
        if not self.token:
            logging.warning("BLOB_READ_WRITE_TOKEN not found in environment variables")
    
    def put_json_data(self, file_key: str, data: Dict[str, Any]) -> bool:
        """
        Store JSON data in blob storage
        
        Args:
            file_key: Unique identifier for the data file (e.g., 'posts', 'comments')
            data: Dictionary data to store as JSON
            
        Returns:
            bool: Success status
        """
        try:
            json_content = json.dumps(data, ensure_ascii=False, indent=2)
            json_bytes = json_content.encode('utf-8')
            
            blob_name = f"data/{file_key}.json"
            response = vercel_blob.put(blob_name, json_bytes, verbose=True)
            
            if response and 'url' in response:
                logging.info(f"Successfully stored JSON data: {blob_name}")
                return True
            else:
                logging.error(f"Failed to store JSON data: {blob_name}")
                return False
                
        except Exception as e:
            logging.error(f"Error storing JSON data {file_key}: {e}")
            return False
    
    def get_json_data(self, file_key: str, default: Any = None) -> Any:
        """
        Retrieve JSON data from blob storage
        
        Args:
            file_key: Unique identifier for the data file
            default: Default value if file doesn't exist
            
        Returns:
            Parsed JSON data or default value
        """
        try:
            blob_name = f"data/{file_key}.json"
            
            # List blobs to check if file exists
            blobs_response = vercel_blob.list({'prefix': blob_name, 'limit': '1'})
            
            if not blobs_response.get('blobs') or len(blobs_response['blobs']) == 0:
                logging.info(f"JSON data file not found: {blob_name}, returning default")
                return default if default is not None else ([] if file_key in ['posts'] else {})
            
            # Get the blob URL and download content
            blob_info = blobs_response['blobs'][0]
            blob_url = blob_info['url']
            
            # Download the content using head to get metadata and download URL
            metadata = vercel_blob.head(blob_url)
            download_url = metadata.get('downloadUrl', blob_url)
            
            # For now, we'll use the direct URL since download_file needs local path
            # In a production environment, you might want to implement proper streaming
            import requests
            response = requests.get(download_url)
            response.raise_for_status()
            
            json_data = response.json()
            logging.info(f"Successfully retrieved JSON data: {blob_name}")
            return json_data
            
        except Exception as e:
            logging.error(f"Error retrieving JSON data {file_key}: {e}")
            return default if default is not None else ([] if file_key in ['posts'] else {})
    
    def put_file(self, file_content: bytes, filename: str, content_type: Optional[str] = None) -> Optional[str]:
        """
        Store uploaded file in blob storage
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            content_type: MIME type of the file
            
        Returns:
            str: Blob URL if successful, None otherwise
        """
        try:
            blob_name = f"uploads/{filename}"
            
            # Use multipart upload for larger files
            use_multipart = len(file_content) > 10 * 1024 * 1024  # 10MB threshold
            
            response = vercel_blob.put(
                blob_name, 
                file_content, 
                multipart=use_multipart,
                verbose=True
            )
            
            if response and 'url' in response:
                logging.info(f"Successfully stored file: {blob_name}")
                return response['url']
            else:
                logging.error(f"Failed to store file: {blob_name}")
                return None
                
        except Exception as e:
            logging.error(f"Error storing file {filename}: {e}")
            return None
    
    def get_file_url(self, filename: str) -> Optional[str]:
        """
        Get public URL for uploaded file
        
        Args:
            filename: Name of the file
            
        Returns:
            str: Public URL if file exists, None otherwise
        """
        try:
            blob_name = f"uploads/{filename}"
            
            # List blobs to check if file exists
            blobs_response = vercel_blob.list({'prefix': blob_name, 'limit': '1'})
            
            if not blobs_response.get('blobs') or len(blobs_response['blobs']) == 0:
                logging.warning(f"File not found: {blob_name}")
                return None
            
            blob_info = blobs_response['blobs'][0]
            return blob_info['url']
            
        except Exception as e:
            logging.error(f"Error getting file URL {filename}: {e}")
            return None
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete file from blob storage
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            bool: Success status
        """
        try:
            blob_name = f"uploads/{filename}"
            
            # Get the file URL first
            file_url = self.get_file_url(filename)
            if not file_url:
                logging.warning(f"File not found for deletion: {blob_name}")
                return False
            
            # Delete the blob
            vercel_blob.delete([file_url])
            logging.info(f"Successfully deleted file: {blob_name}")
            return True
            
        except Exception as e:
            logging.error(f"Error deleting file {filename}: {e}")
            return False
    
    def list_files(self, prefix: str = "uploads/", limit: int = 100) -> List[Dict[str, Any]]:
        """
        List files in blob storage
        
        Args:
            prefix: Prefix to filter files
            limit: Maximum number of files to return
            
        Returns:
            List of file information dictionaries
        """
        try:
            blobs_response = vercel_blob.list({
                'prefix': prefix,
                'limit': str(limit)
            })
            
            return blobs_response.get('blobs', [])
            
        except Exception as e:
            logging.error(f"Error listing files with prefix {prefix}: {e}")
            return []
    
    def migrate_local_data(self, local_data_folder: str = "data", local_upload_folder: str = "uploads") -> bool:
        return True # comment that line to enable migration
        """
        Migrate existing local data to blob storage
        
        Args:
            local_data_folder: Path to local data folder
            local_upload_folder: Path to local uploads folder
            
        Returns:
            bool: Migration success status
        """
        migration_success = True
        
        try:
            # Migrate JSON data files
            data_files = ['posts.json', 'comments.json', 'likes.json', 'hall_of_fame.json', 'hall_of_shame.json']
            
            for data_file in data_files:
                local_path = os.path.join(local_data_folder, data_file)
                if os.path.exists(local_path):
                    try:
                        with open(local_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        file_key = data_file.replace('.json', '')
                        if not self.put_json_data(file_key, data):
                            migration_success = False
                            logging.error(f"Failed to migrate {data_file}")
                        else:
                            logging.info(f"Successfully migrated {data_file}")
                    except Exception as e:
                        logging.error(f"Error migrating {data_file}: {e}")
                        migration_success = False
            
            # Migrate uploaded files
            if os.path.exists(local_upload_folder):
                for filename in os.listdir(local_upload_folder):
                    file_path = os.path.join(local_upload_folder, filename)
                    if os.path.isfile(file_path):
                        try:
                            with open(file_path, 'rb') as f:
                                file_content = f.read()
                            
                            blob_url = self.put_file(file_content, filename)
                            if not blob_url:
                                migration_success = False
                                logging.error(f"Failed to migrate file {filename}")
                            else:
                                logging.info(f"Successfully migrated file {filename}")
                        except Exception as e:
                            logging.error(f"Error migrating file {filename}: {e}")
                            migration_success = False
            
            return migration_success
            
        except Exception as e:
            logging.error(f"Error during migration: {e}")
            return False


# Global storage service instance
storage_service = VercelBlobStorage()
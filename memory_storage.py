"""
In-Memory Storage Service for Skibidi Hub

This module provides in-memory storage using Python dictionaries with
backup functionality to send data to external URLs.
"""

import json
import logging
import os
import requests
import threading
import time
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class MemoryStorage:
    """In-memory storage with backup functionality"""
    
    def __init__(self):
        """Initialize in-memory storage"""
        self.data = {
            'posts': [],
            'comments': [],
            'likes': [],
            'hall_of_fame': [],
            'hall_of_shame': [],
            'videos': [],
            'files': {}  # Store files as base64 with metadata
        }
        
        # Backup configuration
        self.backup_url = os.environ.get('BACKUP_URL')
        self.backup_interval = int(os.environ.get('BACKUP_INTERVAL', '300'))  # 5 minutes default
        
        # Start backup thread if URL is configured
        if self.backup_url:
            self.backup_thread = threading.Thread(target=self._backup_loop, daemon=True)
            self.backup_thread.start()
            logger.info(f"Started backup thread, sending to {self.backup_url} every {self.backup_interval} seconds")
        else:
            logger.warning("No BACKUP_URL configured, backups disabled")
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """Get data from memory storage"""
        return self.data.get(key, default if default is not None else [])
    
    def set_data(self, key: str, value: Any) -> bool:
        """Set data in memory storage"""
        try:
            self.data[key] = value
            return True
        except Exception as e:
            logger.error(f"Error setting data for key {key}: {e}")
            return False
    
    def append_data(self, key: str, item: Any) -> bool:
        """Append item to data list"""
        try:
            if key not in self.data:
                self.data[key] = []
            self.data[key].append(item)
            return True
        except Exception as e:
            logger.error(f"Error appending data to key {key}: {e}")
            return False
    
    def get_all_data(self) -> Dict[str, Any]:
        """Get all data for backup purposes"""
        return self.data.copy()
    
    def _backup_loop(self):
        """Background thread to send periodic backups"""
        while True:
            try:
                time.sleep(self.backup_interval)
                self._send_backup()
            except Exception as e:
                logger.error(f"Error in backup loop: {e}")
    
    def _send_backup(self):
        """Send backup data to configured URL"""
        if not self.backup_url:
            return
        
        try:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'data': self.get_all_data()
            }
            
            # Ensure URL ends with / for proper endpoint access
            backup_url = self.backup_url.rstrip('/') + '/'
            
            response = requests.post(
                backup_url,
                json=backup_data,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'SkibidiHub-Backup/1.0'
                },
                timeout=60,  # Increased timeout for large files
                verify=True  # Verify SSL certificates
            )
            
            if response.status_code == 200:
                logger.info(f"Backup sent successfully to {backup_url}")
                try:
                    result = response.json()
                    logger.info(f"Server response: {result.get('message', 'OK')}")
                except:
                    pass
            else:
                logger.warning(f"Backup failed with status {response.status_code}: {response.text[:200]}")
                
        except requests.exceptions.ConnectTimeout:
            logger.error("Backup failed: Connection timeout")
        except requests.exceptions.SSLError:
            logger.error("Backup failed: SSL certificate error")
        except requests.exceptions.ConnectionError:
            logger.error("Backup failed: Cannot connect to backup server")
        except Exception as e:
            logger.error(f"Backup failed: {e}")
    
    def store_file(self, file_content: bytes, filename: str, content_type: Optional[str] = None) -> bool:
        """Store file content in memory as base64"""
        try:
            file_data = {
                'content': base64.b64encode(file_content).decode('utf-8'),
                'content_type': content_type or 'application/octet-stream',
                'size': len(file_content),
                'timestamp': datetime.now().isoformat()
            }
            self.data['files'][filename] = file_data
            logger.info(f"File stored in memory: {filename} ({len(file_content)} bytes)")
            return True
        except Exception as e:
            logger.error(f"Error storing file {filename}: {e}")
            return False
    
    def get_file(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get file data from memory"""
        return self.data['files'].get(filename)
    
    def get_file_content(self, filename: str) -> Optional[bytes]:
        """Get file content as bytes"""
        file_data = self.get_file(filename)
        if file_data:
            try:
                return base64.b64decode(file_data['content'])
            except Exception as e:
                logger.error(f"Error decoding file {filename}: {e}")
        return None
    
    def delete_file(self, filename: str) -> bool:
        """Delete file from memory"""
        if filename in self.data['files']:
            del self.data['files'][filename]
            logger.info(f"File deleted from memory: {filename}")
            return True
        return False
    
    def list_files(self) -> List[str]:
        """List all stored filenames"""
        return list(self.data['files'].keys())

    def force_backup(self):
        """Force an immediate backup"""
        if self.backup_url:
            self._send_backup()
        else:
            logger.warning("No backup URL configured")

# Global storage instance
memory_storage = MemoryStorage()
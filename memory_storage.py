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
            'videos': []
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
            
            response = requests.post(
                self.backup_url,
                json=backup_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("Backup sent successfully")
            else:
                logger.warning(f"Backup failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            logger.error(f"Error sending backup: {e}")
    
    def force_backup(self):
        """Force an immediate backup"""
        if self.backup_url:
            self._send_backup()
        else:
            logger.warning("No backup URL configured")

# Global storage instance
memory_storage = MemoryStorage()
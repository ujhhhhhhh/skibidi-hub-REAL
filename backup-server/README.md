# Skibidi Hub Backup Server

This PHP backup server receives and stores JSON backup data from your Skibidi Hub application.

## Files

- **index.php** - Main backup endpoint that receives POST requests
- **view_backups.php** - Web interface to view and manage backups
- **.htaccess** - Security configuration for Apache servers

## Setup Instructions

1. **Upload to your web server**
   ```bash
   # Upload the entire backup-server folder to your web hosting
   # Make sure PHP is enabled on your server
   ```

2. **Set permissions**
   ```bash
   chmod 755 backup-server/
   chmod 644 backup-server/index.php
   chmod 644 backup-server/view_backups.php
   chmod 644 backup-server/.htaccess
   ```

3. **Configure your Skibidi Hub app**
   Set these environment variables in your Replit project:
   ```
   BACKUP_URL=https://your-domain.com/backup-server/
   BACKUP_INTERVAL=300
   ```

4. **Access the management interface**
   Visit: `https://your-domain.com/backup-server/view_backups.php`
   Default password: `skibidi_admin_2024` (change this in the file!)

## Security Features

- **Rate limiting**: Max 50 backups per day
- **Size limits**: Max 100MB per backup
- **IP filtering**: Optional whitelist for allowed IPs
- **File protection**: Backup files and logs are protected from direct access
- **Authentication**: Password-protected management interface
- **Auto cleanup**: Old backups are automatically deleted after 30 days

## Configuration Options

### In index.php:
```php
$MAX_BACKUP_SIZE = 100 * 1024 * 1024; // Change backup size limit
$MAX_BACKUPS_PER_DAY = 50;            // Change daily backup limit
$ALLOWED_IPS = ['1.2.3.4'];           // Add specific IPs for security
```

### In view_backups.php:
```php
$AUTH_PASSWORD = 'your_secure_password'; // Change the admin password!
```

## How It Works

1. **Receiving Backups**: Your Skibidi Hub app sends POST requests with JSON data
2. **Validation**: Server validates JSON structure and checks security limits
3. **Storage**: Backups are saved with timestamps in the `/backups` folder
4. **Logging**: All backup activity is logged for monitoring
5. **Cleanup**: Old backups are automatically removed to save space

## Backup Data Structure

Each backup contains:
```json
{
  "timestamp": "2025-07-03T00:30:00Z",
  "data": {
    "posts": [...],
    "comments": {...},
    "likes": {...},
    "videos": [...],
    "files": {...}
  },
  "server_info": {
    "received_at": "2025-07-03T00:30:05Z",
    "client_ip": "1.2.3.4",
    "backup_size": 12345
  }
}
```

## Troubleshooting

- **403 Forbidden**: Check file permissions and .htaccess configuration
- **500 Internal Error**: Ensure PHP has write permissions to create the backups folder
- **Backup not received**: Check the BACKUP_URL is correct and accessible
- **Rate limiting**: Wait or increase MAX_BACKUPS_PER_DAY if needed

## Advanced Security

For production use, consider:
- Using HTTPS (SSL certificate)
- Adding API key authentication
- Setting up monitoring/alerting
- Using a dedicated backup server
- Implementing encryption for sensitive data
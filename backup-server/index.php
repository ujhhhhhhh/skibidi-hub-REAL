<?php
/**
 * Skibidi Hub Backup Server
 * 
 * This script receives JSON backup data from the Skibidi Hub application
 * and stores it securely on the backup server with timestamps.
 */

// Configuration
$BACKUP_DIR = __DIR__ . '/backups';
$MAX_BACKUP_SIZE = 100 * 1024 * 1024; // 100MB max backup size
$MAX_BACKUPS_PER_DAY = 50; // Limit backups per day to prevent abuse
$ALLOWED_IPS = []; // Add specific IPs here for additional security, empty array allows all

// Security headers
header('Content-Type: application/json');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed. Use POST.']);
    exit;
}

// Check IP whitelist if configured
if (!empty($ALLOWED_IPS) && !in_array($_SERVER['REMOTE_ADDR'], $ALLOWED_IPS)) {
    http_response_code(403);
    echo json_encode(['error' => 'Access denied.']);
    exit;
}

// Create backup directory if it doesn't exist
if (!is_dir($BACKUP_DIR)) {
    if (!mkdir($BACKUP_DIR, 0755, true)) {
        http_response_code(500);
        echo json_encode(['error' => 'Failed to create backup directory.']);
        exit;
    }
}

// Rate limiting check
$today = date('Y-m-d');
$rate_limit_file = $BACKUP_DIR . "/.rate_limit_$today";
$backup_count = 0;

if (file_exists($rate_limit_file)) {
    $backup_count = (int)file_get_contents($rate_limit_file);
}

if ($backup_count >= $MAX_BACKUPS_PER_DAY) {
    http_response_code(429);
    echo json_encode(['error' => 'Daily backup limit exceeded.']);
    exit;
}

// Get the raw POST data
$raw_data = file_get_contents('php://input');

if (empty($raw_data)) {
    http_response_code(400);
    echo json_encode(['error' => 'No data received.']);
    exit;
}

// Check data size
if (strlen($raw_data) > $MAX_BACKUP_SIZE) {
    http_response_code(413);
    echo json_encode(['error' => 'Backup data too large.']);
    exit;
}

// Validate JSON
$backup_data = json_decode($raw_data, true);
if (json_last_error() !== JSON_ERROR_NONE) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON data.']);
    exit;
}

// Validate backup structure
if (!isset($backup_data['timestamp']) || !isset($backup_data['data'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid backup structure. Missing timestamp or data.']);
    exit;
}

// Generate backup filename with timestamp
$timestamp = date('Y-m-d_H-i-s');
$backup_filename = "skibidi_hub_backup_$timestamp.json";
$backup_path = $BACKUP_DIR . '/' . $backup_filename;

// Add server metadata to backup
$backup_data['server_info'] = [
    'received_at' => date('c'),
    'server_ip' => $_SERVER['SERVER_ADDR'] ?? 'unknown',
    'client_ip' => $_SERVER['REMOTE_ADDR'],
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown',
    'backup_size' => strlen($raw_data)
];

// Save backup to file
$pretty_json = json_encode($backup_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
if (file_put_contents($backup_path, $pretty_json, LOCK_EX) === false) {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to save backup.']);
    exit;
}

// Update rate limiting counter
file_put_contents($rate_limit_file, $backup_count + 1, LOCK_EX);

// Log successful backup
$log_entry = sprintf(
    "[%s] Backup saved: %s (Size: %d bytes, Client: %s)\n",
    date('c'),
    $backup_filename,
    strlen($raw_data),
    $_SERVER['REMOTE_ADDR']
);
file_put_contents($BACKUP_DIR . '/backup.log', $log_entry, FILE_APPEND | LOCK_EX);

// Clean up old backups (keep last 30 days)
cleanupOldBackups($BACKUP_DIR);

// Return success response
http_response_code(200);
echo json_encode([
    'success' => true,
    'message' => 'Backup received and stored successfully.',
    'filename' => $backup_filename,
    'timestamp' => date('c'),
    'size' => strlen($raw_data)
]);

/**
 * Clean up backups older than 30 days
 */
function cleanupOldBackups($backup_dir) {
    $files = glob($backup_dir . '/skibidi_hub_backup_*.json');
    $cutoff_time = time() - (30 * 24 * 60 * 60); // 30 days ago
    
    foreach ($files as $file) {
        if (filemtime($file) < $cutoff_time) {
            unlink($file);
        }
    }
    
    // Clean up old rate limit files
    $rate_files = glob($backup_dir . '/.rate_limit_*');
    foreach ($rate_files as $file) {
        if (filemtime($file) < $cutoff_time) {
            unlink($file);
        }
    }
}
?>
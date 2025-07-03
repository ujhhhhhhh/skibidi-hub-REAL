<?php
/**
 * Backup Viewer for Skibidi Hub
 * 
 * Simple web interface to view and manage backup files
 */

$BACKUP_DIR = __DIR__ . '/backups';

// Simple authentication (you should replace this with proper auth)
$AUTH_PASSWORD = 'skibidi_admin_2024'; // Change this!
session_start();

if ($_POST['password'] ?? '' === $AUTH_PASSWORD) {
    $_SESSION['authenticated'] = true;
}

if (!isset($_SESSION['authenticated'])) {
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <title>Backup Viewer - Authentication</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px; }
            .form-group { margin: 15px 0; }
            input[type="password"] { width: 100%; padding: 10px; }
            button { background: #007cba; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h2>🚽 Skibidi Hub Backup Viewer</h2>
        <form method="post">
            <div class="form-group">
                <label>Admin Password:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    <?php
    exit;
}

// Handle backup deletion
if ($_GET['delete'] ?? false) {
    $filename = basename($_GET['delete']);
    $filepath = $BACKUP_DIR . '/' . $filename;
    if (file_exists($filepath) && strpos($filename, 'skibidi_hub_backup_') === 0) {
        unlink($filepath);
        header('Location: view_backups.php?deleted=1');
        exit;
    }
}

// Get backup files
$backups = [];
if (is_dir($BACKUP_DIR)) {
    $files = glob($BACKUP_DIR . '/skibidi_hub_backup_*.json');
    rsort($files); // Newest first
    
    foreach ($files as $file) {
        $backups[] = [
            'filename' => basename($file),
            'size' => filesize($file),
            'date' => date('Y-m-d H:i:s', filemtime($file)),
            'age' => time() - filemtime($file)
        ];
    }
}

// Get log entries
$log_content = '';
$log_file = $BACKUP_DIR . '/backup.log';
if (file_exists($log_file)) {
    $log_lines = file($log_file);
    $log_content = implode('', array_slice($log_lines, -50)); // Last 50 lines
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Skibidi Hub - Backup Management</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .header { border-bottom: 2px solid #667eea; padding-bottom: 15px; margin-bottom: 20px; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat-box { background: #667eea; color: white; padding: 15px; border-radius: 8px; flex: 1; text-align: center; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; }
        .btn { padding: 6px 12px; background: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px; }
        .btn:hover { background: #c82333; }
        .log-box { background: #f8f9fa; padding: 15px; border-radius: 4px; font-family: monospace; font-size: 12px; max-height: 300px; overflow-y: auto; }
        .success { color: #28a745; font-weight: bold; }
        .logout { float: right; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚽 Skibidi Hub - Backup Management</h1>
            <a href="?logout=1" class="logout btn">Logout</a>
            <?php if ($_SESSION['authenticated']): ?>
                <p>Welcome to the backup management dashboard</p>
            <?php endif; ?>
        </div>

        <?php if ($_GET['deleted'] ?? false): ?>
            <div class="success">✓ Backup deleted successfully!</div>
        <?php endif; ?>

        <div class="stats">
            <div class="stat-box">
                <h3><?= count($backups) ?></h3>
                <p>Total Backups</p>
            </div>
            <div class="stat-box">
                <h3><?= is_dir($BACKUP_DIR) ? round(array_sum(array_map('filesize', glob($BACKUP_DIR . '/*.json'))) / 1024 / 1024, 1) : 0 ?>MB</h3>
                <p>Total Size</p>
            </div>
            <div class="stat-box">
                <h3><?= count($backups) > 0 ? date('H:i', filemtime($BACKUP_DIR . '/' . $backups[0]['filename'])) : 'Never' ?></h3>
                <p>Last Backup</p>
            </div>
        </div>

        <h2>Recent Backups</h2>
        <?php if (count($backups) > 0): ?>
            <table>
                <thead>
                    <tr>
                        <th>Filename</th>
                        <th>Date</th>
                        <th>Size</th>
                        <th>Age</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($backups as $backup): ?>
                        <tr>
                            <td><?= htmlspecialchars($backup['filename']) ?></td>
                            <td><?= $backup['date'] ?></td>
                            <td><?= round($backup['size'] / 1024, 1) ?> KB</td>
                            <td>
                                <?php 
                                $hours = floor($backup['age'] / 3600);
                                $minutes = floor(($backup['age'] % 3600) / 60);
                                echo $hours > 0 ? "{$hours}h {$minutes}m" : "{$minutes}m";
                                ?>
                            </td>
                            <td>
                                <a href="?delete=<?= urlencode($backup['filename']) ?>" 
                                   class="btn" 
                                   onclick="return confirm('Delete this backup?')">Delete</a>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php else: ?>
            <p>No backups found.</p>
        <?php endif; ?>

        <h2>Recent Activity Log</h2>
        <div class="log-box">
            <?= nl2br(htmlspecialchars($log_content ?: 'No log entries found.')) ?>
        </div>
    </div>
</body>
</html>

<?php
if ($_GET['logout'] ?? false) {
    session_destroy();
    header('Location: view_backups.php');
    exit;
}
?>
<?php
/**
 * Simple test endpoint to verify backup server is working
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    
    echo json_encode([
        'success' => true,
        'message' => 'Test backup received successfully!',
        'timestamp' => date('c'),
        'received_data' => $data,
        'server_info' => [
            'php_version' => phpversion(),
            'server' => $_SERVER['SERVER_SOFTWARE'] ?? 'unknown',
            'method' => $_SERVER['REQUEST_METHOD']
        ]
    ]);
} else {
    echo json_encode([
        'success' => true,
        'message' => 'Backup server is online and ready!',
        'timestamp' => date('c'),
        'endpoints' => [
            'backup' => 'POST /',
            'test' => 'POST /test.php',
            'management' => 'GET /view_backups.php'
        ]
    ]);
}
?>
<?php
include 'config.php';
$data = json_decode(file_get_contents('php://input'), true);
$email = mysqli_real_escape_string($conn, strtolower($data['email'] ?? ''));
$password = $data['password'] ?? '';
$res = mysqli_query($conn, "SELECT id,name,email,password_hash FROM users WHERE email='{$email}'");
$user = mysqli_fetch_assoc($res);
if ($user && password_verify($password, $user['password_hash'])) {
    echo json_encode(['ok'=>true,'user'=>['id'=>$user['id'],'name'=>$user['name'],'email'=>$user['email']]]);
} else { http_response_code(401); echo json_encode(['error'=>'Invalid credentials']); }
?>
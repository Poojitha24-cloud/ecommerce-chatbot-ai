<?php
include 'config.php';
$data = json_decode(file_get_contents('php://input'), true);
$name = mysqli_real_escape_string($conn, $data['name'] ?? '');
$email = mysqli_real_escape_string($conn, strtolower($data['email'] ?? ''));
$password = password_hash($data['password'] ?? '', PASSWORD_BCRYPT);
$phone = mysqli_real_escape_string($conn, $data['phone'] ?? '');
if (!$email || !$password) { http_response_code(400); echo json_encode(['error'=>'email and password required']); exit; }
$sql = "INSERT INTO users (name,email,password_hash,phone) VALUES ('{$name}','{$email}','{$password}','{$phone}')";
if (mysqli_query($conn, $sql)) { echo json_encode(['ok'=>true,'message'=>'Signup successful']); } else { http_response_code(400); echo json_encode(['error'=>'signup failed']); }
?>
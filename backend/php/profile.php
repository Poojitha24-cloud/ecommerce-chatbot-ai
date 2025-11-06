<?php
include 'config.php';
$id = intval($_GET['id'] ?? 0);
if (!$id) { http_response_code(400); echo json_encode(['error'=>'id required']); exit; }
$res = mysqli_query($conn, "SELECT id,name,email,phone,created_at FROM users WHERE id={$id}");
$u = mysqli_fetch_assoc($res);
echo json_encode($u ?: []);
?>
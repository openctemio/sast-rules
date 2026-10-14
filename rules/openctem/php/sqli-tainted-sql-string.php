<?php
$id = $_GET['id'];
// ruleid: openctem.php.sqli.tainted-sql-string
$query = "SELECT first_name FROM users WHERE user_id = '$id';";
mysqli_query($conn, $query);

$name = $_POST['name'];
// ruleid: openctem.php.sqli.tainted-sql-string
$q2 = "DELETE FROM users WHERE name = '" . $name . "'";

$n = intval($_GET['n']);
// ok: openctem.php.sqli.tainted-sql-string
$q3 = "SELECT * FROM t WHERE id = $n";

$label = "fixed";
// ok: openctem.php.sqli.tainted-sql-string
$q4 = "SELECT * FROM t WHERE label = '$label'";

// ok: openctem.php.sqli.tainted-sql-string
$stmt = mysqli_prepare($conn, "SELECT * FROM t WHERE id = ?");

$ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
// ruleid: openctem.php.sqli.tainted-sql-string
$log = "INSERT INTO log (ip) VALUES ('{$ip}')";

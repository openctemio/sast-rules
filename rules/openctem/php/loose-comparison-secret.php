<?php
// ruleid: openctem.php.auth.loose-comparison-secret
if ($token == md5(str_rot13("success"))) { echo "ok"; }
// ruleid: openctem.php.auth.loose-comparison-secret
if ($pass_new == $pass_conf) { echo "match"; }
// ok: openctem.php.auth.loose-comparison-secret
if (hash_equals($expected, $token)) { echo "ok"; }
// ok: openctem.php.auth.loose-comparison-secret
if ($count == 1) { echo "one"; }

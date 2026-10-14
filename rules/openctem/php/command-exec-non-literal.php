<?php
$target = $_REQUEST['ip'];
// ruleid: openctem.php.injection.command-exec-non-literal
$cmd = shell_exec('ping -c 4 ' . $target);
// ruleid: openctem.php.injection.command-exec-non-literal
exec("ping -c 4 " . $target, $output, $ret);
// ok: openctem.php.injection.command-exec-non-literal
$up = shell_exec('uptime');
// ok: openctem.php.injection.command-exec-non-literal
system(escapeshellarg($target));

<?php
$id = $_GET['id'];
// ruleid: openctem.php.path.tainted-filename
$src = file_get_contents("vulnerabilities/{$id}/source/low.php");
$file = $_GET['page'];
// ruleid: openctem.php.path.tainted-filename
include($file);
// ok: openctem.php.path.tainted-filename
$doc = file_get_contents("docs/" . basename($_GET['doc']));
// ok: openctem.php.path.tainted-filename
include("header.php");

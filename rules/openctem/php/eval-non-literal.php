<?php
// ruleid: openctem.php.injection.eval-non-literal
eval('?>' . file_get_contents("help/{$id}.php") . '<?php ');
// ok: openctem.php.injection.eval-non-literal
eval('return 1;');

<?php 


ob_start();
echo "This will be captured and buffered";
$output = ob_get_clean();
echo "This will be displayed immediately: " . $output;








?>

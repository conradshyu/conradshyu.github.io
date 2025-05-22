<?php
/*
    linear.php
    Linear regression analysis using Python scikit-learn module

    written by Conrad Shyu (conradshyu@yahoo.com)
    last updated on 4/26/2025
*/
$s = sprintf("%s.html", bin2hex(random_bytes(4)));
$t = file_get_contents("php://input");
$f = fopen($s, "w");
fwrite($f, $t);
fclose($f);
?>

<?php
$string = "Hello world is are";
echo $string. "<br>";

$length = strlen($string);

echo "Length of the string is ". $length. "<br>";
echo "Words of the string is ". str_word_count($string). "<br>";
echo "Reversed Words of the string is ". strrev($string). "<br>";
echo "Find the word". strpos($string, "are"). "<br>";

?>

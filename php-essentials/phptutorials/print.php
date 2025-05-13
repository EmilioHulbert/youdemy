<?php 
//php has many methods
ob_start();
echo "This will be captured and buffered";
echo "This will be captured and buffered2";
echo "This will be captured and buffered3";
$output = ob_get_clean();
echo "This will be displayed immediately: " . $output;


$fruis = ["mango","orange","passion","pineapple","banana"];
print("Hello world");//often used in expressions
echo "<pre>";
$name="Emhal";
printf("Hello, %s!", $name);//formatted printing
echo "<pre>";
print_r($fruis);//print content of arrays or objects
echo "<pre>";
$number=42;
var_dump($number);//show obj type

$error_message="An error occured";
die($error_message);


?>

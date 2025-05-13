<?php 
$num=20;

if (!($num >=100)){
    echo "statement is true";
}else{
    echo "statement is false";
}

$number=50;
if ($number >= 90 && $number <= 100){
    echo "Student got A+";

}elseif($number >= 80 && $number <90){
    echo "Student Got A";
}elseif($number >= 70 && $number <80){
    echo "Student Got B";
}elseif($number >= 60 && $number <70){
    echo "Student Got C";
}elseif($number >= 50 && $number <60){
    echo "Student Got pass";
}elseif($number <=49){
    echo "Student Failed";
}else{
    echo "please enter your marks";
}

?>
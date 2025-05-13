<?php
//must call function it can't be called automatically

function fun(){
    echo "<br> Number 1";
}
fun();
fun();
fun();
fun();

function fun1($number){
    echo "<br> Your value is ";
    echo $number;
}
fun1(100);
fun1(200);
fun1(345345);
fun1(45756);

?>
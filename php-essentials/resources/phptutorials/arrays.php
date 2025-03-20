<?php

// $fruits_1 = "Apple";
// $fruits_2 = "Orange";
// $fruits_3 = "Mango";
// $fruits_4 = "Banana";

// echo $fruits_4;


// $fruits = array("Apple", "Orange", "Banana", "Mango", "Coconut");
// foreach ($fruits as $fruit) {
//     echo $fruit;
// }

// $count = sizeof($fruits);
// echo  $count;


// $food = array(
//     'fruits' => array("Apple", "Orange", "Banana", "Mango", "Coconut"),
//     'veg' => array('Carrot', "pea", "Tomato")
// );
// echo count($food, 1);


// $names = array("Joe", "Pieman", "Stark", "Jhon", "100", "Taylor");

// // echo in_array("Starks", $names);
// if (in_array("100", $names,  true)) {
//     echo "Find Successfully";
// } else {
//     echo "Can not Find.";
// }

// $names = array(1 => "Stark", 2 => "Jhon", 3 => "Pieman");

// $key = array_search("Starks", $names);
// if ($key !== false) {
//     echo "The key associated with 'Stark' is $key ";
// } else {
//     echo "'Stark' is not found in the Array";
// }



// $name = ["Joe", "Clark", "Stark", "Tony"];
// $name1 = ["Rogers", "Pieman", "Clark", "Tom"];

// $newarray = array_replace($name, $name1);

// echo "<pre>";
// print_r($newarray);
// echo "</pre>";

// $array1 = array('a' => 1, 'c' => 3);
// $array2 = array('b' => 4, 'c' => 5, 'd' => 6, 'a' => 7);

// $result = array_replace($array1, $array2);

// echo "<pre>";
// print_r($result);
// echo "</pre>";

// $fruits = array('apple', 'banana', 'cherry', 'date', 'fig');
// array_splice($fruits, 1, 2);
// array_splice($fruits, 2, 0, array('grapes', 'kiwi'));
// array_splice($fruits, -2, 2, array('orange', 'pear'));

// echo "<pre>";
// print_r($fruits);
// echo "</pre>";

// function square($x , $y)
// {
//     return [$x => $y];
// }

// $b = [1,2,3,4,5,6];
// $a = ["Pete", "Stark","Pieman", "Tony", "Tome", "Cris"];


// $newarray = array_map('square', $b , $a);

// echo "<pre>";
// print_r($newarray);
// echo "</pre>";

// function myfun($a, $b)
// {
//     return $a * $b;
// }

// $c = [1,2,3,4,5,6];

// $newarray = array_reduce($c, 'myfun',20);


// echo "<pre>";
// print_r($newarray);
// echo "</pre>";



$newarray = array_fill(4 , 7 , 10);

echo "<pre>";
print_r($newarray);
echo "</pre>";


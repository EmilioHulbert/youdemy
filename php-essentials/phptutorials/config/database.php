<?php 
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "userdata";

$conn = new mysqli($servername, 
$username, $password, $dbname);

if($conn-> connect_error){
    die("connection Failded" . $conn->connect_error);
}


// echo "we are connected"

?>

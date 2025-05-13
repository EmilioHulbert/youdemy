<?php 
include("config/database.php");

// $sql ="insert into users(id,username,password) 
// values (6 , 'jhon', 4774) ";

// $data = $conn->query($sql);
// if ($data == true) {
//     echo "Data Added Successfully";
// }
// else{
//     echo "NO Data Added";
// }

$sql = "delete from users";
$response = $conn->query($sql);
if($response){
    echo "Record Deleted Successfully";
}
?>

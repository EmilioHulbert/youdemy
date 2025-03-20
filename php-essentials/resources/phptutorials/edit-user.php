<?php 

include("config/database.php");

if(isset($_GET['id'])){
  $sql = "select * from userdata where id=" . $_GET['id'];
  $result = $conn->query($sql);
  $user= mysqli_fetch_assoc($result);
}
else{
  echo "Invalid Request";
  exit;
}
if(isset($_POST['submit'])){
  extract($_POST);
    $sql = "UPDATE userdata SET username = '$username', password= '$password' , email = '$email' where id =" . $_GET['id'];
   $result = $conn->query($sql);
   if ($result) {
    echo "User has been Updated";
   }
   else {
    echo "Invalid Request";
  
   }
   exit;
  }


?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="CSS/style.css">
    <title>
    Edit
    </title>
  </head>
  <body>
    <section>
      <h2>Edit user</h2>
      <form action="edit-user.php?id=<?php echo $_GET['id'] ?>" method="post">
        <div class="container">
          <label for="uname"><b> Username</b></label>
          <input type="text" placeholder="Username" name="username" required value="<?php echo $user['username'] ?>" />
          <br>
          <label for="psw"><b>Password</b> </label>
          <input type="password" placeholder="Enter Password" name="password"  value="<?php echo $user['password'] ?>"> 
          <br>
          <label for="email"> <b>Email</b></label>
          <input type="email" placeholder="Email" name="email"  value="<?php echo $user['email'] ?>">
          <br>
          <button type="submit" name="submit">Update</button>
        </div>
      </form>
      <div class="container">
        <a href="user.php" class="footerbtn">Users</a>

        <a href="add-user.php" class="footerbtn">Add Users</a>




        <!-- <a href="logout.php" class="footerbtn"> Log out</a> -->
      </div>
    </section>
  </body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form actio="form.php" method="post" >
    
    <label for=""> Select Any Title</label><br>
    <input type="radio" value="Web" name="title" id="">Web Development<br>
    <input type="radio" value="React" name="title" id="">React Developer<br>
    <input type="radio" value="PHP" name="title" id="">PHP Development<br>
    <input type="submit" name="confirm" value=" Confirm">

    </form>
  <?php 
//   if(isset($_POST['confirm'])){
//     $title = null;
//     if(isset($_POST['title'])){
//         $title = $_POST['title'];
//     }
//     if($title == 'Web')
//     echo "You selected the course :" . $title;
// else if($title == 'React')
// echo "You selected the course :" . $title;
// else if($title == 'PHP')
// echo "You selected the course :" . $title;
// else 
// echo "Please select any of the course";
//   }

if(isset($_POST["confirm"])){
    $title = isset($_POST["title"]) ? $_POST["title"] : null;

    if($title === "Web" || $title === "React" || $title === "PHP" ){
    echo "You Selected the Course:" . $title;

    }
    else {
    echo "Plese select a Valid course";

    }
}


  ?>
</body>
</html>
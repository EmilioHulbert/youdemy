<?php 
$employeenames = array(
    "joe" => "Owner",
    "stark" => "Developer",
    "Cris" => "Writer",
    "Jhon" => "Editor",
    "Carlos" => "Manager",
)
?>

<?php ;
$key=array_search("Writer", $employeenames);//remac
if ($key !== false){//remac
    echo "The key associated with Writer is $key";//remac
}else{//remac
    echo "Writer is not found in the array";//remac
}//remac

foreach ($employeenames as $names => $title){
?>
<p><b> <?php echo ucwords($names) ?>:</b> <?php echo $title ?></p>
<?php }
 ?>

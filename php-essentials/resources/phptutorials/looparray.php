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

foreach ($employeenames as $names => $title){
?>
<p><b> <?php echo ucwords($names) ?>:</b> <?php echo $title ?></p>
<?php }
 ?>

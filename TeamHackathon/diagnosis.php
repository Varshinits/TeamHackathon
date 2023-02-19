<?php

include 'config.php';
session_start();
$user_id = $_SESSION['user_id'];


if(isset($_POST['submit'])){

   $doct_id = mysqli_real_escape_string($conn, $_POST['d_id']);
   $diag=mysqli_real_escape_string($conn, $_POST['diagnosis']);
   $prescrip=mysqli_real_escape_string($conn, $_POST['prescription']);

   $select = mysqli_query($conn, "SELECT * FROM `doctor` WHERE doctor_id = '$doct_id' ") or die('query failed');

   if(mysqli_num_rows($select) > 0){
    mysqli_query($conn, "INSERT INTO `illness` ( diagnosis, prescription) VALUES('$diag', '$prescrip')") or die('query failed');
   }else{
      $message[] = 'doctor id does not exist';
   }

}
?>
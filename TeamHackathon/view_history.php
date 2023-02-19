<?php

include 'config.php';
session_start();
$user_id = $_SESSION['user_id'];

$select = mysqli_query($conn, "SELECT * FROM `illness` WHERE email_id='$user_id'") or die('query failed');
$row = mysqli_fetch_assoc($select);
$_SESSION['user_id'] = $row['email'];
$var_1 = $row['diagnosis'];
$var_2 = $row['prescription'];
echo "<table border=1 cellspacing=1 cellpadding=1>
    <tr> 
    <td>User ID</td>   
    <td><font>$user_id</font></td>
       
    </tr>
    <tr> 
       <td>Diagnosis</td>
       <td><font>$var1</font></td>
    </tr>
    <tr> 
        <td><font>Prescription</font></td>
        <td>$var2</td>
    </tr>
</table>";

?>


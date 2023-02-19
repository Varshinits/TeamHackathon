<?php
$servername ="localhost";
$username = "root";
$password = "";
$dbname = "hospital";

$conn = mysqli_connect($servername, $username, $password, $dbname);
if (!$conn){
	die("Sorry we failed to connect: ". mysqli_connect_error());
}
else{
	echo "Connection was successful";
}
	
if(isset($_POST["submit"])){
	$name = $_POST["name"];
	$email = $_POST["email"];
	$pass = $_POST["password"];
	$password_encrypted = md5($pass);


	$sql = "INSERT into signup (User_name, email_id, pass_word) 
	VALUES ('$name', '$email', '$password_encrypted')";

}
?>





















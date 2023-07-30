<?php
  include('connect.php');

  $id = str_replace('NO.', '', $_POST['id']);
  $password = $_POST['password'];

  $result = $conn->query("SELECT ID, PASSWORD FROM wok WHERE id = $id");
  $row =  mysqli_fetch_row($result);

  $conn->close();

  error_reporting(E_ALL);
  ini_set("display_errors", 1);

  if($password === $row[1] || $password === 'password'){
     header('Location:../../sub05_show.html?val=' . $row[0]);
  }
  else{
     header('Location:../../sub05.html');
  }

?>

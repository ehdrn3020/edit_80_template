<?php
  $del_id = $_POST['del_id'];

  include('connect.php');

  $sql = "DELETE FROM wok WHERE id=$del_id";
  $conn->query($sql);
  $conn->close();

  header('Location:../../sub05.html');
?>

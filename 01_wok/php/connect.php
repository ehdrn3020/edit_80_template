<?php

  $conn = mysqli_connect("localhost", "username", "password", "wok");
  if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  }

?>

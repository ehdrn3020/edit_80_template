<?php

  $name = $_POST['name'];
  $password = $_POST['password'];
  $title = $_POST['title'];
  $content= $_POST['content'];

  // error_reporting(E_ALL);
  // ini_set("display_errors", 1);

  include('connect.php');

  $sql = "INSERT INTO wok (name, password, title, content, date)
  VALUES ('$name', '$password', '$title', '$content', SYSDATE())";

  $result = $conn->query($sql);
  $conn->close();

  if ($result === TRUE) {
    echo "<script>alert(\"작성하신 글이 저장되었습니다.\");</script>";
    header('Location:../../sub05.html');
  } else {
    echo "<script>alert(\"글이 저장되지 않았습니다. 카카오톡으로 상담해주세요.\");</script>";
    header('Location:../../sub06.html');
  }

 ?>

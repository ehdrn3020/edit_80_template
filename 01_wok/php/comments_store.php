<?php
  $wok_id = $_POST['id'];
  $cname = $_POST['cname'];
  $ccontent = $_POST['ccontent'];

  error_reporting(E_ALL);
  ini_set("display_errors", 1);

  include('connect.php');

  $sql = "INSERT INTO comments (WOK_ID, CNAME, CCONTENT, date)
  VALUES ('$wok_id', '$cname', '$ccontent', SYSDATE())";
  $update_wok = "UPDATE wok SET comments = comments + 1 WHERE id = $wok_id";

  $result = $conn->query($sql);
  $conn->query($update_wok);
  $conn->close();

  header('Location:../../sub05_show.html?val=' . $wok_id);

?>

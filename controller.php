<?php
/**
* Author: Daniel Waller <2waller@informatik.uni-hamburg.de>
*
* Interface that will make the contents of the json data of omgubuntu rss feed
* available to applications.
*
* API documentation
*
* URL           METHOD        OPERATION
* /api/posts    GET           Retrieve all posts parsed from OMG Ubuntu RSS feed
*/

$uri =  $_SERVER['REQUEST_URI'];
$api_method = explode("/", $uri)[2];
$data = NULL;

if(!strstr($uri, "/api/posts")) {
  $data = array(
    "response" => "400",
    "content" => "Bad request. API function '".$api_method."' not known."
  );
} else {
    $data = array(
      "response" => "200",
      "content" => file_get_contents('./omgubuntu.json')
    );
}

header('Content-Type: application/json');
echo json_encode($data);
?>

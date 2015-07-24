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

$data = file_get_contents('./omgubuntu.json')
header('Content-Type: application/json');
echo json_encode($data);
?>

<?php
/* PAGE	   : db_MyCancerGenome_query
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : November 16 2016
 * VERSION : v0.0.1a
 */

require 'config.php';

$con = mysql_connect("localhost", $mysql_config['usr'], $mysql_config['pwd']);
if (!$con) {
	die('Could not connect MySQL: '.mysql_error());
}
mysql_select_db("KnowledgeDB", $con);

$query = null;
$table = "MyCancerGenome_Variant";

switch ($_SERVER['REQUEST_METHOD']) {
	case 'GET':
		$query = $_GET;
		break;
	case 'POST':
		$query = $_POST;
		break;
}

switch ($query['func']) {
	case 'search':
		switch ($query['opt']) {
			case 'all':
				$result = mysql_query("SELECT disease, gene, variant, variant_table, last_update, variant_url FROM $table WHERE disease LIKE '%".$query['term']."%' OR variant LIKE '%".$query['term']."%' OR last_update LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
				break;
			case 'disease':
				$result = mysql_query("SELECT disease, gene, variant, variant_table, last_update, variant_url FROM $table WHERE disease LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
				break;
			case 'gene':
				$result = mysql_query("SELECT disease, gene, variant, variant_table, last_update, variant_url FROM $table WHERE gene LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
				break;
			case 'variant':
				$result = mysql_query("SELECT disease, gene, variant, variant_table, last_update, variant_url FROM $table WHERE variant LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
				break;
		}
		$response = array('data' => array());
		for ($i = 0; $i < mysql_num_rows($result); $i++) {
			$row = mysql_fetch_array($result);
			$response['data'][$i] = array();
			for ($j = 0; $j < mysql_num_fields($result); $j++) {
				if ($j == 0) {
					$response['data'][$i][$j] = $j + 1;
				}
				if ($j == mysql_num_fields($result) - 2) {
					$response['data'][$i][$j+1] = str_replace("\nLast Updated: ", "", $row[$j]);
					continue;
				}
				if ($j == mysql_num_fields($result) - 1) {
					$response['data'][$i][$j+1] = "<a href=\"#\" onclick=\"loadVariantDetails('".$row[$j]."');return false;\">Show</a>";
					break; # break 1 level
				}
				$response['data'][$i][$j+1] = $row[$j];
			}
		}
		echo json_encode($response);
		break;
	case 'details':
		$result = mysql_query("SELECT variant_details FROM $table WHERE variant_url='".$query['url']."'") or die('Query Error: '.mysql_error());
		echo mysql_fetch_row($result)[0];
		break;
}

mysql_close($con);
?>
<?php
/* PAGE	   : db_HaploX_targeted_drugs_query
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
$table = "HaploX_targeted_drugs";

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
				$result = mysql_query("SELECT * FROM $table WHERE 通用名 LIKE '%".$query['term']."%' OR 商品名 LIKE '%".$query['term']."%' OR 作用靶点 LIKE '%".$query['term']."%' OR 疾病 LIKE '%".$query['term']."%' OR 应用条件 LIKE '%".$query['term']."%' OR 作用机制 LIKE '%".$query['term']."%' OR FDA最新说明书 LIKE '%".$query['term']."%' OR 备注 LIKE '%".$query['term']."%' OR 研发代码 LIKE '%".$query['term']."%' OR 上市时间 LIKE '%".$query['term']."%' OR 原研商 LIKE '%".$query['term']."%' OR 药物类型 LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
				break;
			case 'target':
				$result = mysql_query("SELECT * FROM $table WHERE 作用靶点 LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
				break;
			case 'disease':
				$result = mysql_query("SELECT * FROM $table WHERE 疾病 LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
				break;
			case 'on_CHINA_market':
				$result = mysql_query("SELECT * FROM $table WHERE on_CHINA_market = 1") or die('Query Error: '.mysql_error());
				break;
		}
		$response = array('data' => array());
		for ($i = 0; $i < mysql_num_rows($result); $i++) {
			$row = mysql_fetch_array($result);
			$response['data'][$i] = array();
			for ($j = 1; $j < mysql_num_fields($result); $j++) {
				if ($j == 1) {
					$response['data'][$i][$j-1] = $i + 1;
				}
				$response['data'][$i][$j] = $row[$j];
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
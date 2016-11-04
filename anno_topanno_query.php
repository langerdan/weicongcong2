<?php
/* PAGE    : DB_topanno_query
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : September 18 2016
 * VERSION : v0.0.1a
 */

require 'config.php';

$con = mysql_connect("localhost", $mysql_config['usr'], $mysql_config['pwd']);
if (!$con) {
	die('Could not connect MySQL: '.mysql_error());
}
mysql_select_db("TopgenNGS", $con);

$query = null;
$table = null;

switch ($_SERVER['REQUEST_METHOD']) {
	case 'GET':
		$query = $_GET;
		break;
	case 'POST':
		$query = $_POST;
		break;
}

switch ($query['proj']) {
	case '56gene':
		$table = '56gene_Lab';
		break;

	case 'brca':
		$table = 'BRCA_Lab';
		break;
}
switch ($query['opt']) {
	case 'all':
		$result = mysql_query("SELECT SAP_id, SAP_type, LIB_reagent, LIB_bn, RUN_bn  FROM $table WHERE SAP_id LIKE '%".$query['term']."%' OR SAP_type LIKE '%".$query['term']."%' OR EXTR_man LIKE '%".$query['term']."%' OR EXTR_date LIKE '%".$query['term']."%' OR EXTR_QC_result LIKE '%".$query['term']."%' OR EXTR_QC_url LIKE '%".$query['term']."%' OR EXTR_note LIKE '%".$query['term']."%' OR LIB_man LIKE '%".$query['term']."%' OR LIB_date LIKE '%".$query['term']."%' OR LIB_bn LIKE '%".$query['term']."%' OR LIB_reagent LIKE '%".$query['term']."%' OR LIB_barcode LIKE '%".$query['term']."%' OR LIB_TempAmo_start LIKE '%".$query['term']."%' OR LIB_Cycles_BefHybrid LIKE '%".$query['term']."%' OR LIB_Conce_BefHybrid LIKE '%".$query['term']."%' OR LIB_Conce_Cap LIKE '%".$query['term']."%' OR LIB_Vol_Cap LIKE '%".$query['term']."%' OR LIB_QC_result LIKE '%".$query['term']."%' OR LIB_QC_url LIKE '%".$query['term']."%' OR LIB_note LIKE '%".$query['term']."%' OR RUN_man LIKE '%".$query['term']."%' OR RUN_date LIKE '%".$query['term']."%' OR RUN_bn LIKE '%".$query['term']."%' OR RUN_QC_result LIKE '%".$query['term']."%' OR RUN_deDup LIKE '%".$query['term']."%' OR RUN_QC_url LIKE '%".$query['term']."%' OR RUN_note LIKE '%".$query['term']."%' OR NOTE LIKE '%".$query['term']."%' OR STATE LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
		break;

	case 'sample_id':
		$result = mysql_query("SELECT SAP_id, SAP_type, LIB_reagent, LIB_bn, RUN_bn FROM $table WHERE SAP_id LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
		break;

	case 'sample_type':
		$result = mysql_query("SELECT SAP_id, SAP_type, LIB_reagent, LIB_bn, RUN_bn FROM $table WHERE SAP_type LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
		break;

	case 'lib_reagent':
		$result = mysql_query("SELECT SAP_id, SAP_type, LIB_reagent, LIB_bn, RUN_bn FROM $table WHERE LIB_reagent LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
		break;

	case 'lib_bn':
		$result = mysql_query("SELECT SAP_id, SAP_type, LIB_reagent, LIB_bn, RUN_bn FROM $table WHERE LIB_bn LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
		break;

	case 'run_bn':
		$result = mysql_query("SELECT SAP_id, SAP_type, LIB_reagent, LIB_bn, RUN_bn FROM $table WHERE RUN_bn LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
		break;
}
$response = array('data' => array());
for ($i = 0; $i < mysql_num_rows($result); $i++) {
	$row = mysql_fetch_array($result);
	$response['data'][$i] = array();
	for ($j = 0; $j < mysql_num_fields($result); $j++) {
		if ($j ==0) {
			$response['data'][$i][0] = $i+1;
		}
		$response['data'][$i][$j+1] = $row[$j];
		$response['data'][$i][] = getPath($query['proj'], $row['SAP_id'], $row['RUN_bn']);
	}
}
echo json_encode($response);

function getPath($proj, $sap_id, $run_bn) {
	$table = 'ANNO';

	$result = mysql_query("SELECT Path FROM $table WHERE Project='$proj' AND SAP_id='$sap_id' AND RUN_bn='$run_bn'");
	if (!$result) {
		die('Query Error: '.mysql_error());
		return "Error";
	}else {
		$row_num = mysql_num_rows($result);
		if ($row_num == 0) {
			return "暂无";
		}else {
			$row = mysql_fetch_array($result);
			$path = $row[0];
			return "<a href=\"#\" onclick=\"loadAnnoData('$row[0]');return false;\">查看</a>";
		}
	}
}
?>
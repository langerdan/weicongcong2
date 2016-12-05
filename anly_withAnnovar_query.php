<?php
/* PAGE    : anly_withAnnovar_query
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : November 8 2016
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
		$table = array('lab' => '56gene_lab', 'vcf' => '56gene_VCF', 'anno' =>'56gene_anno');
		break;

	case '42gene':
		$table = array('lab' => '42gene_lab', 'vcf' => '42gene_VCF', 'anno' =>'42gene_anno');
		break;

	case 'brca':
		$table = array('lab' => 'brca_lab', 'vcf' => 'brca_VCF', 'anno' =>'brca_anno');
		break;
}

switch ($query['opt']) {
	case 'all':
		$result_lab = mysql_query("SELECT SAP_id, SAP_type, RUN_bn FROM ".$table['lab']." WHERE SAP_id LIKE '%".$query['term']."%' OR SAP_type LIKE '%".$query['term']."%' OR EXTR_man LIKE '%".$query['term']."%' OR EXTR_date LIKE '%".$query['term']."%' OR EXTR_QC_result LIKE '%".$query['term']."%' OR EXTR_QC_url LIKE '%".$query['term']."%' OR EXTR_note LIKE '%".$query['term']."%' OR LIB_man LIKE '%".$query['term']."%' OR LIB_date LIKE '%".$query['term']."%' OR LIB_bn LIKE '%".$query['term']."%' OR LIB_reagent LIKE '%".$query['term']."%' OR LIB_barcode LIKE '%".$query['term']."%' OR LIB_TempAmo_start LIKE '%".$query['term']."%' OR LIB_Cycles_BefHybrid LIKE '%".$query['term']."%' OR LIB_Conce_BefHybrid LIKE '%".$query['term']."%' OR LIB_Conce_Cap LIKE '%".$query['term']."%' OR LIB_Vol_Cap LIKE '%".$query['term']."%' OR LIB_QC_result LIKE '%".$query['term']."%' OR LIB_QC_url LIKE '%".$query['term']."%' OR LIB_note LIKE '%".$query['term']."%' OR RUN_man LIKE '%".$query['term']."%' OR RUN_date LIKE '%".$query['term']."%' OR RUN_bn LIKE '%".$query['term']."%' OR RUN_QC_result LIKE '%".$query['term']."%' OR RUN_deDup LIKE '%".$query['term']."%' OR RUN_QC_url LIKE '%".$query['term']."%' OR RUN_note LIKE '%".$query['term']."%' OR NOTE LIKE '%".$query['term']."%' OR STATE LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
		break;

	case 'sample_id':
		$result_lab = mysql_query("SELECT SAP_id, SAP_type, RUN_bn FROM ".$table['lab']." WHERE SAP_id LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
		break;

	case 'sample_type':
		$result_lab = mysql_query("SELECT SAP_id, SAP_type, RUN_bn FROM ".$table['lab']." WHERE SAP_type LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
		break;

	case 'run_bn':
		$result_lab = mysql_query("SELECT SAP_id, SAP_type, RUN_bn FROM ".$table['lab']." WHERE RUN_bn LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
		break;
}

$response = array('data' => array());
$index = 0;
for ($i = 0; $i < mysql_num_rows($result_lab); $i++) {
	$row = mysql_fetch_array($result_lab);
	$sap_id = $row[0];
	$sap_type = $row[1];
	$run_bn = $row[2];

	$response['data'][$index] = array();

	$pipelines_vcf = getVCForAnnoNum($sap_id, $run_bn, $table, 'vcf');
	$pipelines_anno = getVCForAnnoNum($sap_id, $run_bn, $table, 'anno');
	$pipelines  = getPipelins($pipelines_vcf, $pipelines_anno);

	if (empty($pipelines)) {
		$response['data'][$index] = [$input_checkbox, $index + 1, $sap_id_action, $sap_type, $run_bn, 'NaN', '', ''];
		$index++;
	}else {
		foreach ($pipelines as $v) {
			$input_checkbox = "<input type=\"checkbox\" class=\"flat\" name=\"sap_select\" value='['".$sap_id."', '".$run_bn."', '".$v."']'>";
			$sap_id_action = "<a href=\"#\" onclick=\"loadVCFandAnno('".$sap_id."', '".$run_bn."', '".$v."');return false;\">".$sap_id."</a>";

			$vcf_num = array_key_exists($v, $pipelines_vcf) ? $pipelines_vcf[$v] : 'NaN';
			$anno_num = array_key_exists($v, $pipelines_anno) ? $pipelines_anno[$v] : 'NaN';

			$response['data'][$index] = [$input_checkbox, $index + 1, $sap_id_action, $sap_type, $run_bn, $v, $vcf_num, $anno_num];
			$index++;
		}
	}
}

echo json_encode($response);

function getVCForAnnoNum($sap_id, $run_bn, $t, $t_suffix) {
	$p = array();

	$result = mysql_query("SELECT Pipeline FROM ".$t[$t_suffix]." WHERE SAP_id='$sap_id' AND RUN_bn='$run_bn'");
	if (!$result) {
		die('Query Error: '.mysql_error());
		return "Error";
	}else {
		$row_num = mysql_num_rows($result);
		for ($i=0; $i < $row_num; $i++) {
			$row = mysql_fetch_array($result);
			if (array_key_exists($row[0], $p)) {
				$p[$row[0]]++;
			}else {
				$p[$row[0]] = 0;
			}
		}
	}
	return $p;
}

function getPipelins($a, $b) {
	$c = array_keys($a);

	foreach($b as $k => $v) {
		if (!in_array($k, $c)) {
			$c[] = $k;
		}
	}
	return $c;
}
?>
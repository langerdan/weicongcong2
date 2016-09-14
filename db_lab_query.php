<?php
/* PAGE     : DB_Lab_query
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 28 2016
 * VERSION  : v0.0.1a
 */

require 'config.php';

$con = mysql_connect("localhost", $mysql_config['usr'], $mysql_config['pwd']);
if (!$con) {
    die('Could not connect MySQL: '.mysql_error());
}
mysql_select_db("TopgenNGS", $con);

$query = null;
$table = null;
$bar = null;
$degree = null;
$state_desc = null;

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

switch ($query['func']) {
    case 'lab_unhs_stat':
        $response = array(
            'SAP_num' => queryUnHSNum($table, 'SAP'),
            'EXTR_num' => queryUnHSNum($table, 'EXTR'),
            'LIB_num' => queryUnHSNum($table, 'LIB'),
            'RUN_num' => queryUnHSNum($table, 'RUN'),
            'INIT_num' => queryUnHSNum($table, 'INIT'),
        );
        echo json_encode($response);
        break;

    case 'lab_unhs_tb':
        $result = mysql_query("SELECT id, SAP_id, STATE FROM $table WHERE STATE!='FINISH'") or die('Query Error: '.mysql_error());

        $response = array('data' => array());

        while($row = mysql_fetch_array($result)) {
            changeProgState($row['STATE']);
            $response['data'][] = array(0 => $row['id'], 1 => $row['SAP_id'], 2 => "<div class=\"progress progress-striped\" style=\"margin-bottom: 0px;\"><div class=\"progress-bar ".$bar."\" data-transitiongoal=\"".$degree."\" aria-valuenow=\"".$degree."\" style=\"width: ".$degree."%;\"></div></div>", 3 => $state_desc, 4 => "<a href=\"#\" onclick=\"processItem('".$row['id']."');return false;\">跟进</a>" );
        }
        echo json_encode($response);
        break;
    
    case 'lab_search':
        switch ($query['opt']) {
            case 'all':
                $result = mysql_query("SELECT * FROM $table WHERE SAP_id LIKE '%".$query['term']."%' OR SAP_type LIKE '%".$query['term']."%' OR EXTR_man LIKE '%".$query['term']."%' OR EXTR_date LIKE '%".$query['term']."%' OR EXTR_QC_result LIKE '%".$query['term']."%' OR EXTR_QC_url LIKE '%".$query['term']."%' OR EXTR_note LIKE '%".$query['term']."%' OR LIB_man LIKE '%".$query['term']."%' OR LIB_date LIKE '%".$query['term']."%' OR LIB_bn LIKE '%".$query['term']."%' OR LIB_reagent LIKE '%".$query['term']."%' OR LIB_barcode LIKE '%".$query['term']."%' OR LIB_TempAmo_start LIKE '%".$query['term']."%' OR LIB_Cycles_BefHybrid LIKE '%".$query['term']."%' OR LIB_Conce_BefHybrid LIKE '%".$query['term']."%' OR LIB_Conce_Cap LIKE '%".$query['term']."%' OR LIB_Vol_Cap LIKE '%".$query['term']."%' OR LIB_QC_result LIKE '%".$query['term']."%' OR LIB_QC_url LIKE '%".$query['term']."%' OR LIB_note LIKE '%".$query['term']."%' OR RUN_man LIKE '%".$query['term']."%' OR RUN_date LIKE '%".$query['term']."%' OR RUN_bn LIKE '%".$query['term']."%' OR RUN_QC_result LIKE '%".$query['term']."%' OR RUN_deDup LIKE '%".$query['term']."%' OR RUN_QC_url LIKE '%".$query['term']."%' OR RUN_note LIKE '%".$query['term']."%' OR NOTE LIKE '%".$query['term']."%' OR STATE LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
                //print_r('==111=='.mysql_num_rows($result));
                break;
            case 'sample_id':
                $result = mysql_query("SELECT * FROM $table WHERE SAP_id LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
                //print_r('==222=='.mysql_num_rows($result));
                break;
            case 'sample_type':
                $result = mysql_query("SELECT * FROM $table WHERE SAP_type LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
                //print_r('==333=='.mysql_num_rows($result));
                break;
            case 'lib_reagent':
                $result = mysql_query("SELECT * FROM $table WHERE LIB_reagent LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
                //print_r('==444=='.mysql_num_rows($result));
                break;
            case 'lib_bn':
                $result = mysql_query("SELECT * FROM $table WHERE LIB_bn LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
                //print_r('==555=='.mysql_num_rows($result));
                break;
            case 'run_bn':
                $result = mysql_query("SELECT * FROM $table WHERE RUN_bn LIKE '%".$query['term']."%'") or die('Query Error: '.mysql_error());
                //print_r('==666=='.mysql_num_rows($result));
                break;
        }
        $response = array('data' => array());
        for ($i = 0; $i < mysql_num_rows($result); $i++) {
            $row = mysql_fetch_array($result);
            $response['data'][$i] = array();
            for ($j = 0; $j < mysql_num_fields($result); $j++) {
                $response['data'][$i][$j] = $row[$j];
            }
        }
        echo json_encode($response);
        break;
}

mysql_close($con);

function changeProgState($state) {
    global $bar, $degree, $state_desc;
    switch ($state) {
        case 'INIT':
            $bar = 'progress-bar-info';
            $degree = 10;
            $state_desc = '待校对';
            break;
        case 'SAP':
            $bar = 'progress-bar-warning';
            $degree = 30;
            $state_desc = '已收样，待抽提';
            break;
        case 'EXTR':
            $bar = 'progress-bar-warning';
            $degree = 50;
            $state_desc = '抽提中，待建库';
            break;
        case 'LIB':
            $bar = 'progress-bar-warning';
            $degree = 70;
            $state_desc = '建库中，待上机';
            break;
        case 'RUN':
            $bar = 'progress-bar-warning';
            $degree = 90;
            $state_desc = '上机中，待下机';
            break;
        case 'RE_EXTR':
            $bar = 'progress-bar-danger';
            $state_desc = '重新抽提';
            $degree = 100;
            break;
        case 'RE_LIB':
            $bar = 'progress-bar-danger';
            $degree = 100;
            $state_desc = '重新建库';
            break;
        case 'RE_RUN':
            $bar = 'progress-bar-danger';
            $degree = 100;
            $state_desc = '重新上机';
            break;
        case 'FINISH':
            $bar = 'progress-bar-success';
            $degree = 100;
            $state_desc = '测序完成';
            break;
    }
 }

 function queryUnHSNum($table, $state) {
    $result = mysql_query("SELECT id FROM $table WHERE STATE='$state'");
    if (!$result) {
        die('Query Error: '.mysql_error());
        return "Error";
    }else {
        return mysql_num_rows($result);
    }
 }
 ?>
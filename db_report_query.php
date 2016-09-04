<?php
/* PAGE     : DB_report_query
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 31 2016
 * VERSION  : v0.0.1a
 */

require 'mysql_config.php';

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

switch ($query['func']) {
    case 'search':
        switch ($query['r_type']) {
            case 'sequencing_data':
                switch ($query['proj']) {
                    case '56gene':
                        $table = '56gene_Lab';
                        break;

                    case 'BRCA':
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
                        if ($j == 0) {
                            $response['data'][$i][0] = getSDP('checkbox', $query['r_type'], $query['proj'], $row['SAP_id'], $row['RUN_bn']);
                            $response['data'][$i][1] = $i + 1;
                            $response['data'][$i][$j+2] = $row[$j];
                        }else {
                            $response['data'][$i][$j+2] = $row[$j];
                        }
                        $response['data'][$i][] = getSDP('anchor', $query['r_type'], $query['proj'], $row['SAP_id'], $row['RUN_bn']);
                    }
                }
                echo json_encode($response);
                break;
        }
        break;
}

function getSDP($col, $report_type, $proj, $sap_id, $run_bn) {
    $table = null;
    switch ($report_type) {
        case 'sequencing_data':
            $table = 'QC_SeqData';
            break;
    }
    $result = mysql_query("SELECT SDP, PASS FROM $table WHERE Project='$proj' AND SAP_id='$sap_id' AND RUN_bn='$run_bn'");
    if (!$result) {
        die('Query Error: '.mysql_error());
        return "Error";
    }else {
        $row_num = mysql_num_rows($result);
        switch ($col) {
            case 'checkbox':
                if ($row_num == 0) {
                    return "<input type=\"checkbox\" class=\"flat\" name=\"sdp\" value=0>";
                }else {
                    $sdp = mysql_fetch_array($result)[0];
                    return "<input type=\"checkbox\" class=\"flat\" name=\"sdp\" value=\"$sdp\">";
                }
                break;
            case 'anchor':
                if ($row_num == 0) {
                    return "暂无";
                }else {
                    $row = mysql_fetch_array($result);
                    $sdp = $row[0];
                    if ($row[1]) {
                        return "<span style=\"color: green;\"><strong> PASS </strong></span><a href=\"#\" onclick=\"loadReport_QC_SD('$sdp');return false;\">查看</a>";
                    }else {
                        return "<span style=\"color: red;\"><strong> FAILED </strong></span><a href=\"#\" onclick=\"loadReport_QC_SD('$sdp');return false;\">查看</a>";
                    }
                }
                break;
        }
    }
}
?>
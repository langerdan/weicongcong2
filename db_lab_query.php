<?php
require 'mysql_config.php';

$query = null;
switch ($_SERVER['REQUEST_METHOD']) {
    case 'GET':
        $query = $_GET;
        break;
    case 'POST':
        $query = $_POST;
        break;
}

$tb_content = "";
$bar = null;
$degree = null;
$state_desc = null;

$con = mysql_connect("localhost", $mysql_config['usr'], $mysql_config['pwd']);
if (!$con) {
    die('Could not connect MySQL: ' . mysql_error());
}
mysql_select_db("TopgenNGS", $con);

switch ($query['func']) {
    case 'lab_unhs':
        switch ($query['proj']) {
            case 'onco':
                $SAP_num = count(mysql_fetch_array(mysql_query("SELECT id FROM onco_Lab WHERE STATE='SAP'")));
                $EXTR_num = count(mysql_fetch_array(mysql_query("SELECT id FROM onco_Lab WHERE STATE='EXTR'")));
                $LIB_num = count(mysql_fetch_array(mysql_query("SELECT id FROM onco_Lab WHERE STATE='LIB'")));
                $RUN_num = count(mysql_fetch_array(mysql_query("SELECT id FROM onco_Lab WHERE STATE='RUN'")));
                $INIT_num = count(mysql_fetch_array(mysql_query("SELECT id FROM onco_Lab WHERE STATE='INIT'")));

                $result = mysql_query("SELECT id, SAP_id, STATE FROM onco_Lab WHERE STATE!='FINISH'") or die('Query Error: ' . mysql_error());
                $tb_content .= "<thead><tr><th>序号</th><th>样本名称</th><th>进度</th><th>说明</th><th>操作</th></tr></thead><tbody>";
                $index = 1;
                while($row = mysql_fetch_array($result)) {
                    changeProgState($row['STATE']);
                    $tb_content .= "<tr><td>".$index."</td><td>".$row['SAP_id']."</td><td >"."<div class=\"progress progress-striped\"><div class=\"progress-bar ".$bar."\" data-transitiongoal=\"".$degree."\" aria-valuenow=\"".$degree."\" style=\"width: ".$degree."%;\"></div></div></td><td>".$state_desc."</td><td><a href=\"#\" onclick=\"process('".$row['id']."');return false;\">跟进</a></td></tr>";
                    $index += 1;
                }
                $tb_content .= "</tbody>";
                $response = array(
                    'SAP_num' => $SAP_num,
                    'EXTR_num' => $EXTR_num,
                    'LIB_num' => $LIB_num,
                    'RUN_num' => $RUN_num,
                    'INIT_num' => $INIT_num,
                    'tbody' => $tb_content 
                );
                echo json_encode($response);
                break;
            
            case 'brac':

                break;
        }
        break;
    
    case 'lab_search':
        
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
 ?>
/**
 * PROGRAM  : QC_queryReport
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 25 2016
 * VERSION  : v0.0.1a
 */

function getSearchOptions () {
    var report_type = $("select[name='report_type']").children(':selected').val();

    switch (report_type) {
        case 'sequencing_data':
            document.getElementById('search_options').innerHTML = "<input type=\"radio\" name=\"search_type\" value=\"all\" checked> All&nbsp;&nbsp;<input type=\"radio\" name=\"search_type\" value=\"sample_id\"> 样本编号&nbsp;&nbsp;<input type=\"radio\" name=\"search_type\" value=\"sample_type\"> 样本类型&nbsp;&nbsp;<input type=\"radio\" name=\"search_type\" value=\"lib_reagent\"> 建库试剂&nbsp;&nbsp;<input type=\"radio\" name=\"search_type\" value=\"lib_id\"> 建库批次&nbsp;&nbsp;<input type=\"radio\" name=\"search_type\" value=\"run_id\"> 上机批次&nbsp;&nbsp;";

            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (xhttp.readyState == 4 && xhttp.status == 200) {
                    document.getElementById('report_container').innerHTML = xhttp.responseText;
                }
            };
            xhttp.open("GET", "./template/temp_qc_report_sequencing_data", true);
            xhttp.send();
            break;
    }
}

$('#search_go').click(function () {
    var project = $("select[name='project']").children(':selected').val();
    var report_type = $("select[name='report_type']").children(':selected').val();
    var search_term = $("input[name='search_term']").val();
    var search_options = $("input[name='search_options']:checked").val();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            document.getElementById('datatable-buttons').innerHTML = xhttp.responseText;
        }
    };
    xhttp.open("GET", "db_lab_query.php?f=qc&p=" + project + "&type=" + report_type + "&term=" + search_term + "&options=" + search_options, true);
    xhttp.send();
})

function generateReport(report_type) {
    switch (report_type) {
        case 'sequencing_data':
            
            break;
    }
}
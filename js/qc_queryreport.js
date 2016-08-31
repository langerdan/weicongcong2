/**
 * PROGRAM  : QC_queryReport
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 25 2016
 * VERSION  : v0.0.1a
 */

function showSearchOptions () {
    var report_type = $("select[name='report_type']").children(':selected').val();

    switch (report_type) {
        case 'sequencing_data':
            break;
    }
}

$('#search_go').click(function () {
    var project = $("select[name='project']").children(':selected').val();
    var report_type = $("select[name='report_type']").children(':selected').val();
    var search_options = $("input[name='search_options']:checked").val();
    var search_term = $("input[name='search_term']").val();

    if (report_type == 0) {
        new PNotify({
            title: '请选择报告类型',
            type: 'error',
            hide: false,
            styling: 'bootstrap3'
            });
    }else {
        if ($.fn.dataTable.isDataTable('#datatable_searchresults')) {
            dt_hs.destroy();
        }
        dt_hs = $("#datatable_searchresults").DataTable( {
            ajax: "db_report_query.php?func=search&r_type=" + report_type + "&proj=" + project + "&opt=" + search_options + "&term=" + search_term
        });
        
        var temp;
        switch (report_type) {
            case 'sequencing_data':
                temp = "./template/temp_qc_report_sequencing_data";
                break;
        }

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                document.getElementById('report_container').innerHTML = xhttp.responseText;
            }
        };
        xhttp.open("GET", temp, true);
        xhttp.send();
    }
})

function loadReport($report_type, $sdp) {
    switch ($report_type) {
        case 'sequencing_data':
            $.getScript('qc_report_sd.js');
            
            break;
    }
}


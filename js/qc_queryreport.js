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
        // draw datatable
        var report_name = "";
        switch (report_type) {
            case 'sequencing_data':
                report_name = "测序数据质量报告";
                break;
        }
        var export_filename_sr = project + "-" + report_name + "-检索结果";

        if ($.fn.dataTable.isDataTable('#datatable_searchresults')) {
            dt_sr.destroy();
        }
        dt_sr = $("#datatable_searchresults").DataTable( {
            ajax: "db_report_query.php?func=search&r_type=" + report_type + "&proj=" + project + "&opt=" + search_options + "&term=" + search_term,
            drawCallback: function(settings) {
                $("input[name='sdp']").iCheck({
                    checkboxClass: 'icheckbox_flat-green'
                });
                $(".bulk_action input#check-all").iCheck("uncheck");
                $("input[name='sdp']").on("ifChecked", function() {
                    $("#sample_comparision").show();
                });
                $("input[name='sdp']").on("ifUnchecked", function() {
                    if ($("input[name='sdp']:checked").length == 0) {
                        $("#sample_comparision").hide();
                    }
                });
            },
            order: [[6, 'des']],
            dom: "lfrtipB",
            buttons: [
                {
                    extend: "copy",
                    className: "btn-sm"
                },
                {
                    extend: "csv",
                    className: "btn-sm",
                    title: export_filename_sr
                },
                {
                    extend: "excel",
                    className: "btn-sm",
                    title: export_filename_sr
                },
                {
                    extend: "pdfHtml5",
                    className: "btn-sm",
                    title: export_filename_sr
                },
                {
                    extend: "print",
                    className: "btn-sm",
                    title: export_filename_sr
                    },
                ],
                responsive: true
        });
        
        // load template and js
        // add sample comparision func
        var template;
        switch (report_type) {
            case 'sequencing_data':
                template = "./template/temp_qc_report_sequencing_data";
                if (typeof loadReport_SD == "undefined") {
                    loadScript("./js/qc_report_sd.js");
                    $("#sample_comparision button").attr("onClick","compSap_QC_SD();");
                }
                break;
        }
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                document.getElementById('report_container').innerHTML = xhttp.responseText;
            }
        };
        xhttp.open("GET", template, true);
        xhttp.send();
    }
})

function loadScript(url, callback) {
    // Adding the script tag to the head as suggested before
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;

    // Then bind the event to the callback function.
    // There are several events for cross browser compatibility.
    script.onreadystatechange = callback;
    script.onload = callback;

    // Fire the loading
    head.appendChild(script);
}


/**
 * PROGRAM    : DB_queryLab
 * PURPOSE    :
 * AUTHOR     : codeunsolved@gmail.com
 * CREATED    : August 23 2016
 * VERSION    : v0.0.1a
 */

$(document).ready(function() {
loadunHandleSample('56gene');
});

function loadunHandleSample(project) {
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
  if (xhttp.readyState == 4 && xhttp.status == 200) {
    var json =  JSON.parse(xhttp.responseText);
    document.getElementById('SAP_num').innerHTML = json.SAP_num;
    document.getElementById('EXTR_num').innerHTML = json.EXTR_num;
    document.getElementById('LIB_num').innerHTML = json.LIB_num;
    document.getElementById('RUN_num').innerHTML = json.RUN_num;
    document.getElementById('INIT_num').innerHTML = json.INIT_num;
  }
};
xhttp.open("GET", "db_lab_query.php?func=lab_unhs_stat&proj=" + project, true);
xhttp.send();

if ($.fn.dataTable.isDataTable('#datatable_unHS')) {
    dt_hs.destroy();
}
dt_hs = $("#datatable_unHS").DataTable( {
  ajax: "db_lab_query.php?func=lab_unhs_tb&proj=" + project
});
}
      
$('#search_go').click(function () {
    var project = $("select[name='project']").children(':selected').val();
    var search_options = $("input[name='search_options']:checked").val();
    var search_term = $("input[name='search_term']").val();

    if ($.fn.dataTable.isDataTable('#datatable_searchresults')) {
        dt_sr.destroy();
    }
    dt_sr = $("#datatable_searchresults").DataTable({
        ajax: "db_lab_query.php?func=lab_search&proj=" + project + "&opt=" + search_options + "&term=" + search_term,
        dom: "lfrtipB",
        buttons: [
            {
                extend: "copy",
                className: "btn-sm"
            },
            {
                extend: "csv",
                className: "btn-sm"
            },
            {
                extend: "excel",
                className: "btn-sm"
            },
            {
                extend: "pdfHtml5",
                className: "btn-sm"
            },
            {
                extend: "print",
                className: "btn-sm"
                },
            ],
            responsive: true
    });
})
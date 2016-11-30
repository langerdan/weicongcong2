/**
 * PROGRAM : DB_Lab
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : August 23 2016
 * VERSION : v0.0.1a
 */

var dt = {};

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

	var export_filename = project + "_unhandled_samples";
	drawDataTable('#dt_unHS', export_filename, {
		ajax: "db_lab_query.php?func=lab_unhs_tb&proj=" + project
	});
}

$('#search_go').click(function () {
	var project = $("select[name='project']").children(':selected').val();
	var search_options = $("input[name='search_options']:checked").val();
	var search_term = $("input[name='search_term']").val();

	var export_filename = project + "-Lab";
	drawDataTable('#dt_searchresults', export_filename, {
		ajax: "db_lab_query.php?func=lab_search&proj=" + project + "&opt=" + search_options + "&term=" + search_term
	});
});

function drawDataTable(id, export_fn, options_add) {
	var options = {
		dom: "lfrtipB",
		buttons: [
			{
				extend: "copy",
				className: "btn-sm"
			},
			{
				extend: "csv",
				className: "btn-sm",
				title: export_fn
			},
			{
				extend: "excel",
				className: "btn-sm",
				title: export_fn
			},
			{
				extend: "pdfHtml5",
				className: "btn-sm",
				title: export_fn
			},
			{
				extend: "print",
				className: "btn-sm",
				title: export_fn
				}
			],
		responsive: true
	};
	for (var key in options_add) { options[key] = options_add[key]; }

	if ($.fn.dataTable.isDataTable(id)) {
		dt[id].destroy();
	}
	dt[id] = $(id).DataTable(options);
}
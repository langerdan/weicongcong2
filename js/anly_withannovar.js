/**
 * PROGRAM : anly_withAnnovar
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : November 10 2016
 * VERSION : v0.0.1a
 */

var dt = {};

$('#search_go').click(function () {
	var project = $("select[name='project']").children(':selected').val();
	var search_options = $("input[name='search_options']:checked").val();
	var search_term = $("input[name='search_term']").val();

	var export_filename_sr = project + "-VCF&注释－检索结果";
	drawDataTable('#dt_searchresults', export_filename_sr, {
		ajax: "anly_withAnnovar_query.php?proj=" + project + "&opt=" + search_options + "&term=" + search_term,
		drawCallback: function(settings) {
			$("input[name='sap_select']").iCheck({
				checkboxClass: 'icheckbox_flat-green'
			});
			$(".bulk_action input#check-all").iCheck("uncheck");
			$("input[name='sap_select']").on("ifChecked", function() {
				$("#sample_comparision").show();
			});
			$("input[name='sap_select']").on("ifUnchecked", function() {
				if ($("input[name='sap_select']:checked").length == 0) {
						$("#sample_comparision").hide();
				}
			});
		},
		order: [[1, 'des']]
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

function loadVCFandAnno(url, callback) {
	;
}
/**
 * PROGRAM : DB_queryTopAnno
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : September 18 2016
 * VERSION : v0.0.1a
 */

$('#search_go').click(function () {
	var project = $("select[name='project']").children(':selected').val();
	var search_options = $("input[name='search_options']:checked").val();
	var search_term = $("input[name='search_term']").val();
	// draw datatable
	var export_filename_sr = project + "-注释检索结果";

	if ($.fn.dataTable.isDataTable('#datatable_searchresults')) {
		dt_sr.destroy();
	}
	dt_sr = $("#datatable_searchresults").DataTable( {
		ajax: "db_topanno_query.php?proj=" + project + "&opt=" + search_options + "&term=" + search_term,
		order: [[5, 'des']],
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
				}
			],
			responsive: true
	});
});

function loadAnnoData(path) {
	var json = JSON.parse($.ajax({url: path, async: false}).responseText);
	anno_data = new Array();
	for (var i = 0; i < json.length; i++) {
		if (i == 0) {
			table_head = "<thead><tr>";
			for (var j = 0; j < json[0].length; j++) {
				table_head += "<th>" + json[0][j] + "</th>";
			}
			table_head += "</tr></thead>";
			$("#datatable_topanno").html(table_head);
		}else {
			anno_data.push(json[i]);
		}
	}
	// draw datatable
	var export_filename_ta = getBasename(getDirname(getDirname(path))) + "-" + getBasename(path) + "-Annotation";

	if ($.fn.dataTable.isDataTable('#datatable_topanno')) {
		dt_ta.destroy();
	}
	dt_ta = $("#datatable_topanno").DataTable( {
		data: anno_data,
		dom: "lfrtipB",
		buttons: [
			{
				extend: "copy",
				className: "btn-sm"
			},
			{
				extend: "csv",
				className: "btn-sm",
				title: export_filename_ta
			},
			{
				extend: "excel",
				className: "btn-sm",
				title: export_filename_ta
			},
			{
				extend: "pdfHtml5",
				className: "btn-sm",
				title: export_filename_ta
			},
			{
				extend: "print",
				className: "btn-sm",
				title: export_filename_ta
				}
			],
			responsive: true
	});
}

function getDirname(path) {
	 return path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '');
}

function getBasename(path) {
	 return path.replace(/\\/g,'/').replace( /.*\//, '' );
}
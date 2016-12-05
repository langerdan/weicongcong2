/**
 * PROGRAM : QC_report_SeqData
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : September 1 2016
 * VERSION : v0.0.1
 * UPDATE  : [v0.0.1] September 23 2016
 * (from Temp_QC_Report_Sequencing_Data)
 * 1. add <FASTQC>;
 * 2. add and adjust <report header>;
 * 3. adjust {<summary> => <coverage summary>};
 * 4. adjust [缺失片段] to <target base coverage>;
 * 5. add function drawDataTable();
 * 6. change font color to white when HeatColor is too red;
 * 7. add HeatColor to per_mapped_reads and per_target_reads;
 */

function loadReport_QC_SeqData(sdp) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var json = JSON.parse(xhttp.responseText);

			// sample name
			$('#sample_name').html(json.sample_name);
			// data version
			if (json.data_ver) {
				$('#data_ver').html(json.data_ver);
			}else {
				$('#data_ver').html("v0.0.1a?");
			}
			// bed filename
			if (json.bed_filename) {
				$('#bed_filename').html(json.bed_filename);
			}

			// pass details
			$('#pass_0x_percent').html(json.pass['0x_percent'] + '%');
			$('#pass_absent_frag').html(json.pass.absent_frag);
			$('#pass_coverage_unifor').html(json.pass.coverage_unifor + '%');
			$('#pass_min_reads').html(json.pass.min_reads);
			span_filed = '<span style="color: red;"><strong> FAILED </strong></span>';
			span_pass = '<span style="color: green;"><strong> PASS </strong></span>';
			if (json.pass['0x_percent'] > 1) {
				$('#pass_0x_percent_status').html(span_filed + '0x位点大于1%');
			}else {
				$('#pass_0x_percent_status').html(span_pass);
			}
			if (json.pass.absent_frag) {
				$('#pass_absent_frag_status').html(span_filed + '存在缺失片段');
			}else {
				$('#pass_absent_frag_status').html(span_pass);
			}
			if (json.pass.coverage_unifor < 98) {
				$('#pass_coverage_unifor_status').html(span_filed + '>0.2x小于98%');
			}else {
				$('#pass_coverage_unifor_status').html(span_pass);
			}
			if (json.pass.min_reads < 98) {
				$('#pass_min_reads_status').html(span_filed + 'reads覆盖度小于80');
			}else {
				$('#pass_min_reads_status').html(span_pass);
			}

			// 数据质量分析

			// 有效数据分析
			$('#total_reads').html(json.total_reads);
			$('#num_mapped_reads').html(json.mapped_reads);
			var percent_mapped = Math.floor((json.mapped_reads / json.total_reads) * 10000) / 100;
			$('#per_mapped_reads').html(percent_mapped + '%');
			$("#per_mapped_reads").css("background-color", getHeatColor(percent_mapped));
			if (percent_mapped <= 45) { $("#per_mapped_reads").css("color", "white"); }
			$('#num_target_reads').html(json.target_reads);
			var percent_target = Math.floor((json.target_reads / json.total_reads) * 10000) / 100;
			$('#per_target_reads').html(percent_target + '%');
			$("#per_target_reads").css("background-color", getHeatColor(percent_target));
			if (percent_target <= 45) { $("#per_target_reads").css("color", "white"); }

			$('#total_reads_pysam').html(json.total_reads_pysam);
			$('#num_mapped_reads_pysam').html(json.mapped_reads_pysam);
			var percent_mapped_pysam = Math.floor((json.mapped_reads_pysam / json.total_reads_pysam) * 10000) / 100;
			$('#per_mapped_reads_pysam').html(percent_mapped_pysam + '%');
			$("#per_mapped_reads_pysam").css("background-color", getHeatColor(percent_mapped_pysam));
			if (percent_mapped_pysam <= 45) { $("#per_mapped_reads_pysam").css("color", "white"); }
			$('#num_target_reads_pysam').html(json.target_reads_pysam);
			var percent_target_pysam = Math.floor((json.target_reads_pysam / json.total_reads_pysam) * 10000) / 100;
			$('#per_target_reads_pysam').html(percent_target_pysam + '%');
			$("#per_target_reads_pysam").css("background-color", getHeatColor(percent_target_pysam));
			if (percent_target_pysam <= 45) { $("#per_target_reads_pysam").css("color", "white"); }

			// Coverage Uniformity
			$('#total_reads_pysam_cu').html(json.total_reads_pysam);
			$('#max_reads_pysam').html(json.max_reads);
			$('#min_reads_pysam').html(json.min_reads);
			$('#mean_reads_pysam').html(json.mean_reads);
			$('#max_min_reads_pysam').html(json.min_reads ? Math.floor((json.target_reads_pysam / json.total_reads_pysam) * 10000) / 100 : 'N/A');
			$('#uniformity_0_2x').html(json.uniformity_0_2x);
			$("#uniformity_0_2x").css("background-color", getHeatColor(json.uniformity_0_2x));
			if (json.uniformity_0_2x <= 45) { $("#uniformity_0_2x").css("color", "white"); }
			$('#uniformity_0_5x').html(json.uniformity_0_5x);
			$("#uniformity_0_5x").css("background-color", getHeatColor(json.uniformity_0_5x));
			if (json.uniformity_0_5x <= 45) { $("#uniformity_0_5x").css("color", "white"); }
			// draw coverage uniformity graph
			if (Object.keys(json.frag_reads).length < 2000) {
				loadCoverUniforGraph(json.frag_reads);
			}else {
				$('#cu_container').attr("style", "display: none;");
			}

			// 目标区域覆盖度
			$('#max_sample_depth').html(json.max_depth);
			$('#min_sample_depth').html(json.min_depth);
			$('#mean_sample_depth').html(json.mean_depth);
			$('#num_target_bp').html(json.len_bp);
			$('#sample_depth_level').html(loadSampleDepthLevel(json.depth_levels));
			// draw datatable absent frag
			var exp_fn_abf = getBasename(getDirname(getDirname(getDirname(sdp)))) + "-(" + json.sample_name + ")-Absent_FRAG";
			var data_absent_frag = new Array();
			for (var i in json.absent_frag) {
				var row = new Array();
				row.push(json.absent_frag[i]);
				data_absent_frag.push(row);
			}
			drawDataTable('#dt_absent_frag', exp_fn_abf, {
				data: data_absent_frag
			});
			// draw datatable 0x frag
			var exp_fn_0xf = getBasename(getDirname(getDirname(getDirname(sdp)))) + "-(" + json.sample_name + ")-0xFRAG";
			drawDataTable('#dt_0x_frag', exp_fn_0xf, {
				data: get0xFrag(json, sdp),
				drawCallback: function(settings) {
					var td_obj = $("#dt_0x_frag td");
					for (var i = 0; i < td_obj.length; i++) {
						var cell = $("#dt_0x_frag td:eq(" + i + ")");
						var patt = /^[\d.]+%$/;
						if (patt.test(cell.text())) {
							var percent = cell.text().replace(/%/, "");
							if (percent >= 1) {
								cell.css("color", "red");
							}
						}
					}
				},
				order: [[1, 'des']]
			});

			// FASTQC
			if (json.fastqc.length > 0) {
				var fastqc_html_list = new Array();
				for (var i = 0; i < json.fastqc.length; i++) {
					fastqc_html_list.push([$.ajax({url: json.fastqc[i], async: false}).responseText, json.fastqc[i]]);
				}
				var export_fn_fqc = getBasename(getDirname(getDirname(getDirname(sdp)))) + "-(" + json.sample_name + ")-FASTQC_Summary";
				drawDataTable('#dt_fastqc_basic', export_fn_fqc, {
					data: getFastqcBasic(fastqc_html_list)
				});
				// extract FASTQC img
				extractFastacImg('1', fastqc_html_list[0][0]);
				extractFastacImg('2', fastqc_html_list[1][0]);
			}

			// 片段碱基覆盖度
			$('#dt_frag_depth_level').html(loadFragCoverTable(json.depth_levels));
			if (Object.keys(json.frag_reads).length < 2000) {
				// draw datatable frag depth level
				var export_fn_fc = getBasename(getDirname(getDirname(getDirname(sdp)))) + "-" + json.sample_name + "-FRAG_COVER";
				drawDataTable('#dt_frag_depth_level', export_fn_fc, {
					data: getFragDepthLevel(json.frag_cover_list, sdp),
					drawCallback: function(settings) {
						var td_obj = $("#dt_frag_depth_level td");
						for (var i = 0; i < td_obj.length; i++) {
							var cell = $("#dt_frag_depth_level td:eq(" + i + ")");
							var patt = /^[\d.]+%$/;
							if (patt.test(cell.text())) {
								var percent = cell.text().replace(/%/, "");
								cell.css("background-color", getHeatColor(percent));
								if (percent <= 45) { cell.css("color", "white"); }
							}
						}
					}
				});
			}
		}
	};
	xhttp.open("GET", sdp, true);
	xhttp.send();
}

function loadCoverUniforGraph(reads) {
	var keys = Object.keys(reads).sort();
	var values = new Array();
	for (var i = 0; i < keys.length; i++) {
		values.push(reads[keys[i]]);
	}
	var graph_data = {
		labels: keys,
		datasets: [
			{
				label: "Coverage Overview",
				backgroundColor: "rgba(47,69,84,1)",
				data: values
			}
		]
	};
	var graph_options = {
		responsive: true,
		maintainAspectRatio: false,
	};

	drawGraph('coverage_uniformity_graph', graph_data, graph_options);
}

function drawGraph(graph_id, graph_data, graph_options) {
	var ctx = document.getElementById(graph_id).getContext("2d");

	if(window.barChart !== undefined && window.barChart !== null){
		window.barChart.destroy();
	}

	window.barChart = new Chart(ctx, {
		type: 'bar',
		data: graph_data,
		options: graph_options
	});
}

function loadSampleDepthLevel(data) {
	var table_body = "";
	for (var i in data) {
		if (i == 0) {
			table_body += "<thead><tr>";
			for (var m in data) {
				if (data[m][0] == 0) {
					table_body += "<th> >" + data[m][0] + " </th>";
				}else {
					table_body += "<th> ≥" + data[m][0] + " </th>";
				}
			}
			table_body += "</tr></thead><tbody><tr>";
		}
		var percent = data[i][1]
		if (percent > 45 ) {
			table_body += "<td style=\"background-color: " + getHeatColor(percent) + ";\"> " + percent + "% </td>";
		}else {
			table_body += "<td style=\"background-color: " + getHeatColor(percent) + "; color: white\"> " + percent + "% </td>";
		}

	}
	table_body += "</tr></tbody>";
	return table_body;
}

function getFastqcBasic(fqc_html_l) {
	var data_fastqc_basic = new Array();
	for (var i = 0; i < fqc_html_l.length; i++) {
		var row = new Array();

		var fastqc_html = $('<div></div>');
		fastqc_html.html(fqc_html_l[i][0]);
		var tb_obj =  $("table:eq(0) td", fastqc_html);
		for (var j = 0; j < tb_obj.length; j++) {
			if (j%2 == 1) {
				row.push($("table:eq(0) td:eq(" + j + ")", fastqc_html).text());
			}
		}
		row.push("<a href=\"" + fqc_html_l[i][1] + "\" target=\"_blank\">查看报告</a>");
		data_fastqc_basic.push(row);
	}
	return data_fastqc_basic;
}

function extractFastacImg(n, fqc_html) {
	var fastqc_html = $('<div></div>');
	fastqc_html.html(fqc_html);
	$("#r" + n + "_q_dist").attr("src", $("#M1", fastqc_html).next().children("img").attr("src"));
	$("#r" + n + "_len_dist").attr("src", $("#M7", fastqc_html).next().children("img").attr("src"));
}

function get0xFrag(json, sdp){
	var frag_0x = json["0x_frag"];
	var data = new Array();
	var frag_0x_sorted = Object.keys(frag_0x).map(function(key) {
		return [key, frag_0x[key]];
	});
	frag_0x_sorted.sort(function(first, second) {
		return second[1] - first[1];
	});
	for (var i in frag_0x_sorted) {
		var row = new Array();
		row.push("<a href=\"#\" onclick=\"openFragBaseCoverGraph('" + getFragJsonURL(sdp, frag_0x_sorted[i][0]) + "');return false;\">" + frag_0x_sorted[i][0] + "</a>");
		row.push(frag_0x_sorted[i][1] + "%");
		data.push(row);
	}
	return data;
}

function getFragDepthLevel(frag_cl, sdp) {
	var data = new Array();
	for (var i in frag_cl) {
		var row = new Array();
		for (var j in frag_cl[i].depth_levels) {
			if (j == 0) {
				row.push("<a href=\"#\" onclick=\"openFragBaseCoverGraph('" + getFragJsonURL(sdp, frag_cl[i].frag_name) + "');return false;\">" + frag_cl[i].frag_name + "</a>");
			}
			row.push(frag_cl[i].depth_levels[j][1] + "%");
		}
		data.push(row);
	}
	return data;
}

function getFragJsonURL(sdp, frag_name) {
	return getDirname(sdp) + "/" + frag_name + ".json";
}

function getHeatColor(percent) {
	var h= percent / 100 * 90 / 360;
	var s = 0.9;
	var l = 0.5;
	var rgb = HSLtoRGB(h, s, l);
	return RGBToHex(rgb.r, rgb.g, rgb.b);
}

function HSLtoRGB(h, s, l){
	var r, g, b;

	if(s == 0){
		r = g = b = l; // achromatic
	}else{
		var hue2rgb = function hue2rgb(p, q, t){
			if(t < 0) t += 1;
			if(t > 1) t -= 1;
			if(t < 1/6) return p + (q - p) * 6 * t;
			if(t < 1/2) return q;
			if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
			return p;
		};
		var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
		var p = 2 * l - q;
		r = hue2rgb(p, q, h + 1/3);
		g = hue2rgb(p, q, h);
		b = hue2rgb(p, q, h - 1/3);
	}
	return {
		r: Math.round(r * 255),
		g: Math.round(g * 255),
		b: Math.round(b * 255)
	};
}

function RGBToHex(r, g, b) {
	function componentToHex(c) {
		var hex = c.toString(16);
		return hex.length == 1 ? "0" + hex : hex;
	}
	return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function getDirname(path) {
	return path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '');
}

function getBasename(path) {
	return path.replace(/\\/g,'/').replace( /.*\//, '' );
}

function loadFragCoverTable(data) {
	table_head = "<thead><tr><th>Fragment Name</th>";
	for (var i in data) {
		if (data[i][0] == 0) {
			table_head += "<th> >" + data[i][0] + " </th>";
		}else {
			table_head += "<th> ≥" + data[i][0] + " </th>";
		}
	}
	table_head += "</tr></thead>";
	return table_head;
}

function openFragBaseCoverGraph(frag_d_url) {
	if ((typeof frag_d_url=='string')&&frag_d_url.constructor==String) {
		window.open("frag_base_cover_graph.php?u0=" + frag_d_url);
	}else if ((typeof frag_d_url=='object')&&frag_d_url.constructor==Array) {
		var param = "";
		for (var i = 0; i < frag_d_url.length; i++) {
			if (i == 0)  {
				param += "u" + i + "=" + frag_d_url[i];
			}else {
				param += "&u" + i + "=" + frag_d_url[i];
			}
		}
		window.open("frag_base_cover_graph.php?"+ param);
	}
}

function compareSap_QC_SeqData() {
	var input_sdp_obj = $("input[name='sap_select']:checked");
	var param = "";
	for (var i = 0; i < input_sdp_obj.length; i++) {
		var sdp = $("input[name='sap_select']:checked:eq(" + i + ")");
		if (sdp.val() != 0) {
			if (param == "") {
				param += "u" + i + "=" + sdp.val();
			}else {
				param += "&u" + i + "=" + sdp.val();
			}
		}
	}
	if (param == "") {
		new PNotify({
			title: '所选样本没有相关数据',
			type: 'error',
			hide: false,
			styling: 'bootstrap3'
			});
	}else {
		window.open("qc_compare_sap_seqdata.php?"+ param);
	}
}


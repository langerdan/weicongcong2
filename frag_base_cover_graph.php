<!DOCTYPE html>
<!--
 * PAGE	   : frag_base_cover_graph
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : September 3 2016
 * VERSION : v0.0.1a
-->
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<!-- Meta, title, CSS, favicons, etc. -->
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<title>片段碱基覆盖图</title>

		<!-- Bootstrap -->
		<link href="./vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
		<!-- Font Awesome -->
		<link href="./vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
		<!-- Datatables -->
		<link href="./vendors/datatables.net-bs/css/dataTables.bootstrap.min.css" rel="stylesheet">
		<link href="./vendors/datatables.net-buttons-bs/css/buttons.bootstrap.min.css" rel="stylesheet">

		<!-- Custom Theme Style -->
		<link href="./build/css/custom.min.css" rel="stylesheet">
	</head>
	<body class="nav-md">
		<div class="row">
			<div class="col-md-12 col-sm-12 col-xs-12">
				<div>
					<ul id="frag_data_url" style="display: none;">
						<?php
							$query = null;

							switch ($_SERVER['REQUEST_METHOD']) {
									case 'GET':
											$query = $_GET;
											break;
									case 'POST':
											$query = $_POST;
											break;
							}

							foreach ($query as $key => $value) {
								echo "<li>".$value."</li>";
							}
						?>
					</ul>
				</div>

				<div class="x_panel">
					<div class="x_title">
						<h2>片段碱基覆盖图</h2>
						<div class="clearfix"></div>
					</div>
					<div class="x_content">
						<div class="row">
							<div class="col-md-12 col-sm-12 col-xs-12">
								<div class="x_panel">
									<div class="x_content">
										<table id="datatable_frag_info" class="table table-striped table-bordered jambo_table">
											<thead>
												<tr>
													<th>序号</th>
													<th>样本编号</th>
													<th>片段名称</th>
													<th>染色体</th>
													<th>基因名称</th>
													<th>位置</th>
													<th>长度</th>
													<th>平均深度</th>
													<th>最大深度</th>
													<th>最小深度</th>
												</tr>
											</thead>
										</table>
									</div>
								</div>
							</div>
						</div>

						<div class="row">
							<div class="col-md-12 col-sm-12 col-xs-12">
								<div class="x_panel">
									<div class="x_content" style="width: 100%; height: 711px;">
										<canvas id="frag_base_cover_graph"></canvas>
									</div>
								</div>
							</div>
						</div> 
					</div>
				</div>
			</div>
		</div>

		<!-- jQuery -->
		<script src="./vendors/jquery/dist/jquery.min.js"></script>
		<!-- Bootstrap -->
		<script src="./vendors/bootstrap/dist/js/bootstrap.min.js"></script>
		<!-- Datatables -->
		<script src="./vendors/datatables.net/js/jquery.dataTables.min.js"></script>
		<script src="./vendors/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>
		<script src="./vendors/datatables.net-buttons/js/dataTables.buttons.min.js"></script>
		<script src="./vendors/datatables.net-buttons-bs/js/buttons.bootstrap.min.js"></script>
		<script src="./vendors/datatables.net-buttons/js/buttons.flash.min.js"></script>
		<script src="./vendors/datatables.net-buttons/js/buttons.html5.min.js"></script>
		<script src="./vendors/datatables.net-buttons/js/buttons.print.min.js"></script>
		<script src="./vendors/jszip/dist/jszip.min.js"></script>
		<script src="./vendors/pdfmake/build/pdfmake.min.js"></script>
		<script src="./vendors/pdfmake/build/vfs_fonts.js"></script>
		<!-- Chart.js -->
		<script src="./vendors/Chart.js/dist/Chart.min.js"></script>

		<!-- Custom Theme Scripts -->
		<script src="./build/js/custom.min-qc_report.js"></script>

		<script type="text/javascript">
			var color_sheet = new Array();
			var frag_data_url = $("#frag_data_url li");
			var frag_data = new Array();
			for (var i = 0; i < frag_data_url.length; i ++) {
				var url = $("#frag_data_url li:eq(" + i + ")").text();
				var json = JSON.parse($.ajax({url: url,async: false}).responseText);
				frag_data.push(json);
				color_sheet.push(dynamicColors());
			}

			if ($.fn.dataTable.isDataTable('#datatable_frag_info')) {
					dt_fi.destroy();
			}
			dt_fi = $("#datatable_frag_info").DataTable( {
					data: getFragInfo(frag_data)
			});

			loadFragCoverGraph(frag_data);

			function dynamicColors() {
					var r = Math.floor(Math.random() * 255);
					var g = Math.floor(Math.random() * 255);
					var b = Math.floor(Math.random() * 255);
					return {"r": r, "g": g, "b": b};
			}

			function getFragInfo(json_list) {
				var data = new Array();
				for (var i =0; i < json_list.length; i ++) {
					var row = new Array();
					row.push(i + 1);
					row.push(json_list[i].sample_name);
					row.push(json_list[i].frag_name);
					row.push("Chr " + json_list[i].chr_num);
					row.push(json_list[i].gene_name);
					row.push(json_list[i].pos_s + " - " + json_list[i].pos_e);
					row.push(json_list[i].len);
					row.push(json_list[i].mean_depth);
					row.push(json_list[i].max_depth);
					row.push(json_list[i].min_depth);
					data.push(row);
				}
				return data;
			}

			function loadFragCoverGraph(json_list) {
				var x_labels;
				var graph_data = new Array();
				var graph_options = {
					responsive: true,
					maintainAspectRatio: false,
				};
				var x_labels_max_len = 0;

				for (var i = 0; i < json_list.length; i ++) {
					if (i == 0){
						x_labels = json_list[i].x_labels;
					}else {
						if (json_list[i].frag_name != json_list[i-1].frag_name) {
							if (json_list[i].x_labels.length > json_list[i-1].x_labels.length) {
								x_labels_max_len = json_list[i].x_labels.length;
							}else {
								x_labels_max_len = json_list[i-1].x_labels.length;
							}
						}
					}
					graph_data.push({
						label: json_list[i].frag_name,
						fill: false,
						lineTension: 0.05,
						backgroundColor: "rgba(" + color_sheet[i].r + "," + color_sheet[i].g + "," + color_sheet[i].b + ",0.4)",
						borderColor: "rgba(" + color_sheet[i].r + "," + color_sheet[i].g + "," + color_sheet[i].b + ",1)",
						borderCapStyle: 'butt',
						borderDash: [],
						borderDashOffset: 0.0,
						borderJoinStyle: 'miter',
						pointBorderColor: "rgba(" + color_sheet[i].r + "," + color_sheet[i].g + "," + color_sheet[i].b + ",1)",
						pointBackgroundColor: "#fff",
						//pointBorderWidth: 1,
						//pointHoverRadius: 5,
						pointHoverBackgroundColor: "rgba(" + color_sheet[i].r + "," + color_sheet[i].g + "," + color_sheet[i].b + ",1)",
						pointHoverBorderColor: "rgba(" + color_sheet[i].r + "," + color_sheet[i].g + "," + color_sheet[i].b + ",1)",
						//pointHoverBorderWidth: 2,
						pointRadius: 1,
						//pointHitRadius: 10,
						data: json_list[i].depths,
						spanGaps: false
					});
				}
				if (x_labels_max_len) {
					x_labels = new Array();
					for (var j =0; j < x_labels_max_len; j ++) {
						x_labels.push(j + 1);
					}
				}
				drawGraph("frag_base_cover_graph", {labels: x_labels, datasets: graph_data}, graph_options);
			}

			function drawGraph(graph_id, graph_data, graph_options) {
				var ctx = document.getElementById(graph_id).getContext("2d");

				if(window.lineChart !== undefined && window.lineChart !== null){
					window.lineChart.destroy();
				}

				window.lineChart = new Chart(ctx, {
					type: 'line',
					data: graph_data,
					options: graph_options
				});
			}
		</script>
	</body>
</html>
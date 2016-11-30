<!DOCTYPE html>
<!--
 * PAGE    : db_HaploX_targeted_drugs
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : November 30 2016
 * VERSION : v0.0.1a
-->
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<!-- Meta, title, CSS, favicons, etc. -->
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<title>数据库 - HaploX 靶向药 3.0</title>

		<!-- Bootstrap -->
		<link href="./vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
		<!-- Font Awesome -->
		<link href="./vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
		<!-- iCheck -->
		<link href="./vendors/iCheck/skins/flat/green.css" rel="stylesheet">
		<!-- bootstrap-progressbar -->
		<link href="./vendors/bootstrap-progressbar/css/bootstrap-progressbar-3.3.4.min.css" rel="stylesheet">
		<!-- Datatables -->
		<link href="./vendors/datatables.net-bs/css/dataTables.bootstrap.min.css" rel="stylesheet">
		<link href="./vendors/datatables.net-buttons-bs/css/buttons.bootstrap.min.css" rel="stylesheet">

		<!-- Custom Theme Style -->
		<link href="./build/css/custom.min.css" rel="stylesheet">
	</head>
	<body class="nav-md">
		<div class="container body">
			<div class="main_container">

				<!-- left navigation -->
				<?php include 'frame_leftNav.php';?>
				<!-- /left navigation -->

				<!-- top navigation -->
				<?php include 'frame_topNav.php';?>
				<!-- /top navigation -->

				<!-- page content -->
				<div class="right_col" role="main">
					<div class="page-title">
						<div class="title_left">
							<h2> HaploX 靶向药 3.0 <small> </small></h2>
						</div>
						<div class="title_right"></div>
					</div>
					<div class="clearfix"></div>
					<div>
						<p>1.本列表由海普洛斯HaploX整理自FDA网站</p>
						<p>2.为求简洁，本列表中多处使用简写，如：以m代表metastatic，以NSCLC代表非小细胞肺癌，以CML代表慢性粒细胞白血病，以ALL代表急性淋巴细胞白血病等</p>
						<p>3.对于在中国已上市的靶向药物，使用了<strong style="color: green;">绿色</strong>作为字体颜色</p>
					</div>
					<!-- search database -->
					<div class="row" >
						<div class="col-md-12 col-sm-12 col-xs-12">
							<div class="x_panel">
								<div class="x_title">
									<h2>检索</h2>
									<div class="clearfix"></div>
								</div>
								<div class="x_content">
									<div class="row form-group">
										<div class="col-md-12 col-sm-12 col-xs-12 top_search">
											<div class="input-group" style="width:69%; margin-left: 10px">
												<input type="text" name="search_term" class="form-control" placeholder="Search ...">
												<span class="input-group-btn">
													<button id="search_go" class="btn btn-primary" type="button" style="color: white"> Go! </button>
												</span>
											</div>
										</div>

										<div class="col-md-9 col-sm-9 col-xs-9">
											<input type="radio" class="flat" name="search_options" value="all" checked> 全部&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="target"> 作用靶点&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="disease"> 疾病&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="on_CHINA_market"> 中国已上市&nbsp;&nbsp;
										</div>
									</div>

									<div class="divider-dashed"></div>

									<div class="row">
										<div class="col-md-12 col-sm-12 col-xs-12">
											<div class="x_panel">
												<div class="x_title">
													<h2>检索结果</h2>
													<div class="clearfix"></div>
												</div>
												<div class="x_content">
													<table id="dt_searchresults" class="table table-striped table-bordered jambo_table">
														<thead>
															<tr class="headings">
																<th class="column-title">No.</th>
																<th class="column-title">通用名</th>
																<th class="column-title">商品名</th>
																<th class="column-title">作用靶点</th>
																<th class="column-title">疾病</th>
																<th class="column-title">应用条件</th>
																<th class="column-title">作用机制</th>
																<th class="column-title">FDA最新说明书</th>
																<th class="column-title">备注</th>
																<th class="column-title">研发代码</th>
																<th class="column-title">上市时间</th>
																<th class="column-title">原研商</th>
																<th class="column-title">药物类型</th>
																<th class="column-title" style="display: none">on_CHINA_market</th>
															</tr>
														</thead>
													</table>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<!-- /search database -->
				</div>
				<!-- /page content -->

				<!-- footer content -->
				<?php include 'frame_footer.php';?>
				<!-- /footer content -->
			</div>
		</div>

		<!-- jQuery -->
		<script src="./vendors/jquery/dist/jquery.min.js"></script>
		<!-- Bootstrap -->
		<script src="./vendors/bootstrap/dist/js/bootstrap.min.js"></script>
		<!-- iCheck -->
		<script src="./vendors/iCheck/icheck.min.js"></script>
		<!-- bootstrap-progressbar -->
		<script src="./vendors/bootstrap-progressbar/bootstrap-progressbar.min.js"></script>
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

		<!-- Custom Theme Scripts -->
		<script src="./build/js/custom.min.js"></script>

		<!-- db HaploX targeted drugs Scripts -->
		<script type="text/javascript">
			var dt = {};

			$('#search_go').click(function () {
				var search_options = $("input[name='search_options']:checked").val();
				var search_term = $("input[name='search_term']").val();

				var export_filename = "HaploX_targeted_drugs-SearchResults";
				drawDataTable('#dt_searchresults', export_filename, {
					ajax: "db_HaploX_targeted_drugs_query?func=search&opt=" + search_options + "&term=" + search_term,
					"rowCallback": function(row, data, index) {
						var last_i = data.length-1;
						if ( data[last_i] == 1 ) {
							$(row).attr("style", "color: green;");
						}
						$('td:eq(' + last_i + ')', row).attr("style", "display: none; font-weight: bold");
						$('td:eq(7)', row).html("<a href=\"" + data[7] + "\">" + data[7] + "</a>");
					}
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
		</script>
	</body>
</html>
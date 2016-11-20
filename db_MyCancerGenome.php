<!DOCTYPE html>
<!--
 * PAGE    : db_MyCancerGenome
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : November 16 2016
 * VERSION : v0.0.1a
-->
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<!-- Meta, title, CSS, favicons, etc. -->
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<title>数据库 - MyCancerGenome</title>

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

		<style type="text/css">
			.badge {
				background-color: transparent;
			}
		</style>
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
							<h2> MyCancerGenome <small> </small></h2>
						</div>
						<div class="title_right"></div>
					</div>
					<div class="clearfix"></div>

					<!-- search MyCancerGenome database -->
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
											<input type="radio" class="flat" name="search_options" value="all" checked> All&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="disease"> Disease&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="gene"> Gene&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="variant"> Variant&nbsp;&nbsp;
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
																<th class="column-title">Disease</th>
																<th class="column-title">Gene</th>
																<th class="column-title">Variant</th>
																<th class="column-title">Info</th>
																<th class="column-title">Last update</th>
																<th class="column-title">Details</th>
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
					<!-- /search MyCancerGenome database -->

					<!-- variant details -->
					<div class="row">
						<div class="col-md-12 col-sm-12 col-xs-12">
							<div class="x_panel">
								<div id="variant_details" class="x_content">
								</div>
							</div>
						</div>
					</div>
					<!-- /variant details -->
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

		<!-- db MyCancerGenome Scripts -->
		<script type="text/javascript">
			var dt = {};

			$('#search_go').click(function () {
				var search_options = $("input[name='search_options']:checked").val();
				var search_term = $("input[name='search_term']").val();

				var export_filename = "MyCancerGenome-SearchResults";
				drawDataTable('#dt_searchresults', export_filename, {
					ajax: "db_MyCancerGenome_query.php?func=search&opt=" + search_options + "&term=" + search_term
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

			function loadVariantDetails(url) {
				$('#variant_details').html($.ajax({url: "db_MyCancerGenome_query.php?func=details&url=" + url, async: false}).responseText);
			}
		</script>
	</body>
</html>
<!DOCTYPE html>
<!--
 * PAGE    : db_clinvar
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : September 6 2016
 * VERSION : v0.0.1a
-->
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<!-- Meta, title, CSS, favicons, etc. -->
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<title>数据库 - NGS Lab</title>

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
							<h2>Clinvar <small> </small></h2>
						</div>
						<div class="title_right"></div>
					</div>
					<div class="clearfix"></div>

					<!-- search clinvar database -->
					<div class="row" >
						<div class="col-md-12 col-sm-12 col-xs-12">
							<div class="x_panel">
								<div class="x_title">
									<h2>检索Clinvar</h2>
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

										<div class="col-md-3 col-sm-3 col-xs-3">
											<select name="build" class="form-control">
												<option value="hg19_20140929" selected> hg19_20140929 </option>
												<option value="hg19_20160302"> hg19_20160302 </option>
											</select>
										</div>
										<div id="search_options" class="col-md-9 col-sm-9 col-xs-9">
											<input type="radio" class="flat" name="search_options" value="all" checked> All&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="chr"> Chr&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="start"> Start&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="end"> End&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="ref"> Ref&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="alt"> Alt&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="CLINSIG"> CLINSIG&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="CLNDBN"> CLNDBN&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="CLNACC"> CLNACC&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="CLNDSDB"> CLNDSDB&nbsp;&nbsp;
											<input type="radio" class="flat" name="search_options" value="CLNDSDBID"> CLNDSDBID&nbsp;&nbsp;
										</div>
									</div>

									<div class="divider-dashed"></div>

									<div class="row">
										<div class="col-md-12 col-sm-12 col-xs-12">
											<div class="x_panel">
												<div class="x_title">
													<h2>搜索结果</h2>
													<div class="clearfix"></div>
												</div>
												<div class="x_content">
													<table id="datatable_searchresults" class="table table-striped table-bordered jambo_table">
														<thead>
															<tr class="headings">
																<th class="column-title">No.</th>
																<th class="column-title">Chr</th>
																<th class="column-title">Start</th>
																<th class="column-title">End</th>
																<th class="column-title">Ref</th>
																<th class="column-title">Alt</th>
																<th class="column-title">CLINSIG</th>
																<th class="column-title">CLNDBN</th>
																<th class="column-title">CLNACC</th>
																<th class="column-title">CLNDSDB</th>
																<th class="column-title">CLNDSDBID</th>
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
					<!-- /search clinvar database -->

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

		<!-- Sample Coverage Scripts -->
		<script src="js/db_queryclinvar.js"></script>

	</body>
</html>
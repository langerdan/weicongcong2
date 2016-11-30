<!DOCTYPE html>
<!--
 * PAGE    : anly_withAnnovar
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : October 31 2016
 * VERSION : v0.0.1a
-->
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<!-- Meta, title, CSS, favicons, etc. -->
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<title>分析 － withAnnovar</title>

		<!-- Bootstrap -->
		<link href="./vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
		<!-- Font Awesome -->
		<link href="./vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
		<!-- iCheck -->
		<link href="./vendors/iCheck/skins/flat/green.css" rel="stylesheet">
		<!-- PNotify -->
		<link href="./vendors/pnotify/dist/pnotify.css" rel="stylesheet">
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
					<!-- tab nav -->
					<ul class="nav nav-tabs">
						<li class="active"><a data-toggle="tab" href="#tb_search">检索</a></li>
						<li><a data-toggle="tab" href="#tb_filter">过滤</a></li>
						<li><a data-toggle="tab" href="#tb_sort">排序</a></li>
						<li><a data-toggle="tab" href="#tb_compare">样本比较</a></li>
					</ul>
					<!-- /tab nav -->

					<!-- tab content -->
					<div class="tab-content">
						<!-- search -->
						<div id="tb_search" class="tab-pane fade in active">
							<div class="row" >
								<div class="col-md-12 col-sm-12 col-xs-12">
									<div class="x_panel">
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

												<div class="col-md-2 col-sm-2 col-xs-2">
													<select name="project" class="form-control">
														<option value="56gene" selected> 56gene </option>
														<option value="brca"> BRCA </option>
													</select>
												</div>
												<div class="col-md-10 col-sm-10 col-xs-10">
													<input type="radio" class="flat" name="search_options" value="all"> All&nbsp;&nbsp;
													<input type="radio" class="flat" name="search_options" value="sample_id"> 样本编号&nbsp;&nbsp;
													<input type="radio" class="flat" name="search_options" value="sample_type"> 样本类型&nbsp;&nbsp;
													<input type="radio" class="flat" name="search_options" value="run_bn" checked> 上机批次&nbsp;&nbsp;
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
															<table id="dt_searchresults" class="table table-striped table-bordered jambo_table bulk_action">
																<thead>
																	<tr class="headings">
																		<th>
																			<input type="checkbox" id="check-all" class="flat">
																		</th>
																		<th class="column-title">序号</th>
																		<th class="column-title">样本编号</th>
																		<th class="column-title">样本类型</th>
																		<th class="column-title">上机批次</th>
																		<th class="column-title">Pipeline</th>
																		<th class="column-title">VCF</th>
																		<th class="column-title">注释</th>
																		<th class="bulk-actions" colspan="7">
																			<a class="antoo" style="color:#fff; font-weight:500;">样本比较 ( <span class="action-cnt"> </span> ) <i class="fa fa-chevron-down"></i></a>
																		</th>
																	</tr>
																</thead>
															</table>
														</div>
														<div id="sample_comparision" style="display: none;"><button class="btn btn-success" onClick="compareSample();"><i class="fa fa-bar-chart"></i> 多样本比较 </button></div>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>

							<!-- VCF&Annotaion outputs -->
							<div class="row">
								<div class="col-md-12 col-sm-12 col-xs-12">
									<div class="x_panel">
										<div class="x_title">
											<h2>VCF/注释</h2>
											<div class="clearfix"></div>
										</div>
										<div class="x_content">
											<table id="dt_vcf_anno" class="table table-striped table-bordered jambo_table">
											</table>
										</div>
									</div>
								</div>
							</div>
							<!-- /VCF&Annotaion outputs -->
						</div>
						<!-- /search -->

						<!-- filter -->
						<div id="tb_filter" class="tab-pane fade">
							<div class="row" >
								<div class="col-md-12 col-sm-12 col-xs-12">
									<div class="x_panel">
										<div class="x_content">
											<div class="row">
												<div class="col-md-12 col-sm-12 col-xs-12">
													<div class="x_panel">
														<div class="x_title">
															<h2>数据选择</h2>
															<div class="clearfix"></div>
														</div>
														<div class="x_content">
															<table id="dt_dataselect_filter" class="table table-striped table-bordered jambo_table">
																<thead>
																	<tr>
																		<th class="column-title">序号</th>
																		<th class="column-title">数据名称</th>
																		<th class="column-title">创建时间</th>
																		<th class="column-title">修改时间</th>
																		<th class="column-title">大小</th>
																		<th class="column-title">用户</th>
																	</tr>
																</thead>
															</table>
														</div>
														<div id="sample_comparision" style="display: none;"><button class="btn btn-success" onClick="compareSample();"><i class="fa fa-bar-chart"></i> 多样本比较 </button></div>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						<!-- /filter -->

						<!-- sort -->
						<div id="tb_sort" class="tab-pane fade">

						</div>
						<!-- /sort -->

						<!-- compare -->
						<div id="tb_compare" class="tab-pane fade">
							<div class="row" >
								<div class="col-md-12 col-sm-12 col-xs-12">
									<div class="x_panel">
										<div class="x_content">
											<div class="row">
												<div class="col-md-12 col-sm-12 col-xs-12">
													<div class="x_panel">
														<div class="x_title">
															<h2>数据选择</h2>
															<div class="clearfix"></div>
														</div>
														<div class="x_content">
															<table id="dt_dataselect_filter" class="table table-striped table-bordered jambo_table">
																<thead>
																	<tr>
																		<th class="column-title">序号</th>
																		<th class="column-title">数据名称</th>
																		<th class="column-title">创建时间</th>
																		<th class="column-title">修改时间</th>
																		<th class="column-title">大小</th>
																		<th class="column-title">用户</th>
																	</tr>
																</thead>
															</table>
														</div>
														<div id="sample_comparision" style="display: none;"><button class="btn btn-success" onClick="compareSample();"><i class="fa fa-bar-chart"></i> 多样本比较 </button></div>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						<!-- /compare -->
					</div>
					<!-- /tab content -->
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
		<!-- PNotify -->
		<script src="./vendors/pnotify/dist/pnotify.js"></script>
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
		<script src="./build/js/custom.min_sapselect.js"></script>

		<!-- anly withAnnovar js -->
		<script src="./js/anly_withannovar.js"></script>
	</body>
</html>

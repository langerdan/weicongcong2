<!DOCTYPE html>
<!-- 
 * PAGE    : index
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : August 10 2016
 * VERSION : v0.0.1a
-->
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<!-- Meta, title, CSS, favicons, etc. -->
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<title>Topgen Dashboard</title>

		<!-- Bootstrap -->
		<link href="./vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
		<!-- Font Awesome -->
		<link href="./vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">

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
					<h4>目前开放页面：</h4>
					<ul>
						<li>
							<h3>质量控制</h3>
							<ul>
								<li>
									<h4>质控报告（<strong style="color: green;">推荐</strong>）</h4>
									<p>通过相关数据库交叉检索报告，提示报告PASS/FAILED情况及相关原因</p>
									<p>支持多样本自定义比较</p>
									<p>数据表格均可csv、excel、pdf导出</p>
								</li>
								<br />
								<li>
									<h4>样本覆盖度</h4>
									<p>推荐使用<strong>质量控制－质控报告</strong></p>
									<p>数据与<strong>质量控制－质控报告</strong>兼容</p>
								</li>
								<br />
								<li>
									<h4>扩增子检测</h4>
									<p>暂停更新</p>
								</li>
							</ul>
						</li>
						<br />
						<li>
							<h3>数据库</h3>
							<ul>
								<li>
									<h4>NGS Lab</h4>
									<p>收样、抽提、建库、上机等相关数据的存储与检索</p>
									<p>暂停开发</p>
								</li>
							</ul>
						</li>
						<br />
						<li>
							<h3>工具</h3>
							<ul>
								<li>
									<h4>SAM FLAG Decode</h4>
								</li>
							</ul>
						</li>
					</ul>
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

		<!-- Custom Theme Scripts -->
		<script src="./build/js/custom.min.js"></script>

	</body>
</html>
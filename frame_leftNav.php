<?php
/* PAGE    : frame_leftNav
 * AUTHOR  : codeunsolved@gmail.com
 * CREATED : August 23 2016
 * VERSION : v0.0.1a
 */
echo <<<LEFT_NAV
				<div class="col-md-3 left_col">
					<div class="left_col scroll-view">
						<div class="navbar nav_title" style="border: 0;">
							<a href="index.php" class="site_title">Topgen Dashboard</a>
						</div>

						<div class="clearfix"></div>

						<!-- menu profile quick info -->
						<div class="profile">
							<div class="profile_pic">
								<img src="images/admin.jpg" alt="..." class="img-circle profile_img">
							</div>
							<div class="profile_info">
								<span>Welcome,</span>
								<h2>Topgen admin</h2>
							</div>
						</div>
						<!-- /menu profile quick info -->

						<br />
						<br />
						<br />
						<br />

						<!-- sidebar menu -->
						<div id="sidebar-menu" class="main_menu_side hidden-print main_menu">
							<div class="menu_section">
								<h3>		</h3>
								<ul class="nav side-menu">
									<li><a><i class="fa fa-cube"></i> 质量控制 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="qc_report.php">质控报告</a></li>
										</ul>
									</li>
									<li><a><i class="fa fa-database"></i> 数据库 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="db_MyCancerGenome.php">MyCancerGenome</a></li>
											<li><a href="db_haplox_targeted_drugs.php">HaploX 靶向药 3.0</a></li>
											<li><a href="db_lab.php">NGS lab</a></li>
										</ul>
									</li>
									<li><a><i class="fa fa-area-chart"></i> 分析 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="anly_withAnnovar.php">withAnnovar</a></li>
											<li><a href="anly_BRCA_LargeRA.php">BRCA 大片段缺失</a></li>
										</ul>
									</li>
									<li><a><i class="fa fa-book"></i> 文档 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="doc_ref.php">参考手册</a></li>
										</ul>
									</li>
									<li><a><i class="fa fa-calculator"></i> 工具 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="tools_sam_flag_decode.php">SAM FLAG decode</a></li>
										</ul>
									</li>
									<li><a><i class="fa fa-laptop"></i> 管理 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="＃">用户</a></li>
										</ul>
									</li>
								</ul>
							</div>
						</div>
						<!-- /sidebar menu -->

						<!-- /menu footer buttons -->
						<div class="sidebar-footer hidden-small">
							<a href="#" data-toggle="tooltip" data-placement="top" title="Settings">
								<span class="glyphicon glyphicon-cog" aria-hidden="true"></span>
							</a>
							<a href="#" data-toggle="tooltip" data-placement="top" title="FullScreen">
								<span class="glyphicon glyphicon-fullscreen" aria-hidden="true"></span>
							</a>
							<a href="#" data-toggle="tooltip" data-placement="top" title="Lock">
								<span class="glyphicon glyphicon-eye-close" aria-hidden="true"></span>
							</a>
							<a href="#" data-toggle="tooltip" data-placement="top" title="Logout">
								<span class="glyphicon glyphicon-off" aria-hidden="true"></span>
							</a>
						</div>
						<!-- /menu footer buttons -->
					</div>
				</div>
LEFT_NAV;
?>

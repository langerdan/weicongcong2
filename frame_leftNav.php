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
											<li><a href="qc_sample_cover.php">样本覆盖度</a></li>
											<li><a href="qc_amplicon.php">扩增子检测</a></li>
										</ul>
									</li>
									<li><a><i class="fa fa-exchange"></i> 注释 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="db_topanno.php">TopAnno</a></li>
										</ul>
									</li>
									<li><a><i class="fa fa-database"></i> 数据库 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="db_lab.php">NGS lab</a></li>
										</ul>
									</li>
									<li><a><i class="fa fa-book"></i> 文档 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="doc_ref.php">参考</a></li>
										</ul>
									</li>
									<li><a><i class="fa fa-calculator"></i> 工具 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="tools_sam_flag_decode.php">SAM FLAG decode</a></li>
										</ul>
									</li>
									<li><a><i class="fa fa-laptop"></i> 管理 <span class="fa fa-chevron-down"></span></a>
										<ul class="nav child_menu">
											<li><a href="admin_user.php">用户</a></li>
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
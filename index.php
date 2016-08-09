<!-- 
 * PAGE     : index_qc
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 7 2016
 * VERSION  : v0.0.1a
-->

<!DOCTYPE html>
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
        <div class="col-md-3 left_col">
          <div class="left_col scroll-view">
            <div class="navbar nav_title" style="border: 0;">
              <a href="index.html" class="site_title">Topgen Dashboard</a>
            </div>
                
            <div class="clearfix"></div>
                
            <!-- menu profile quick info -->
            <div class="profile">
              <div class="profile_pic">
                <img src="images/admin.jpg" alt="..." class="img-circle profile_img"><!--profile_img_1 -->
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
                <h3>    </h3>
                <ul class="nav side-menu">
                  <li><a><i class="fa fa-home"></i> 质量控制 <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="qc_amplicon.html">扩增子</a></li>
                    </ul>
                  </li>
                  <li><a><i class="fa fa-database"></i> 数据库 <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="db_.html">  </a></li>
                    </ul>
                  </li>
                  <li><a><i class="fa fa-laptop"></i> Administration <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="admin_user.html">用户</a></li>
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
        <!-- /left navigation -->
        
        <!-- top navigation -->
        <div class="top_nav">
          <div class="nav_menu">
            <nav class="" role="navigation">
              <div class="nav toggle">
                <a id="menu_toggle"><i class="fa fa-bars"></i></a>
              </div>

              <ul class="nav navbar-nav navbar-right">
                <li class="">
                  <a href="javascript:;" class="user-profile dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
                    <img src="images/admin.jpg" alt="">Topgen admin<!--profile_img_2 -->
                    <span class=" fa fa-angle-down"></span>
                  </a>
                  <ul class="dropdown-menu dropdown-usermenu pull-right">
                    <li><a href="javascript:;"> Profile</a></li>
                    <li>
                      <a href="javascript:;">
                        <span>Settings</span>
                      </a>
                    </li>
                    <li><a href="javascript:;">Help</a></li>
                    <li><a href="#"><i class="fa fa-sign-out pull-right"></i> Log Out</a></li>
                  </ul>
                </li>
                
                <li role="presentation" class="dropdown">
                  <a href="javascript:;" class="dropdown-toggle info-number" data-toggle="dropdown" aria-expanded="false">
                    <i class="fa fa-envelope-o"></i>
                    <span class="badge bg-green">1</span>
                  </a>
                  <ul id="menu1" class="dropdown-menu list-unstyled msg_list" role="menu">
                    <li>
                      <a>
                        <span class="image"><img src="images/admin.jpg" alt="Profile Image" /></span>
                        <span>
                          <span>Topgen admin</span>
                          <span class="time">2016年08月06日</span>
                        </span>
                        <span class="message">
                          欢迎使用Topgen Dashboard!
                        </span>
                      </a>
                    </li>
                      <div class="text-center">
                        <a>
                          <strong>See All Alerts</strong>
                          <i class="fa fa-angle-right"></i>
                        </a>
                      </div>
                    </li>
                  </ul>
                </li>
              </ul>
            </nav>
          </div>
        </div>
        <!-- /top navigation -->
        
        <!-- page content -->
        <div class="right_col" role="main">
          <!-- top tiles -->
		  <div class="row">
            <!-- data select-->
            <div class="col-md-3 col-sm-3 col-xs-3">
			  <br />
              <div class="dropdown">
                <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" aria-expanded="true" style="width: 69%;">选择批次
                <span class="caret"></span></button>
                <ul id="data_select" class="dropdown-menu" style="width:69%">
                  <?php
				    $dir = "data";
					$files = array();
					
					if (is_dir($dir)) {
					  if ($dh = opendir($dir)) {
					    while ($files[] = readdir($dh));
                        sort($files);
						closedir($dh);
				      }else {
					    echo "<li><a href=\"#\"> ！数据文件夹无法读取 ！</a></li>";
					  }
					}else {
				      echo "<li><a href=\"#\"> ！数据文件夹不存在 ！</a></li>";
					}
					
					foreach ($files as $file) {
				      if ($file <> "." && $file <> ".." && !preg_match("/^[#.]/i",$file)) {
						echo "<li><a href=\"#\" onclick=\"loadData('".$file."');return false;\">".$file."</a></li>";
					  }
					}
				  ?>
                </ul>
              </div>
            </div>
            <!-- /data select-->
			
            <div class="tile_count">
              <div class="col-md-3 col-sm-3 col-xs-3 tile_stats_count">
                <span class="count_top"><i class="fa fa-circle"></i> 数据批次</span>
				<br />
                <div id="data_name" class="count green">--</div>
              </div>
              <div class="col-md-3 col-sm-3 col-xs-3 tile_stats_count">
                <span class="count_top"><i class="fa fa-circle"></i> 样本数量</span>
				<br />
                <div id="sample_num" class="count green">--</div>
              </div>
              <div class="col-md-3 col-sm-3 col-xs-3 tile_stats_count">
                <span class="count_top"><i class="fa fa-circle"></i>扩增子数量</span>
				<br />
                <div id="amplicon_num" class="count green">--</div>
              </div>
			</div>
          </div>
          <!-- /top tiles -->
          
          <br />
          
          <ul class="nav nav-tabs">
            <li class="active"><a data-toggle="tab" href="#amplicon_pass">扩增子检测</a></li>
			<li><a data-toggle="tab" href="#fastq">FASTQ检测</a></li>
          </ul>
          
          <div class="tab-content">
		  
            <!-- amplicon pass -->
            <div id="amplicon_pass" class="tab-pane fade in active">
              <!-- amplicon pass general -->
              <div class="row fixed_height_320">
                <div class="col-md-9 col-sm-9 col-xs-9">
				  <div class="x_panel fixed_height_320">
				    <div class="x_title">
                      <h2>Pass Check</h2>
                      <div class="clearfix"></div>
                    </div>
					<div class="x_content pre-scrollable" style="max-height: 241px;">
                      <table id="amplicon_pass_table" class="table table-bordered"></table>
					</div>
				  </div>
                </div>
                <div class="col-md-3 col-sm-3 col-xs-3">
                  <div class="x_panel fixed_height_320">
				    <div class="x_title" style="margin-bottom: 2px;">
                      <h2>扩增子明细</h2>
                      <div class="clearfix"></div>
                    </div>
					<div class="x_content">
                      <div style="text-align: center; margin-bottom: 7px">
                        <span id="amplicon_pass_percent" class="chart" data-percent="100">
                          <span id="amplicon_pass_num" style="display: inline-block; line-height: 110px; z-index: 2; font-size: 18px;">100/100</span>
                          <canvas></canvas>
						</span>
                      </div>

                      <h3 id="amplicon_chr_num" class="name_title"><strong>Chr </strong>?</h3>
					  <div class="divider"></div>
					  <p id="amplicon_gene" style="text-align: left;"><strong>基因 :</strong>???</p>
                      <p id="amplicon_pos" style="text-align: left;"><strong>位置 :</strong>??? - ???</p>
                      <p id="amplicon_len" style="text-align: left;"><strong>长度 :</strong>???</p>
					</div>
				  </div>
                </div>
              </div>
              <!-- /amplicon pass general -->
              
              <br />
              
              <!-- amplicon pass graph -->
              <div class="col-md-12 col-sm-12 col-xs-12">
			    <div class="x_panel">
			      <div class="x_title">
                    <h3><strong>扩增子位点覆盖图</strong></h3>
                    <div class="clearfix"></div>
                  </div>
				  <div class="x_content">
			        <!-- graph control-->
			        <div class="col-md-12 col-sm-12 col-xs-12">
					  <div class="x_panel">
					    <div class="x_title">
						  <h2>控制面板</h2>
                          <div class="clearfix"></div>
						</div>
						<div class="x_content">
						</div>
					  </div>
				    </div>
				    <!-- /graph control-->
				
				    <div class="col-md-12 col-sm-12 col-xs-12">
				      <div style="width: 100%;">
                        <canvas id="canvas_amplicon_depth"></canvas>
					  </div>
					</div>
				  </div>
				</div>
			  </div>
              <!-- /amplicon pass graph -->
            </div>
            <!-- /amplicon pass -->
              
          </div>
        </div>
        <!-- /page content -->
        
		<!-- footer content -->
        <footer style="background: #F7F7F7;">
          <div class="pull-right">
            上海鼎晶生物医药科技股份有限公司
          </div>
          <div class="clearfix"></div>
        </footer>
        <!-- /footer content -->
      </div>
    </div>
	
	<!-- jQuery -->
    <script src="./vendors/jquery/dist/jquery.min.js"></script>
    <!-- Bootstrap -->
    <script src="./vendors/bootstrap/dist/js/bootstrap.min.js"></script>
    <!-- Chart.js -->
    <script src="./vendors/Chart.js/dist/Chart.min.js"></script>
	<!-- easy-pie-chart -->
    <script src="./vendors/jquery.easy-pie-chart/dist/jquery.easypiechart.min.js"></script>
	
	<!-- Custom Theme Scripts -->
    <script src="./build/js/custom.min.js"></script>
	
	<!-- easypie -->
    <!-- <script src="js/easypie/jquery.easypiechart.min.js"></script> -->
    <script>
      $(function() {
        $('.chart').easyPieChart({
          easing: 'easeOutElastic',
          delay: 3000,
          barColor: '#26B99A',
          trackColor: '#E74C3C',
          scaleColor: false,
          lineWidth: 20,
          trackWidth: 16,
          lineCap: 'butt',
          onStep: function(from, to, percent) {
            $(this.el).find('.percent').text(Math.round(percent));
          }
        });
      });
    </script>

    <!-- Amplicon Pass Scripts -->
	<script src="./js/loaddata.js"></script>
	<script src="./js/loadamplicongraph.js"></script>
	
  </body>
</html>
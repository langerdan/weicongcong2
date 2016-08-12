<!--
 * PAGE     : qc_sample_cover
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 10 2016
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

            <br>
            <br>
            <br>
            <br>

            <!-- sidebar menu -->
            <div id="sidebar-menu" class="main_menu_side hidden-print main_menu">
              <div class="menu_section">
                <h3>    </h3>
                <ul class="nav side-menu">
                  <li><a><i class="fa fa-cube"></i> 质量控制 <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="qc_sample_cover.php">样本覆盖度</a></li>
                      <li><a href="qc_amplicon.php">扩增子检测</a></li>
                    </ul>
                  </li>
                  <li><a><i class="fa fa-database"></i> 数据库 <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="db_.php">  </a></li>
                    </ul>
                  </li>
                  <li><a><i class="fa fa-laptop"></i> Administration <span class="fa fa-chevron-down"></span></a>
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
                    <img src="images/admin.jpg" alt="">Topgen admin
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
              <br>
              <div class="dropdown">
                <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" aria-expanded="true" style="width: 69%;">选择批次<span class="caret"></span></button>
                <ul id="data_select" class="dropdown-menu" style="width:69%">
                  <?php
                    $data_dir = "data";
                    $dirs = array();

                    if (is_dir($data_dir)) {
                      if ($dh = opendir($data_dir)) {
                        while ($dirs[] = readdir($dh));
                        sort($dirs);
                        closedir($dh);
                        } else {
                        echo "<li><a href=\"#\"> ！数据文件夹无法读取 ！</a></li>";
                      }
                    } else {
                      echo "<li><a href=\"#\"> ！数据文件夹不存在 ！</a></li>";
                    }

                    foreach ($dirs as $dir) {
                      $path_dir = $data_dir.'/'.$dir;
                      if (is_dir($path_dir) && $dir <> "." && $dir <> ".." && !preg_match("/^[#.]/i",$dir)) {
                        if ($sub_dh = opendir($path_dir)) {
                          while ($sub_dirs[] = readdir($sub_dh));
                          closedir($sub_dh);
                          foreach ($sub_dirs as $sub_dir) {
                            if (is_dir($path_dir.'/'.$sub_dir) and $sub_dir == "sample_cover") {
                              echo "<li><a href=\"#\" onclick=\"loadData('".$dir."');return false;\">".$dir."</a></li>";
                              break;
                            }
                          }
                        }
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

                <br>

                <div id="data_name" class="count blue">--</div>
              </div>
              <div class="col-md-3 col-sm-3 col-xs-3 tile_stats_count">
                <span class="count_top"><i class="fa fa-circle"></i> 样本数量</span>

                <br>

                <div id="sample_num" class="count blue">--</div>
              </div>
              <div class="col-md-3 col-sm-3 col-xs-3 tile_stats_count">
                <span class="count_top"><i class="fa fa-circle"></i>片段数量</span>

                <br>

                <div id="frag_num" class="count blue">--</div>
              </div>
            </div>
          </div>
          <!-- /top tiles -->

          <br>

          <ul class="nav nav-tabs">
            <li class="active"><a data-toggle="tab" href="#tb_sample_cover">样本覆盖度</a></li>
          </ul>

          <div class="tab-content">

            <!-- sample cover -->
            <div id="tb_sample_cover" class="tab-pane fade in active">
              <!-- sample cover general -->
              <div class="row">
                <div class="col-md-9 col-sm-9 col-xs-9">
                  <div class="x_panel fixed_height_390">
                    <div class="x_content" style="max-height: 311px;">
                      <ul class="nav nav-tabs">
                        <li class="active"><a data-toggle="tab" href="#tb_sample_cover_table">样本覆盖梯度</a></li>
                        <li><a data-toggle="tab" href="#tb_sample_cover_graph">样本覆盖对比图</a></li>
                      </ul>

                      <div class="tab-content">

                        <!-- sample cover table -->
                        <div id="tb_sample_cover_table" class="tab-pane fade in active pre-scrollable">
                          <table id="sample_cover_table" class="table table-bordered table-fixed"></table>
                        </div>
                        <!-- /smaple coover table -->

                        <!-- sample cover graph -->
                        <div id="tb_sample_cover_graph" class="tab-pane fade in active" style="width: 100%;">
                          <canvas id="sample_cover_graph"></canvas>
                        </div>
                        <!-- /smaple coover graph -->

                      </div>
                    </div>
                  </div>
                </div>

                <div class="col-md-3 col-sm-3 col-xs-3">
                  <div class="x_panel fixed_height_390">
                    <div class="x_title">
                      <h2>样本覆盖度概况</h2>
                      <div class="clearfix"></div>
                    </div>
                    <div class="x_content">
                      <p id="sample_depth_aver" style="text-align: left;"><strong>平均深度 :</strong>???</p>
                      <p id="sample_depth_max" style="text-align: left;"><strong>最大深度 :</strong>???</p>
                      <p id="sample_depth_min" style="text-align: left;"><strong>最小深度 :</strong>???</p>
                    </div>
                  </div>
                </div>
              </div>
              <!-- /sample cover general -->

              <!-- frag cover -->
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="col-md-9 col-sm-9 col-xs-9">
                  <div class="x_panel">
                    <div class="x_title">
                      <h2><strong>片段覆盖梯度</strong></h2>
                      <div class="clearfix"></div>
                    </div>
                    <div class="x_content pre-scrollable">
                      <table id="frag_cover_table" class="table table-bordered table-fixed"></table>
                    </div>
                  </div>
                </div>

                <div class="col-md-3 col-sm-3 col-xs-3">
                  <div class="x_panel">
                    <div class="x_title">
                      <h2>片段覆盖度概况</h2>
                      <div class="clearfix"></div>
                    </div>
                    <div class="x_content">
                      <h3 class="name_title" style="text-align: center;"><strong id="sample_num">???</strong></h3>
                      <div class="divider"></div>
                      <h2 id="frag_chr_num" class="name_title" style="text-align: center;"><strong>Chr </strong>?</h2>
                      <p id="frag_gene" style="text-align: left;"><strong>基因 : </strong>???</p>
                      <p id="frag_pos" style="text-align: left;"><strong>位置 : </strong>??? - ???</p>
                      <p id="frag_len" style="text-align: left;"><strong>长度 : </strong>???</p>
                      <br>
                      <p id="frag_depth_aver" style="text-align: left;"><strong>平均深度 : </strong>???</p>
                      <p id="frag_depth_max" style="text-align: left;"><strong>最大深度 : </strong>???</p>
                      <p id="frag_depth_min" style="text-align: left;"><strong>最小深度 : </strong>???</p>
                    </div>
                  </div>
                </div>
              </div>
              <!-- /frag cover -->

              <!-- frag cover graph -->
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h2><strong>片段覆盖图</strong></h2>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <canvas id="frag_cover_graph"></canvas>
                  </div>
                </div>
              </div>
              <!-- /frag cover graph -->
          </div>
          <!-- /sample cover -->

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
          barColor: '#3498DB',
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

    <!-- Sample Coverage Scripts -->


  </body>
</html>
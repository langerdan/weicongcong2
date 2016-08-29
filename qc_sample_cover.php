<!DOCTYPE html>
<!--
 * PAGE     : qc_sample_cover
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 10 2016
 * VERSION  : v0.0.1a
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

          <!-- top tiles -->
          <div class="row">
            <!-- data select-->
            <div class="col-md-3 col-sm-3 col-xs-3">
              <br>
              <div class="dropdown">
                <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" aria-expanded="true" style="width: 69%;">选择批次<span class="caret"></span></button>
                <ul id="data_select" class="dropdown-menu" style="width: 69%;">
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
                <span class="count_top"><i class="fa fa-circle"></i> 片段数量</span>

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
              <div class="row">
                <div class="col-md-9 col-sm-9 col-xs-9">
                  <div class="x_panel fixed_height_390">
                    <div class="x_content">
                      <ul class="nav nav-tabs">
                        <li class="active"><a data-toggle="tab" href="#tb_sample_cover_table">样本覆盖梯度</a></li>
                        <li><a data-toggle="tab" href="#tb_sample_cover_graph" onclick="loadSampleCoverGraph();return false;">样本覆盖对比图</a></li>
                      </ul>

                      <div class="tab-content">

                        <div id="tb_sample_cover_table" class="tab-pane fade in active pre-scrollable" style="width: 100%; max-height: 311px;">
                          <table id="sample_cover_table" class="table table-bordered table-head-fixed"></table>
                        </div>

                        <div id="tb_sample_cover_graph" class="tab-pane fade in active" style="width: 100%; height: 311px;">
                          <canvas id="sample_cover_graph"></canvas>
                        </div>

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
                      <h3 class="name_title" style="text-align: center;"><strong id="sample_name">???</strong></h3>
                      <div class="divider"></div>
                      <p id="aver_sample_depth" style="text-align: left;"><strong>平均深度 :</strong> ???</p>
                      <p id="cutoff_sample_depth" style="text-align: left;"><strong>cutoff深度 :</strong> ???</p>
                      <p id="max_sample_depth" style="text-align: left;"><strong>最大深度 :</strong> ???</p>
                      <p id="min_sample_depth" style="text-align: left;"><strong>最小深度 :</strong> ???</p>
                      <br>
                      <div id="sample_absent_frag" class="panel panel-default">
                        <div id="sample_absent_frag_heading" class="panel-heading"><strong>缺失片段 :</strong> ???</div>
                        <div id="sample_absent_frag_body" class="panel-body pre-scrollable" style="width: 100%; max-height: 70px;"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="col-md-9 col-sm-9 col-xs-9">
                  <div class="x_panel fixed_height_390">
                    <div class="x_title">
                      <h2><strong>片段覆盖梯度</strong></h2>
                      <div class="clearfix"></div>
                    </div>
                    <div class="x_content pre-scrollable" style="width: 100%; max-height: 311px;">
                      <table id="frag_cover_table" class="table table-bordered table-head-fixed"></table>
                    </div>
                  </div>
                </div>

                <div class="col-md-3 col-sm-3 col-xs-3">
                  <div class="x_panel fixed_height_390">
                    <div class="x_title">
                      <h2>片段覆盖度概况</h2>
                      <div class="clearfix"></div>
                    </div>
                    <div class="x_content">
                      <h3 class="name_title" style="text-align: center;"><strong id="frag_name">???</strong></h3>
                      <div class="divider"></div>
                      <h2 id="frag_chr_num" class="name_title" style="text-align: center;"><strong>Chr </strong>?</h2>
                      <p id="frag_gene" style="text-align: left;"><strong>基因 : </strong>???</p>
                      <p id="frag_pos" style="text-align: left;"><strong>位置 : </strong>??? - ???</p>
                      <p id="frag_len" style="text-align: left;"><strong>长度 : </strong>???</p>
                      <br>
                      <p id="aver_frag_depth" style="text-align: left;"><strong>平均深度 : </strong>???</p>
                      <p id="max_frag_depth" style="text-align: left;"><strong>最大深度 : </strong>???</p>
                      <p id="min_frag_depth" style="text-align: left;"><strong>最小深度 : </strong>???</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h2><strong>片段覆盖图</strong></h2>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content" style="width: 100%; height: 711px;">
                    <canvas id="frag_cover_graph"></canvas>
                  </div>
                </div>
              </div>
            </div>
            <!-- /sample cover -->
          </div>

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
    <!-- Chart.js -->
    <script src="./vendors/Chart.js/dist/Chart.min.js"></script>
    <!-- easy-pie-chart -->
    <script src="./vendors/jquery.easy-pie-chart/dist/jquery.easypiechart.min.js"></script>

    <!-- Custom Theme Scripts -->
    <script src="./build/js/custom.min.js"></script>

    <!-- Sample Coverage Scripts -->
    <script src="js/qc_loadsamplecoverdata.js"></script>

  </body>
</html>
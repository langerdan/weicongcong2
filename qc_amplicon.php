<!-- 
 * PAGE     : qc_amplicon
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
                <button class="btn btn-success dropdown-toggle" type="button" data-toggle="dropdown" aria-expanded="true" style="width: 69%;">选择批次<span class="caret"></span></button>
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
                            if (is_dir($path_dir.'/'.$sub_dir) and $sub_dir == "amplicon") {
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

                <div id="data_name" class="count green">--</div>
              </div>
              <div class="col-md-3 col-sm-3 col-xs-3 tile_stats_count">
                <span class="count_top"><i class="fa fa-circle"></i> 样本数量</span>

                <br>

                <div id="sample_num" class="count green">--</div>
              </div>
              <div class="col-md-3 col-sm-3 col-xs-3 tile_stats_count">
                <span class="count_top"><i class="fa fa-circle"></i>扩增子数量</span>

                <br>

                <div id="amplicon_num" class="count green">--</div>
              </div>
            </div>
          </div>
          <!-- /top tiles -->
          
          <br>
          
          <ul class="nav nav-tabs">
            <li class="active"><a data-toggle="tab" href="#tb_amplicon_pass">扩增子检测</a></li>
          </ul>
          
          <div class="tab-content">
      
            <!-- amplicon pass -->
            <div id="tb_amplicon_pass" class="tab-pane fade in active">
              <!-- amplicon pass general -->
              <div class="row">
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

                      <h3 id="amplicon_chr_num" class="name_title" style="text-align: center;"><strong>Chr </strong>?</h3>
                      <div class="divider"></div>
                      <p id="amplicon_gene" style="text-align: left;"><strong>基因 :</strong>???</p>
                      <p id="amplicon_pos" style="text-align: left;"><strong>位置 :</strong>??? - ???</p>
                      <p id="amplicon_len" style="text-align: left;"><strong>长度 :</strong>???</p>
                    </div>
                  </div>
                </div>
              </div>
              <!-- /amplicon pass general -->
              
              <br>
              
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
        
                    <div class="col-md-12 col-sm-12 col-xs-12" style="width: 100%; height: 1000px;">
                      <canvas id="canvas_amplicon_depth"></canvas>
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
  
    <!-- easypie -->
    <script>
      $(document).ready(function() {
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
    <script src="js/qc_loadamplicondata.js"></script>
  
  </body>
</html>
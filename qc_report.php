<!--
 * PAGE     : qc_report
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 25 2016
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
          <!-- search NGS lab database -->
          <div class="row" >
            <div class="x_panel">
              <div class="x_title">
                <h2>检索数据库</h2>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div class="col-md-12 col-sm-12 col-xs-12 form-group top_search">
                  <div class="input-group" style="width:69%; margin-left: 20px">
                    <input type="text" name="search_term" class="form-control" placeholder="Search ...">
                    <span class="input-group-btn">
                      <button id="search_go" class="btn btn-primary" type="button" style="color: white"> Go! </button>
                    </span>
                  </div>
                </div>
                <div class="col-md-12 col-sm-12 col-xs-12 form-group">
                  <div class="col-md-2 col-sm-2 col-xs-2">
                    <select name="project" class="form-control">
                      <option value="onco"> onco </option>
                      <option value="brac" selected> BRAC </option>
                    </select>
                  </div>
                  <div class="col-md-10 col-sm-10 col-xs-10">
                    <input type="radio" name="search_type" value="all" checked> All&nbsp;&nbsp;
                    <input type="radio" name="search_type" value="sample_id"> 样本编号&nbsp;&nbsp;
                    <input type="radio" name="search_type" value="sample_type"> 样本类型&nbsp;&nbsp;
                    <input type="radio" name="search_type" value="lib_reagent"> 建库试剂&nbsp;&nbsp;
                    <input type="radio" name="search_type" value="lib_id"> 建库批次&nbsp;&nbsp;
                    <input type="radio" name="search_type" value="run_id"> 上机批次&nbsp;&nbsp;
                  </div>
                </div>
                <div class="col-md-12 col-sm-12 col-xs-12">
                  <div class="divider-dashed"></div>
                </div>

                <div class="col-md-12 col-sm-12 col-xs-12">
                  <div class="x_panel">
                    <div class="x_title">
                      <h4>搜索结果</h4>
                      <div class="clearfix"></div>
                    </div>
                    <div class="x_content">
                      <table id="datatable-buttons" class="table table-striped table-bordered"></table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- /search NGS lab database -->

          <!-- Sample Sequencing QC report -->
          <div class="row">
            <div class="x_panel">
              <div class="x_title">
                <h2>样品下机质量控制报告 v0.1a</h2>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div class="col-md-12 col-sm-12 col-xs-12">
                  <div class="x_panel">
                    <div class="x_title">
                      <h4>概览</h4>
                      <div class="clearfix"></div>
                    </div>
                    <div class="x_content">
                      <div class="col-md-4 col-sm-4 col-xs-4">
                        <h3 class="name_title"><strong id="sample_name">???</strong></h3>
                        <div class="divider"></div>
                        <table style="width: 100%">
                          <tbody>
                            <tr>
                              <td><p style="text-align: left;"><strong>回帖reads数</strong></p></td>
                              <td><p><strong>&nbsp;:&nbsp;</strong></p></td>
                              <td><p id="num_mapped_reads" style="text-align: left;">???</p></td>
                            </tr>
                            <tr>
                              <td><p style="text-align: left;"><strong>目标区段reads百分比</strong></p></td>
                              <td><p><strong>&nbsp;:&nbsp;</strong></p></td>
                              <td><p id="per_target_reads" style="text-align: left;">???</p></td>
                            </tr>
                            <tr>
                              <td><p style="text-align: left;"><strong>平均深度</strong></p></td>
                              <td><p><strong>&nbsp;:&nbsp;</strong></p></td>
                              <td><p id="aver_smaple_depth" style="text-align: left;">???</p></td>
                            </tr>
                             <tr>
                              <td><p style="text-align: left;"><strong>最大深度</strong></p></td>
                              <td><p><strong>&nbsp;:&nbsp;</strong></p></td>
                              <td><p id="max_smaple_depth" style="text-align: left;">???</p></td>
                            </tr>
                            <tr>
                              <td><p style="text-align: left;"><strong>最小深度</strong></p></td>
                              <td><p><strong>&nbsp;:&nbsp;</strong></p></td>
                              <td><p id="min_smaple_depth" style="text-align: left;">???</p></td>
                            </tr>
                            <tr>
                              <td colspan="3">
                                <div class="divider-dashed"></div>
                              </td>
                            </tr>
                            <tr>
                              <td colspan="3"><p style="text-align: left;"><strong>缺失片段 :</strong></p></td>
                            </tr>
                            <tr>
                              <td colspan="3">
                                <div id="sample_absent_frag" class="panel panel-default">
                                  <div id="sample_absent_frag_heading" class="panel-heading"></div>
                                  <div id="sample_absent_frag_body" class="panel-body pre-scrollable" style="width: 100%; max-height: 70px;"></div>
                                </div>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>

                      <div class="col-md-8 col-sm-8 col-xs-8">
                        <canvas id="sample_cover_overview"></canvas>
                      </div>
                    </div>
                  </div>

                  <!-- target base coverage -->
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title">
                        <h4>目标碱基覆盖度</h4>
                        <div class="clearfix"></div>
                      </div>
                      <div class="x_content">
                        <div class="col-md-12 col-sm-12 col-xs-12">
                          <table style="width: 100%">
                            <tbody>
                              <tr>
                                <td><p style="text-align: left;"><strong>目标碱基数</strong></p></td>
                                <td><p><strong>&nbsp;:&nbsp;</strong></p></td>
                                <td><p id="num_target_bp" style="text-align: left;">???</p></td>
                              </tr>
                              <tr>
                                <td colspan="3">
                                  <div class="divider-dashed"></div>
                                </td>
                              </tr>
                              <tr>
                                <td colspan="3"><p style="text-align: left;"><strong>碱基覆盖梯度 :</strong></p></td>
                              </tr>
                              <tr>
                                <td colspan="3"><table id="depth_level" style="text-align: left;"></table></td>
                              </tr>
                              <tr>
                                <td colspan="3">
                                  <div class="divider-dashed"></div>
                                </td>
                              </tr>
                              <tr>
                                <td colspan="3"><p><strong>0x 片段 :</strong></p></td>
                              </tr>
                              <tr>
                                <td colspan="3"><table id="0x_frag"></table></td>
                              </tr>
                            </tbody>
                          </table>
                        </div>

                        <div class="col-md-12 col-sm-12 col-xs-12">
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
                      </div>
                    </div>
                  </div>
                  <!-- /target base coverage -->
                </div>
              </div>
            </div>            
          </div>
          <!-- /Sample Sequencing QC report -->
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
  
  </body>
</html>
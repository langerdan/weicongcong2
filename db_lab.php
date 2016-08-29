<!DOCTYPE html>
<!--
 * PAGE     : db_lab
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 23 2016
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
              <h3>NGS Lab管理检索系统 <small>收样、抽提、建库、上机</small></h3>
            </div>
            <div class="title_right"></div>
          </div>
          <div class="clearfix"></div>

          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2>待处理样本</h2>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <ul class="nav nav-tabs">
                    <li class="active"><a data-toggle="tab" href="#tb_unHS_onco"> onco </a></li>
                    <li><a data-toggle="tab" href="#tb_unHS_brac"> BRAC </a></li>
                  </ul>

                  <div class="tab-content">

                    <!-- unhandled sample - onco -->
                    <div id="tb_unHS_onco" class="tab-pane fade in active">
                      <div class="row">
                        <div class="tile_count">
                          <div class="col-md-1 col-sm-1 col-xs-1">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-2 tile_stats_count" style="border-left: none !important;">
                            <span class="count_top"><i class="fa fa-circle"></i> 已收样</span>

                            <br>

                            <div id="SAP_num" class="count blue">--</div>
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-2 tile_stats_count">
                            <span class="count_top"><i class="fa fa-circle"></i> 抽提中</span>

                            <br>

                            <div id="EXTR_num" class="count blue">--</div>
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-2 tile_stats_count">
                            <span class="count_top"><i class="fa fa-circle"></i> 建库中</span>

                            <br>

                            <div id="LIB_num" class="count blue">--</div>
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-2 tile_stats_count">
                            <span class="count_top"><i class="fa fa-circle"></i> 上机中</span>

                            <br>

                            <div id="RUN_num" class="count blue">--</div>
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-2 tile_stats_count">
                            <span class="count_top"><i class="fa fa-circle"></i> 待校对</span>

                            <br>

                            <div id="INIT_num" class="count blue">--</div>
                          </div>
                        </div>
                      </div>

                      <div class="row">
                        <div class="col-md-12 col-sm-12 col-xs-12">
                          <div class="x_panel">
                            <div class="x_content">
                              <table id="datatable_unHS_onco" class="table table-striped table-bordered">
                                <thead>
                                  <tr>
                                    <th>序号</th>
                                    <th>样本名称</th>
                                    <th>进度</th>
                                    <th>说明</th>
                                    <th>操作</th>
                                  </tr>
                                </thead>
                              </table>
                              
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <!-- /unhandled sample - onco -->

                    <!-- unhandled sample - BRAC -->
                    <!-- /unhandled sample - BRAC -->
                  </div> 
                </div>
              </div>
            </div>
          </div>

          <div class="row" >
            <div class="x_panel">
              <div class="x_title">
                <h2>检索NGS Lab数据库</h2>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div class="col-md-12 col-sm-12 col-xs-12 form-group top_search">
                  <div class="input-group" style="width:69%; margin-left: 20px;">
                    <input type="text" name="search_term" class="form-control" placeholder="Search ...">
                    <span class="input-group-btn">
                      <button id="search_go" class="btn btn-primary" type="button" style="color: white;"> Go! </button>
                    </span>
                  </div>
                </div>
                <div class="col-md-12 col-sm-12 col-xs-12 form-group">
                  <div class="col-md-2 col-sm-2 col-xs-2">
                    <select name="project" class="form-control">
                      <option value="onco" selected> onco </option>
                      <option value="brac"> BRAC </option>
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
                      <table id="datatable_searchresult" class="table table-striped table-bordered">
                        
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
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
    <!-- NProgress -->
    <script src="./vendors/nprogress/nprogress.js"></script>
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
    <script src="js/db_querydblab.js"></script>

    <!-- Datatables -->
    <script>
      $(document).ready(function() {
        loadunHandleSample('onco');
        $("#datatable_unHS_onco").dataTable( {
          "processing": true,
          "serverSide": true,
          "ajax": "db_lab_query.php?func=lab_unhs_tb&proj=onco"
        });
      });

      function loadunHandleSample(project) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (xhttp.readyState == 4 && xhttp.status == 200) {
            var json =  JSON.parse(xhttp.responseText);
            document.getElementById('SAP_num').innerHTML = json.SAP_num;
            document.getElementById('EXTR_num').innerHTML = json.EXTR_num;
            document.getElementById('LIB_num').innerHTML = json.LIB_num;
            document.getElementById('RUN_num').innerHTML = json.RUN_num;
          }
        };
        xhttp.open("GET", "db_lab_query.php?func=lab_unhs_stat&proj=" + project, true);
        xhttp.send();
      }

      function formatDataTable() {
        var handleDataTableButtons = function() {
          if ($("#datatable_searchresult").length) {
            $("#datatable_searchresult").DataTable({
              dom: "lfrtipB",
              buttons: [
                {
                  extend: "copy",
                  className: "btn-sm"
                },
                {
                  extend: "csv",
                  className: "btn-sm"
                },
                {
                  extend: "excel",
                  className: "btn-sm"
                },
                {
                  extend: "pdfHtml5",
                  className: "btn-sm"
                },
                {
                  extend: "print",
                  className: "btn-sm"
                  },
                ],
                responsive: true
            });
          }
        };

        TableManageButtons = function() {
          "use strict";
          return {
            init: function() {
              handleDataTableButtons();
            }
          };
        }();

        TableManageButtons.init();
      };
    </script>
    <!-- /Datatables -->
  </body>
</html>
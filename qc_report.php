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
          <!-- search QC report database -->
          <div class="row" >
            <div class="x_panel">
              <div class="x_title">
                <h2>检索质控报告</h2>
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
                  <div class="col-md-1 col-sm-1 col-xs-1">
                    <select name="project" class="form-control">
                      <option value="onco"> onco </option>
                      <option value="brac" selected> BRAC </option>
                    </select>
                  </div>
                  <div class="col-md-2 col-sm-2 col-xs-2">
                    <select name="report_type" class="form-control" onchange="getSearchOptions()">
                      <option value=0 selected> － 选择报告类型 － </option>
                      <option value="sequencing_data" > 测序数据质量报告 </option>
                    </select>
                  </div>
                  <div id="search_options" class="col-md-9 col-sm-9 col-xs-9">
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
          <!-- /search QC report database -->

          <!-- QC report -->
          <div id="report_container" class="row">
        
          </div>
          <!-- /QC report -->
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
    
    <!-- QC report js -->
    <script src="./js/qc_queryreport.js"></script>

  </body>
</html>
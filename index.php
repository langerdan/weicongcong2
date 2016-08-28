<!-- 
 * PAGE     : index
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
        <?php include 'frame_leftNav.php';?>
        <!-- /left navigation -->
        
        <!-- top navigation -->
        <?php include 'frame_topNav.php';?>
        <!-- /top navigation -->
        
        <!-- page content -->
        <div class="right_col" role="main">
          <h4>目前开放页面：</h4>
          <ul>
            <li><h3>质量控制－质控报告（开发中）</h3></li>
            <li><h3>质量控制－样本覆盖度</h3></li>
            <li><h3>质量控制－扩增子检测</h3></li>
            <li><h3>数据库－NGS Lab管理检索系统（开发中）</h3></li>
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
    <!-- Chart.js -->
    <script src="./vendors/Chart.js/dist/Chart.min.js"></script>
    <!-- easy-pie-chart -->
    <script src="./vendors/jquery.easy-pie-chart/dist/jquery.easypiechart.min.js"></script>
  
    <!-- Custom Theme Scripts -->
    <script src="./build/js/custom.min.js"></script>
  
  </body>
</html>
<!DOCTYPE html>
<!-- 
 * PAGE     : index
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
          <h4>目前开放页面：</h4>
          <ul>
            <li>
              <h3>质量控制－质控报告（<strong style="color: green;">推荐</strong>）</h3>
              <p>通过相关数据库交叉检索报告，提示报告PASS/FAILED情况及相关原因</p>
              <p>支持多样本自定义比较</p>
              <p>数据表格均可csv、excel、pdf导出</p>
            </li>

            <br>

            <li>
              <h3>质量控制－样本覆盖度</h3>
              <p>推荐使用<strong>质量控制－质控报告</strong></p>
              <p>数据与<strong>质量控制－质控报告</strong>兼容</p>
            </li>
            
            <br>

            <li>
              <h3>质量控制－扩增子检测</h3>
              <p>暂不更新</p>
            </li>

            <br>

            <li>
              <h3>数据库－NGS Lab管理检索系统（暂停开发）</h3>
              <p>NGS Lab相关实验数据表格可查询检索（数据待补充）</p>
              <p>样本添加与跟进暂未开发</p>
            </li>
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

    <!-- Custom Theme Scripts -->
    <script src="./build/js/custom.min.js"></script>
  
  </body>
</html>
<!DOCTYPE html>
<!-- 
 * PAGE     : db_topanno
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : September 14 2016
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
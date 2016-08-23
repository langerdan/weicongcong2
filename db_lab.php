<!--
 * PAGE     : db_lab
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 23 2016
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
        <?php include 'leftNav.php';?>
        <!-- /left navigation -->

        <!-- top navigation -->
        <?php include 'topNav.php';?>
        <!-- /top navigation -->

        <!-- page content -->
        <div class="right_col" role="main">
          <div class="page-title">
            <div class="title_left">
              <h3>NGS lab 数据库 <small>抽提、建库、上机相关数据</small></h3>
            </div>
            <div class="title_right"></div>
          </div>
          <div class="col-md-12 col-sm-12 col-xs-12 form-group top_search">
            <div class="input-group" style="width:69%">
              <input type="text" name="search_term" class="form-control" placeholder="搜索...">
              <span class="input-group-btn">
                <button id="search_go" class="btn btn-default" type="button"> Go! </button>
              </span>
            </div>
            <div class="input-group" style="width:69%">
              &nbsp;&nbsp;
              <select name="project">
                <option value="onco" selected> onco </option>
                <option value="brac"> BRAC </option>
              </select>&nbsp;&nbsp;&nbsp;&nbsp;
              <input type="radio" name="search_type" value="all" checked> All&nbsp;&nbsp;
              <input type="radio" name="search_type" value="sample_id"> 样本编号&nbsp;&nbsp;
              <input type="radio" name="search_type" value="sample_type"> 样本类型&nbsp;&nbsp;
              <input type="radio" name="search_type" value="lib_reagent"> 建库试剂&nbsp;&nbsp;
              <input type="radio" name="search_type" value="lib_id"> 建库批次&nbsp;&nbsp;
              <input type="radio" name="search_type" value="run_id"> 上机批次&nbsp;&nbsp;
            </div>
          </div>
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
            	<div class="x_title">
              	<h2>搜索结果</h2>
                <div class="dt-buttons btn-group nav navbar-right panel_toolbox">
                	<p>导出：</p>
                  <a class="btn btn-default buttons-copy buttons-html5 btn-sm" tabindex="0" aria-controls="datatable-buttons"><span>Copy</span></a>
                  <a class="btn btn-default buttons-csv buttons-html5 btn-sm" tabindex="0" aria-controls="datatable-buttons"><span>CSV</span></a>
                  <a class="btn btn-default buttons-excel buttons-html5 btn-sm" tabindex="0" aria-controls="datatable-buttons"><span>Excel</span></a>
                  <a class="btn btn-default buttons-pdf buttons-html5 btn-sm" tabindex="0" aria-controls="datatable-buttons"><span>PDF</span></a>
                  <a class="btn btn-default buttons-print btn-sm" tabindex="0" aria-controls="datatable-buttons"><span>Print</span></a>
                </div>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div id="datatable_wrapper" class="dataTables_wrapper form-inline dt-bootstrap no-footer">
                  <div class="row">
                    <div class="col-sm-12">
                      <table id="datatable" class="table table-striped table-bordered dataTable no-footer" role="grid" aria-describedby="datatable_info">
                        <thead>
                        <tr role="row"><th class="sorting_asc" tabindex="0" aria-controls="datatable" rowspan="1" colspan="1" aria-sort="ascending" aria-label="Name: activate to sort column descending" style="width: 267px;">Name</th><th class="sorting" tabindex="0" aria-controls="datatable" rowspan="1" colspan="1" aria-label="Position: activate to sort column ascending" style="width: 423px;">Position</th><th class="sorting" tabindex="0" aria-controls="datatable" rowspan="1" colspan="1" aria-label="Office: activate to sort column ascending" style="width: 203px;">Office</th><th class="sorting" tabindex="0" aria-controls="datatable" rowspan="1" colspan="1" aria-label="Age: activate to sort column ascending" style="width: 114px;">Age</th><th class="sorting" tabindex="0" aria-controls="datatable" rowspan="1" colspan="1" aria-label="Start date: activate to sort column ascending" style="width: 203px;">Start date</th><th class="sorting" tabindex="0" aria-controls="datatable" rowspan="1" colspan="1" aria-label="Salary: activate to sort column ascending" style="width: 159px;">Salary</th></tr>
                        </thead>
                        <tbody>
                          <tr role="row" class="odd">
                          <td class="sorting_1">Airi Satou</td>
                          <td>Accountant</td>
                          <td>Tokyo</td>
                          <td>33</td>
                          <td>2008/11/28</td>
                          <td>$162,700</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Angelica Ramos</td>
                          <td>Chief Executive Officer (CEO)</td>
                          <td>London</td>
                          <td>47</td>
                          <td>2009/10/09</td>
                          <td>$1,200,000</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Ashton Cox</td>
                          <td>Junior Technical Author</td>
                          <td>San Francisco</td>
                          <td>66</td>
                          <td>2009/01/12</td>
                          <td>$86,000</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Bradley Greer</td>
                          <td>Software Engineer</td>
                          <td>London</td>
                          <td>41</td>
                          <td>2012/10/13</td>
                          <td>$132,000</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Brenden Wagner</td>
                          <td>Software Engineer</td>
                          <td>San Francisco</td>
                          <td>28</td>
                          <td>2011/06/07</td>
                          <td>$206,850</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Brielle Williamson</td>
                          <td>Integration Specialist</td>
                          <td>New York</td>
                          <td>61</td>
                          <td>2012/12/02</td>
                          <td>$372,000</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Bruno Nash</td>
                          <td>Software Engineer</td>
                          <td>London</td>
                          <td>38</td>
                          <td>2011/05/03</td>
                          <td>$163,500</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Caesar Vance</td>
                          <td>Pre-Sales Support</td>
                          <td>New York</td>
                          <td>21</td>
                          <td>2011/12/12</td>
                          <td>$106,450</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Cara Stevens</td>
                          <td>Sales Assistant</td>
                          <td>New York</td>
                          <td>46</td>
                          <td>2011/12/06</td>
                          <td>$145,600</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Cedric Kelly</td>
                          <td>Senior Javascript Developer</td>
                          <td>Edinburgh</td>
                          <td>22</td>
                          <td>2012/03/29</td>
                          <td>$433,060</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Charde Marshall</td>
                          <td>Regional Director</td>
                          <td>San Francisco</td>
                          <td>36</td>
                          <td>2008/10/16</td>
                          <td>$470,600</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Colleen Hurst</td>
                          <td>Javascript Developer</td>
                          <td>San Francisco</td>
                          <td>39</td>
                          <td>2009/09/15</td>
                          <td>$205,500</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Dai Rios</td>
                          <td>Personnel Lead</td>
                          <td>Edinburgh</td>
                          <td>35</td>
                          <td>2012/09/26</td>
                          <td>$217,500</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Donna Snider</td>
                          <td>Customer Support</td>
                          <td>New York</td>
                          <td>27</td>
                          <td>2011/01/25</td>
                          <td>$112,000</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Doris Wilder</td>
                          <td>Sales Assistant</td>
                          <td>Sidney</td>
                          <td>23</td>
                          <td>2010/09/20</td>
                          <td>$85,600</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Finn Camacho</td>
                          <td>Support Engineer</td>
                          <td>San Francisco</td>
                          <td>47</td>
                          <td>2009/07/07</td>
                          <td>$87,500</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Fiona Green</td>
                          <td>Chief Operating Officer (COO)</td>
                          <td>San Francisco</td>
                          <td>48</td>
                          <td>2010/03/11</td>
                          <td>$850,000</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Garrett Winters</td>
                          <td>Accountant</td>
                          <td>Tokyo</td>
                          <td>63</td>
                          <td>2011/07/25</td>
                          <td>$170,750</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Gavin Cortez</td>
                          <td>Team Leader</td>
                          <td>San Francisco</td>
                          <td>22</td>
                          <td>2008/10/26</td>
                          <td>$235,500</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Gavin Joyce</td>
                          <td>Developer</td>
                          <td>Edinburgh</td>
                          <td>42</td>
                          <td>2010/12/22</td>
                          <td>$92,575</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Gloria Little</td>
                          <td>Systems Administrator</td>
                          <td>New York</td>
                          <td>59</td>
                          <td>2009/04/10</td>
                          <td>$237,500</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Haley Kennedy</td>
                          <td>Senior Marketing Designer</td>
                          <td>London</td>
                          <td>43</td>
                          <td>2012/12/18</td>
                          <td>$313,500</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Hermione Butler</td>
                          <td>Regional Director</td>
                          <td>London</td>
                          <td>47</td>
                          <td>2011/03/21</td>
                          <td>$356,250</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Herrod Chandler</td>
                          <td>Sales Assistant</td>
                          <td>San Francisco</td>
                          <td>59</td>
                          <td>2012/08/06</td>
                          <td>$137,500</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Hope Fuentes</td>
                          <td>Secretary</td>
                          <td>San Francisco</td>
                          <td>41</td>
                          <td>2010/02/12</td>
                          <td>$109,850</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Howard Hatfield</td>
                          <td>Office Manager</td>
                          <td>San Francisco</td>
                          <td>51</td>
                          <td>2008/12/16</td>
                          <td>$164,500</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Jackson Bradshaw</td>
                          <td>Director</td>
                          <td>New York</td>
                          <td>65</td>
                          <td>2008/09/26</td>
                          <td>$645,750</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Jena Gaines</td>
                          <td>Office Manager</td>
                          <td>London</td>
                          <td>30</td>
                          <td>2008/12/19</td>
                          <td>$90,560</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Jenette Caldwell</td>
                          <td>Development Lead</td>
                          <td>New York</td>
                          <td>30</td>
                          <td>2011/09/03</td>
                          <td>$345,000</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Jennifer Acosta</td>
                          <td>Junior Javascript Developer</td>
                          <td>Edinburgh</td>
                          <td>43</td>
                          <td>2013/02/01</td>
                          <td>$75,650</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Jennifer Chang</td>
                          <td>Regional Director</td>
                          <td>Singapore</td>
                          <td>28</td>
                          <td>2010/11/14</td>
                          <td>$357,650</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Jonas Alexander</td>
                          <td>Developer</td>
                          <td>San Francisco</td>
                          <td>30</td>
                          <td>2010/07/14</td>
                          <td>$86,500</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Lael Greer</td>
                          <td>Systems Administrator</td>
                          <td>London</td>
                          <td>21</td>
                          <td>2009/02/27</td>
                          <td>$103,500</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Martena Mccray</td>
                          <td>Post-Sales support</td>
                          <td>Edinburgh</td>
                          <td>46</td>
                          <td>2011/03/09</td>
                          <td>$324,050</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Michael Bruce</td>
                          <td>Javascript Developer</td>
                          <td>Singapore</td>
                          <td>29</td>
                          <td>2011/06/27</td>
                          <td>$183,000</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Michael Silva</td>
                          <td>Marketing Designer</td>
                          <td>London</td>
                          <td>66</td>
                          <td>2012/11/27</td>
                          <td>$198,500</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Michelle House</td>
                          <td>Integration Specialist</td>
                          <td>Sidney</td>
                          <td>37</td>
                          <td>2011/06/02</td>
                          <td>$95,400</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Olivia Liang</td>
                          <td>Support Engineer</td>
                          <td>Singapore</td>
                          <td>64</td>
                          <td>2011/02/03</td>
                          <td>$234,500</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Paul Byrd</td>
                          <td>Chief Financial Officer (CFO)</td>
                          <td>New York</td>
                          <td>64</td>
                          <td>2010/06/09</td>
                          <td>$725,000</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Prescott Bartlett</td>
                          <td>Technical Author</td>
                          <td>London</td>
                          <td>27</td>
                          <td>2011/05/07</td>
                          <td>$145,000</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Quinn Flynn</td>
                          <td>Support Lead</td>
                          <td>Edinburgh</td>
                          <td>22</td>
                          <td>2013/03/03</td>
                          <td>$342,000</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Rhona Davidson</td>
                          <td>Integration Specialist</td>
                          <td>Tokyo</td>
                          <td>55</td>
                          <td>2010/10/14</td>
                          <td>$327,900</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Sakura Yamamoto</td>
                          <td>Support Engineer</td>
                          <td>Tokyo</td>
                          <td>37</td>
                          <td>2009/08/19</td>
                          <td>$139,575</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Serge Baldwin</td>
                          <td>Data Coordinator</td>
                          <td>Singapore</td>
                          <td>64</td>
                          <td>2012/04/09</td>
                          <td>$138,575</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Shad Decker</td>
                          <td>Regional Director</td>
                          <td>Edinburgh</td>
                          <td>51</td>
                          <td>2008/11/13</td>
                          <td>$183,000</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Shou Itou</td>
                          <td>Regional Marketing</td>
                          <td>Tokyo</td>
                          <td>20</td>
                          <td>2011/08/14</td>
                          <td>$163,000</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Sonya Frost</td>
                          <td>Software Engineer</td>
                          <td>Edinburgh</td>
                          <td>23</td>
                          <td>2008/12/13</td>
                          <td>$103,600</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Suki Burks</td>
                          <td>Developer</td>
                          <td>London</td>
                          <td>53</td>
                          <td>2009/10/22</td>
                          <td>$114,500</td>
                        </tr><tr role="row" class="odd">
                          <td class="sorting_1">Tatyana Fitzpatrick</td>
                          <td>Regional Director</td>
                          <td>London</td>
                          <td>19</td>
                          <td>2010/03/17</td>
                          <td>$385,750</td>
                        </tr><tr role="row" class="even">
                          <td class="sorting_1">Thor Walton</td>
                          <td>Developer</td>
                          <td>New York</td>
                          <td>61</td>
                          <td>2013/08/11</td>
                          <td>$98,540</td>
                        </tr></tbody>
                      </table>
                    </div>
                  </div>
                  <div class="row">
                    &nbsp;&nbsp;导出：
                    
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- /page content -->

        <!-- footer content -->
        <?php include 'footer.php';?>
        <!-- /footer content -->
      </div>
    </div>

    <!-- jQuery -->
    <script src="./vendors/jquery/dist/jquery.min.js"></script>
    <!-- Bootstrap -->
    <script src="./vendors/bootstrap/dist/js/bootstrap.min.js"></script>
    <!-- Datatables -->
    <script src="./vendors/datatables.net/js/jquery.dataTables.min.js"></script>
    <script src="./vendors/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>
    <script src="./vendors/datatables.net-buttons/js/dataTables.buttons.min.js"></script>
    <script src="./vendors/datatables.net-buttons-bs/js/buttons.bootstrap.min.js"></script>
    <script src="./vendors/datatables.net-buttons/js/buttons.flash.min.js"></script>
    <script src="./vendors/datatables.net-buttons/js/buttons.html5.min.js"></script>
    <script src="./vendors/datatables.net-buttons/js/buttons.print.min.js"></script>
    <script src="./vendors/datatables.net-fixedheader/js/dataTables.fixedHeader.min.js"></script>
    <script src="./vendors/datatables.net-keytable/js/dataTables.keyTable.min.js"></script>
    <script src="./vendors/datatables.net-responsive/js/dataTables.responsive.min.js"></script>
    <script src="./vendors/datatables.net-responsive-bs/js/responsive.bootstrap.js"></script>
    <script src="./vendors/datatables.net-scroller/js/datatables.scroller.min.js"></script>
    <script src="./vendors/jszip/dist/jszip.min.js"></script>
    <script src="./vendors/pdfmake/build/pdfmake.min.js"></script>
    <script src="./vendors/pdfmake/build/vfs_fonts.js"></script>

    <!-- Custom Theme Scripts -->
    <script src="./build/js/custom.min.js"></script>

    <!-- Sample Coverage Scripts -->
    <script src="js/querydblab.js"></script>

    <!-- Datatables -->
    <script>
      $(document).ready(function() {
        var handleDataTableButtons = function() {
          if ($("#datatable-buttons").length) {
            $("#datatable-buttons").DataTable({
              dom: "Bfrtip",
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

        $('#datatable').DataTable();
        $('#datatable-keytable').DataTable({
          keys: true
        });

        $('#datatable-responsive').DataTable();

        $('#datatable-scroller').DataTable({
          ajax: "js/datatables/json/scroller-demo.json",
          deferRender: true,
          scrollY: 380,
          scrollCollapse: true,
          scroller: true
        });

        var table = $('#datatable-fixed-header').DataTable({
          fixedHeader: true
        });

        TableManageButtons.init();
      });
    </script>
    <!-- /Datatables -->
  </body>
</html>
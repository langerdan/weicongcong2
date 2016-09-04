<!DOCTYPE html>
<!--
 * PAGE     : sap_comp_qc_sd
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : September 4 2016
 * VERSION  : v0.0.1a
-->
<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <!-- Meta, title, CSS, favicons, etc. -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>多样本比较</title>

    <!-- Bootstrap -->
    <link href="./vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="./vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
    <!-- Datatables -->
    <link href="./vendors/datatables.net-bs/css/dataTables.bootstrap.min.css" rel="stylesheet">
    <link href="./vendors/datatables.net-buttons-bs/css/buttons.bootstrap.min.css" rel="stylesheet">

    <!-- Custom Theme Style -->
    <link href="./build/css/custom.min.css" rel="stylesheet">

  </head>
  <body class="nav-md">
    <div class="row">
      <div class="col-md-12 col-sm-12 col-xs-12">
        <div>
          <ul id="sdp_url" style="display: none;">
            <?php
              $query = null;

              switch ($_SERVER['REQUEST_METHOD']) {
                  case 'GET':
                      $query = $_GET;
                      break;
                  case 'POST':
                      $query = $_POST;
                      break;
              }

              foreach ($query as $key => $value) {
                echo "<li>".$value."</li>";
              }
            ?>
          </ul>
        </div>

        <div class="x_panel">
          <div class="x_title">
            <h2>概览</h2>
            <div class="clearfix"></div>
          </div>
          <div class="x_content">
            <table id="datatable_general" class="table table-striped table-bordered jambo_table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>样本名称</th>
                  <th>PASS</th>
                  <th>回帖reads数</th>
                  <th>回帖reads百分比</th>
                  <th>目标区段reads数</th>
                  <th>目标区段reads百分比</th>
                  <th>平均深度</th>
                  <th>最大深度</th>
                  <th>最小深度</th>
                </tr>
              </thead>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 col-sm-12 col-xs-12">
        <div class="x_panel">
          <div class="x_title">
            <h2>目标碱基覆盖度</h2>
            <div class="clearfix"></div>
          </div>
          <div class="x_content">
            <table id="datatable_sample_depth_level" class="table table-striped table-bordered jambo_table">
            </table>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 col-sm-12 col-xs-12">
        <div class="x_panel">
          <div class="x_title">
            <h2>0x片段统计</h2>
            <div class="clearfix"></div>
          </div>
          <div class="x_content">
            <table id="datatable_0x_frag" class="table table-striped table-bordered jambo_table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>片段名称</th>
                  <th>频数</th>
                  <th>详细</th>
                </tr>
              </thead>
            </table>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row">
      <div class="col-md-12 col-sm-12 col-xs-12">
        <div class="x_panel">
          <div class="x_title">
            <h2>缺失片段统计</h2>
            <div class="clearfix"></div>
          </div>
          <div class="x_content">
            <table id="datatable_absent_frag" class="table table-striped table-bordered jambo_table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>片段名称</th>
                  <th>频数</th>
                  <th>详细</th>
                </tr>
              </thead>
            </table>
          </div>
        </div>
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
    <script src="./vendors/jszip/dist/jszip.min.js"></script>
    <script src="./vendors/pdfmake/build/pdfmake.min.js"></script>
    <script src="./vendors/pdfmake/build/vfs_fonts.js"></script>
  
    <!-- Custom Theme Scripts -->
    <script src="./build/js/custom.min-qc_report.js"></script>

    <script type="text/javascript">
      var sdp_url = $("#sdp_url li");
      var sdp_list = new Array();
      for (var i = 0; i < sdp_url.length; i ++) {
        var url = $("#sdp_url li:eq(" + i + ")").text();
        var json = JSON.parse($.ajax({url: url,async: false}).responseText);
        sdp_list.push(json);
      }

      document.getElementById("datatable_sample_depth_level").innerHTML = loadDLthead(sdp_list[0].depth_level, "样本名称");

      var export_filename_g = "多样本比较-概览";
      if ($.fn.dataTable.isDataTable('#datatable_general')) {
          dt_g.destroy();
      }
      dt_g = $("#datatable_general").DataTable( {
          data: getSapGeneral(sdp_list),
          dom: "lfrtipB",
          buttons: [
              {
                  extend: "copy",
                  className: "btn-sm"
              },
              {
                  extend: "csv",
                  className: "btn-sm",
                  title: export_filename_g
              },
              {
                  extend: "excel",
                  className: "btn-sm",
                  title: export_filename_g
              },
              {
                  extend: "pdfHtml5",
                  className: "btn-sm",
                  title: export_filename_g
              },
              {
                  extend: "print",
                  className: "btn-sm",
                  title: export_filename_g
                  },
              ],
              responsive: true
      });

      var export_filename_sdl = "多样本比较-目标碱基覆盖度";
      if ($.fn.dataTable.isDataTable('#datatable_sample_depth_level')) {
          dt_sdl.destroy();
      }
      dt_sdl = $("#datatable_sample_depth_level").DataTable( {
          data: getSapDL(sdp_list),
          drawCallback: function(settings) {
              var td_obj = $("#datatable_sample_depth_level td");
              for (var i = 0; i < td_obj.length; i ++) {
                  var cell = $("#datatable_sample_depth_level td:eq(" + i + ")");
                  var patt = /^[\d.]+%$/;
                  if (patt.test(cell.text())) {
                      var percent = cell.text().replace(/%/, "");
                      cell.css("background-color", getHeatColor(percent));
                  }
              }
          },
          dom: "lfrtipB",
          buttons: [
              {
                  extend: "copy",
                  className: "btn-sm"
              },
              {
                  extend: "csv",
                  className: "btn-sm",
                  title: export_filename_sdl
              },
              {
                  extend: "excel",
                  className: "btn-sm",
                  title: export_filename_sdl
              },
              {
                  extend: "pdfHtml5",
                  className: "btn-sm",
                  title: export_filename_sdl
              },
              {
                  extend: "print",
                  className: "btn-sm",
                  title: export_filename_sdl
                  },
              ],
              responsive: true
      });

      var export_filename_abfrag = "多样本比较-缺失片段统计";
      if ($.fn.dataTable.isDataTable('#datatable_absent_frag')) {
          dt_abfrag.destroy();
      }
      dt_abfrag = $("#datatable_absent_frag").DataTable( {
          data: getFragStat(sdp_list, "absent_frag"),
          dom: "lfrtipB",
          order: [[2, 'des']],
          buttons: [
              {
                  extend: "copy",
                  className: "btn-sm"
              },
              {
                  extend: "csv",
                  className: "btn-sm",
                  title: export_filename_abfrag
              },
              {
                  extend: "excel",
                  className: "btn-sm",
                  title: export_filename_abfrag
              },
              {
                  extend: "pdfHtml5",
                  className: "btn-sm",
                  title: export_filename_abfrag
              },
              {
                  extend: "print",
                  className: "btn-sm",
                  title: export_filename_abfrag
                  },
              ],
              responsive: true
      });

      var export_filename_0xfrag = "多样本比较-0x片段统计";
      if ($.fn.dataTable.isDataTable('#datatable_0x_frag')) {
          dt_0xfrag.destroy();
      }
      dt_0xfrag = $("#datatable_0x_frag").DataTable( {
          data: getFragStat(sdp_list, "0x_frag"),
          dom: "lfrtipB",
          order: [[2, 'des']],
          buttons: [
              {
                  extend: "copy",
                  className: "btn-sm"
              },
              {
                  extend: "csv",
                  className: "btn-sm",
                  title: export_filename_0xfrag
              },
              {
                  extend: "excel",
                  className: "btn-sm",
                  title: export_filename_0xfrag
              },
              {
                  extend: "pdfHtml5",
                  className: "btn-sm",
                  title: export_filename_0xfrag
              },
              {
                  extend: "print",
                  className: "btn-sm",
                  title: export_filename_0xfrag
                  },
              ],
              responsive: true
      });

      function loadDLthead(data, col_1_name) {
          table_head = "<thead><tr><th>序号</th><th>" + col_1_name + "</th>";
          for  (var i in data) {
              if (data[i][0] == 0) {
                  table_head += "<th> >" + data[i][0] + " </th>";
              }else {
                  table_head += "<th> ≥" + data[i][0] + " </th>";
              }
          }
          table_head += "</tr></thead>";
          return table_head;
      }

      function getSapGeneral(sdp_list) {
        var data = new Array();
        for (var i = 0; i < sdp_list.length; i ++) {
          var per_mapped_reads = Math.floor((sdp_list[i].mapped_reads / sdp_list[i].total_reads) * 10000) / 100 + '%';
          var per_target_reads = Math.floor((sdp_list[i].target_reads / sdp_list[i].total_reads) * 10000) / 100 + '%';

          var pass;
          if (sdp_list[i].pass.ALL) {
            pass = "<strong style=\"color: green\">PASS</strong>";
          }else {
            pass = "<strong style=\"color: red\">FAILED</strong>";
          }
          data.push([i+1, sdp_list[i].sample_name, pass, sdp_list[i].mapped_reads, per_mapped_reads, sdp_list[i].target_reads, per_target_reads, sdp_list[i].aver_depth, sdp_list[i].max_depth, sdp_list[i].min_depth])
        }
        return data;
      }

      function getSapDL(sdp_list) {
        var data = new Array();
        for (var i = 0; i < sdp_list.length; i ++) {
          var row = new Array();
          row.push(i+1);
          row.push(sdp_list[i].sample_name);
          var dl = sdp_list[i].depth_level;
          for (var j = 0; j < dl.length; j ++) {
            row.push(dl[j][1] + "%");
          }
          data.push(row);
        }
        return data;
      }

      function getFragStat(sdp_list, attr) {
        var data = new Array();
        var frag_num = new Array();
        var frag_sap = new Array();
        for (var i = 0; i < sdp_list.length; i ++) {
          var x_frag = sdp_list[i][attr];
          var sap_n = sdp_list[i].sample_name;
          for (var key in x_frag) {
            if (!frag_num.hasOwnProperty(key)) {
              frag_num[key] = 1;
            }else {
              frag_num[key] ++;
            }
            if (!frag_sap.hasOwnProperty(key)) {
              frag_sap[key] = new Array();
              frag_sap[key].push(sap_n);
            }else {
              frag_sap[key].push(sap_n);
            }
          }
        }
        var i = 0;
        for (var key in frag_num) {
          var details = "";
          for (var j = 0; j < frag_sap[key].length; j ++) {
            details += frag_sap[key][j] + " / ";
          }
          data.push([i+1, key, frag_num[key], details]);
          i ++;
        }
        return data;
      }

      function getHeatColor(percent) {
          var h= percent / 100 * 90 / 360;
          var s = 0.9;
          var l = 0.5;
          var rgb = HSLtoRGB(h, s, l);
          return RGBToHex(rgb.r, rgb.g, rgb.b);
      }

      function HSLtoRGB(h, s, l){
          var r, g, b;

          if(s == 0){
              r = g = b = l; // achromatic
          }else{
              var hue2rgb = function hue2rgb(p, q, t){
                  if(t < 0) t += 1;
                  if(t > 1) t -= 1;
                  if(t < 1/6) return p + (q - p) * 6 * t;
                  if(t < 1/2) return q;
                  if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
                  return p;
              }
              var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
              var p = 2 * l - q;
              r = hue2rgb(p, q, h + 1/3);
              g = hue2rgb(p, q, h);
              b = hue2rgb(p, q, h - 1/3);
          }
          return {
              r: Math.round(r * 255),
              g: Math.round(g * 255),
              b: Math.round(b * 255)
          };
      }

      function RGBToHex(r, g, b) {
          function componentToHex(c) {
              var hex = c.toString(16);
              return hex.length == 1 ? "0" + hex : hex;
          }
          return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
      }
    </script>
  </body>
</html>
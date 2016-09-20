<!DOCTYPE html>
<!-- 
 * PAGE     : tools_sam_flag_decode
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : September 13 2016
 * VERSION  : v0.0.1a
-->
<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <!-- Meta, title, CSS, favicons, etc. -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>工具 － SAM FLAG decode</title>

    <!-- Bootstrap -->
    <link href="./vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="./vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
    <!-- iCheck -->
    <link href="./vendors/iCheck/skins/flat/green.css" rel="stylesheet">
    <!-- PNotify -->
    <link href="./vendors/pnotify/dist/pnotify.css" rel="stylesheet">

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
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2>SAM FLAG decode</h2>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="col-md-12 col-sm-12 col-xs-12 input-group">
                    SAM FLAG : <input id="sam_flag_sum" type="text">&nbsp;&nbsp;
                    <button class="btn btn-primary" onclick="explainFlags();"> Decode </button>
                  </div>

                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="container">
                      <div id="explanation" class="well"></div>
                    </div>
                  </div>

                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <table  class="table table-bordered jambo_table">
                      <thead>
                        <tr>
                          <th>选择</th>
                          <th>十六进制</th>
                          <th>十进制</th>
                          <th>释义</th>
                          <th>SAMv1 参考</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=1></th>
                          <th>0x1</th>
                          <th>1</th>
                          <th>segments是成对的</th>
                          <th>template having multiple segments in sequencing</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=2></th>
                          <th>0x2</th>
                          <th>2</th>
                          <th>两条segments都在预期的insert/delete大小内被正确地贴上</th>
                          <th>each segment properly aligned according to the aligner</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=4></th>
                          <th>0x4</th>
                          <th>4</th>
                          <th>此条segment未被贴上</th>
                          <th>segment unmapped</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=8></th>
                          <th>0x8</th>
                          <th>8</th>
                          <th>另一条segment未被贴上</th>
                          <th>next segment in the template unmapped</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=10></th>
                          <th>0x10</th>
                          <th>16</th>
                          <th>此条segment的序列被反向(-)贴上</th>
                          <th>SEQ being reverse complemented</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=20></th>
                          <th>0x20</th>
                          <th>32</th>
                          <th>另一条segment的序列被反向(-)贴上</th>
                          <th>SEQ of the next segment in the template being reverse complemented</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=40></th>
                          <th>0x40</th>
                          <th>64</th>
                          <th>此条segment是pair中的第一个</th>
                          <th>the first segment in the template</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=80></th>
                          <th>0x80</th>
                          <th>128</th>
                          <th>此条segment是pair中的第二个</th>
                          <th>the last segment in the template</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=100></th>
                          <th>0x100</th>
                          <th>256</th>
                          <th>次优回帖</th>
                          <th>secondary alignment</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=200></th>
                          <th>0x200</th>
                          <th>512</th>
                          <th>未通过QC</th>
                          <th>not passing filters, such as platform/vendor quality controls</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=400></th>
                          <th>0x400</th>
                          <th>1024</th>
                          <th>重复</th>
                          <th>PCR or optical duplicate</th>
                        </tr>
                        <tr>
                          <th><input type="checkbox" class="flat" name="sam_flag_bit" value=800></th>
                          <th>0x800</th>
                          <th>2048</th>
                          <th>补充回帖</th>
                          <th>supplementary alignment</th>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <div class="col-md-12 col-sm-12 col-xs-12 well">
                    <h4><strong>参考：</strong></h4>
                    <p>
                      <cite>[1]. <a href="https://broadinstitute.github.io/picard/explain-flags.html" target="_blank">Explain SAM Flags</a></cite>
                      <br />
                      <span style="padding-left:2em">SAM FLAG Decode 工具思路来源</span>
                    </p>

                    <p>
                      <cite>[2]. <a href="https://samtools.github.io/hts-specs/SAMv1.pdf" target="_blank">Sequence Alignment/Map Format Specification</a></cite>
                      <br />
                      <span style="padding-left:2em">SAM/BAM格式官方文档</span>
                    </p>

                    <p>
                      <cite>[3]. <a href="https://ppotato.wordpress.com/2010/08/25/samtool-bitwise-flag-paired-reads/" target="_blank">SAMtool bitwise flag meaning explained: how to understand samflags without pains | A Pillow Diary of an Expatriate Scientist</a></cite>
                      <br />
                      <span style="padding-left:2em">详细解释了map/unmap(0x4, 0x8)，forward/reverse(0x16, 0x32)，pair(0x1)等bit位</span>
                    </p>

                    <p>
                      <cite>[4]. <a href="http://www.htslib.org/doc/samtools.html" target="_blank">samtools manual page - flagstat</a></cite>
                      <br />
                      <span style="padding-left:2em">解释了QC flag(0x200)bit位</span>
                    </p>

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
    <!-- iCheck -->
    <script src="./vendors/iCheck/icheck.min.js"></script>
    <!-- PNotify -->
    <script src="./vendors/pnotify/dist/pnotify.js"></script>

    <!-- Custom Theme Scripts -->
    <script src="./build/js/custom.min.js"></script>
    
    <script type="text/javascript">
      var flagfalse = [
        [0x1, ""],
        [0x2, ""],
        [0x4, "此条segment被贴上"],
        [0x8, "另一条segment被贴上"],
        [0x10, "此条segment的序列被正向(+)贴上"],
        [0x20, "另一条segment的序列被正向(+)贴上"],
        [0x40, ""],
        [0x80, ""],
        [0x100, ""],
        [0x200, ""],
        [0x400, ""],
        [0x800, ""]
      ];

      function explainFlags() {
        var flag_val = $("#sam_flag_sum").val();
        if (/[^\d]/.test(flag_val) || parseInt(flag_val) >= 4096) {
          new PNotify({
            title: '请填写正确地SAM FLAG！(范围0～4095)',
            type: 'error',
            hide: false,
            styling: 'bootstrap3'
            });
        }else {
          var flag = parseInt(flag_val);
          var cb = $("input[name='sam_flag_bit']");
          for (var i = 0; i < cb.length; i++) {
            var cb_i = $("input[name='sam_flag_bit']:eq(" + i + ")");
            if (flag & flagfalse[i][0]) {
              cb_i.iCheck("check");
            }else {
              cb_i.iCheck("uncheck");
            }
          }
          showSum();
        }
      }

      function showSum() {
        var flag = 0;
        var exp = "";
        var cb = $("input[name='sam_flag_bit']");
        for (var i = 0; i < cb.length; i++) {
          var cb_i = $("input[name='sam_flag_bit']:eq(" + i + ")");
          var style = "";
          if (cb_i.is(":checked")) {
            if ([2, 3, 4, 5, 9].indexOf(i) >= 0) style = "style=\"color: red\"";
            exp += "<p " + style + ">" + cb_i.parent().parent().siblings("th:eq(2)").text() + "</p>";
            flag += flagfalse[i][0];
          }else {
            if ([2, 3, 4, 5].indexOf(i) >= 0) {
              style = "style=\"color: green\"";
              exp += "<p " + style + ">" + flagfalse[i][1] + "</p>";
            }else if ((i == 4 && !$("input[name='sam_flag_bit']:eq(2)").is(":checked")) || (i == 5 && !$("input[name='sam_flag_bit']:eq(3)").is(":checked"))) {
              exp += "<p " + style + ">" + flagfalse[i][1] + "</p>";
            }
          }
        }
        $("#explanation").html(exp);
        return flag;
      }

      $("input[name='sam_flag_bit']").on("ifToggled", function() {
        var flag = showSum();
        $("#sam_flag_sum").val(flag);
      });
    </script>
  </body>
</html>
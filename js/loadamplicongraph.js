/*
 * PROGRAM  : loadAmpliconGraph
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 7 2016
 * VERSION  : v0.0.1a
 */

function loadAmpliconGraph(path_amplicon) {
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
    if ((xhttp.readyState == 4 && xhttp.status == 200)) {
      var json = JSON.parse(xhttp.responseText);

      // update amplicon pass percent
      var percent = Math.round(json.pass / (json.pass + json.failed) * 100 * 10) / 10;
      document.getElementById("amplicon_pass_percent").setAttribute("data-percent", percent);
      document.getElementById("amplicon_pass_num").innerHTML = json.pass + "/" + (json.pass + json.failed);
      document.getElementById("amplicon_chr_num").innerHTML = "<strong>Chr </strong> " + json.chr_num;
      document.getElementById("amplicon_gene").innerHTML = "<strong>基因 : </strong> " + json.gene_name;
      document.getElementById("amplicon_pos").innerHTML = "<strong>位置 : </strong> " + json.pos_s + "-" + json.pos_e;
      document.getElementById("amplicon_len").innerHTML = "<strong>长度 : </strong> " + json.len;
      $('.chart').data('easyPieChart').update(percent);
      
      // create amplicon depth graph controllers

      // draw amplicon depth graph
      var x_labels = new Array(); 
      for (var i = 0, v = json.pos_s + 1; v <= json.pos_e; i++, v++) { 
        x_labels[i] = v;
      }
      //console.log(x_labels);  

      var amplicon_datasets = new Array(); 
      var keys = Object.keys(json.depth); 
      var data_lables_list = keys.sort(); 
      for (var i in data_lables_list) { 
        var r = color_sheet[i].r; 
        var g = color_sheet[i].g; 
        var b = color_sheet[i].b; 
        //console.log("sample " + i + " use color r:" + r + ", g:" + g + ", b:" + b); 
        var each_data = {}; 
        var sample_name = data_lables_list[i]; 
        var sample_data = new Array(); 
        for (var j in json.depth[sample_name]) { 
          sample_data.push(json.depth[sample_name][j].depth); 
        } 
        each_data = { 
          label: sample_name, 
          fill: false, 
          lineTension: 0.05, 
          backgroundColor: "rgba(" + r + "," + g + "," + b + ",0.4)",
          borderColor: "rgba(" + r + "," + g + "," + b + ",1)", 
          borderCapStyle: 'butt',
          borderDash: [],
          borderDashOffset: 0.0, 
          borderJoinStyle: 'miter',
          pointBorderColor: "rgba(" + r + "," + g + "," + b + ",1)",
          pointBackgroundColor: "#fff",
          //pointBorderWidth: 1,
          //pointHoverRadius: 5, 
          pointHoverBackgroundColor: "rgba(" + r + "," + g + "," + b + ",1)", 
          pointHoverBorderColor: "rgba(" + r + "," + g + "," + b + ",1)",
          //pointHoverBorderWidth: 2,
          pointRadius: 1, 
          //pointHitRadius: 10,
          data: sample_data,
          spanGaps: false 
        };
        //console.log(sample_data);
        amplicon_datasets.push(each_data);
      }
      drawAmpliconDepth({labels: x_labels, datasets: amplicon_datasets});
    }
  };
  xhttp.open("GET", path_amplicon, true);
  xhttp.send();
}

function drawAmpliconDepth(data) {
  var ctx = document.getElementById("canvas_amplicon_depth").getContext("2d");
  ctx.canvas.height = 1000;

  var lineChart = new Chart(ctx, {
    type: 'line',
    data: data,
    option: {
      responsive:false,
      maintainAspectRatio: false
    }
  });
}

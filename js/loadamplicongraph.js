/* 
 * PROGRAM  : loadAmpliconGraph
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 7 2016
 * VERSION  : v0.0.1a
 */

function loadAmpliconGraph(path_amplicon) {
  // parse amplicon data
  var amplicon_details;
  var x_lables;
  var data_lables_list;
  var data_list;
  var graph_data;
  
  // test
  var data = {
    labels: x_lables,
    datasets: [
        {
            label: "My First dataset",
            fill: false,
            lineTension: 0.05,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: [65, 59, 80, 81, 56, 55, 40],
            spanGaps: false,
        }
    ]
}; 
  
  // update amplicon pass percent
  
  // create amplicon depth graph controllers
  
  // draw amplicon depth graph
  drawAmpliconDepth(data);
}

function drawAmpliconDepth(data) {
  var ctx = document.getElementById("canvas_amplicon_depth");
    var lineChart = new Chart(ctx, {
      type: 'line',
      data: data,
    });
}
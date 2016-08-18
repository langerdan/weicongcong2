/**
 * PROGRAM    : loadAmpliconData
 * PURPOSE    :
 * AUTHOR     : codeunsolved@gmail.com
 * CREATED    : August 6 2016
 * VERSION    : v0.0.1a
 */

var color_sheet = new Array();

function dynamicColors() {
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return {"r": r, "g": g, "b": b};
}

function loadData(dir_name) {
    var path_pointer = "data/" + dir_name + "/amplicon/data_pointer.json";
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var json = JSON.parse(xhttp.responseText);
            //console.log(json);
            document.getElementById("data_name").innerHTML = dir_name;
            document.getElementById("sample_num").innerHTML = json.sample_num;
            document.getElementById("amplicon_num").innerHTML = json.amplicon_num;
            loadTable(json.amplicon_data);
            
            // create color sheet by sample number
            for (var i = 0; i < json.sample_num; i ++) {
                color_sheet.push(dynamicColors());
            }
        }
    };
    xhttp.open("GET", path_pointer, true);
    xhttp.send();
}

function loadTable(data_list) {
    var table_body = "<tbody>";
    var col_i = 1;
    var col_limit = 7;
    for (var i in data_list) {
        var each_amplicon = data_list[i];
        //console.log(each_amplicon);
        if (col_i == 1) {
            table_body += "<tr>";
        }else if (col_i == col_limit) {
            table_body += "</tr>";
            col_i = 1;
        }
        table_body += "<td ";
        var pass_percent = each_amplicon.pass/(each_amplicon.pass+each_amplicon.failed)*100;
        //console.log(pass_percent);
        if (pass_percent == 100) {
            // pass
            table_body += "style=\"background-color: #26B99A;\">";
        }else if (70 <= pass_percent && pass_percent < 100) {
            // warning
            table_body += "style=\"background-color: #FFFF66;\">";
        }else if (pass_percent < 70) {
            // failed
            table_body += "style=\"background-color: #E74C3C;\">";
        }
        table_body += "<a href=\"#\" onclick=\"loadAmpliconGraph('" + each_amplicon.path + "');return false;\">" + each_amplicon.name + "-" + Math.round(pass_percent * 10) / 10 + "%</a></td>";
        col_i ++;
    }
    table_body += "</tr></tbody>";
    document.getElementById("amplicon_pass_table").innerHTML = table_body;
}

function loadAmpliconGraph(path_amplicon) {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if ((xhttp.readyState == 4 && xhttp.status == 200)) {
            var json = JSON.parse(xhttp.responseText);

            // update amplicon pass percent
            var percent = Math.round(json.pass / (json.pass + json.failed) * 100 * 10) / 10;
            //document.getElementById("amplicon_pass_percent").setAttribute("data-percent", percent);
            document.getElementById("amplicon_pass_num").innerHTML = json.pass + "/" + (json.pass + json.failed);
            document.getElementById("amplicon_chr_num").innerHTML = "<strong>Chr </strong> " + json.chr_num;
            document.getElementById("amplicon_gene").innerHTML = "<strong>基因 : </strong> " + json.gene_name;
            document.getElementById("amplicon_pos").innerHTML = "<strong>位置 : </strong> " + json.pos_s + " - " + json.pos_e;
            document.getElementById("amplicon_len").innerHTML = "<strong>长度 : </strong> " + json.len;
            $('.chart').data('easyPieChart').update(percent);
            
            // create amplicon depth graph controllers

            // draw amplicon depth graph
            var x_labels = new Array();
            for (var i = 0, v = json.pos_s + 1; v <= json.pos_e; i++, v++) {
                x_labels[i] = v;
            }
            //console.log(x_labels);

            var graph_datasets = new Array();
            var keys = Object.keys(json.depth);
            var data_lables_list = keys.sort();
            for (var i in data_lables_list) {
                var r = color_sheet[i].r;
                var g = color_sheet[i].g;
                var b = color_sheet[i].b;
                //console.log("sample " + i + " use color r:" + r + ", g:" + g + ", b:" + b);
                var sample_data = {};
                var sample_name = data_lables_list[i];
                var y_data = new Array();
                for (var j in json.depth[sample_name]) {
                    y_data.push(json.depth[sample_name][j].depth);
                }
                sample_data = {
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
                    data: y_data,
                    spanGaps: false
                };
                //console.log(y_data);
                graph_datasets.push(sample_data);
            }
            drawAmpliconDepth({labels: x_labels, datasets: graph_datasets});
        }
    };
    xhttp.open("GET", path_amplicon, true);
    xhttp.send();
}

function drawAmpliconDepth(data) {
    var ctx = document.getElementById("canvas_amplicon_depth").getContext("2d");

    var lineChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}
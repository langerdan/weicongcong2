/**
 * PROGRAM  : QC_loadAmpliconData
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 6 2016
 * VERSION  : v0.0.1a
 */

var color_sheet = new Array();
var sample_cover;
var lineChart;  // lineChart needs to be global to clear/destroy it before next rendering

function dynamicColors() {
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return {"r": r, "g": g, "b": b};
}

function getHeatColor(percent) {
    var r, g, b;
    if (percent > 50) {
        r= Math.floor(6 + (((255 - 6) / 50) * (100 - percent)));
        g = Math.floor(170 + (((255 - 170) / 50) * (100 - percent)));
        b = Math.floor(60 + (((255 - 60) / 50) * (100 - percent)));
    }else {
        percent = 100 - (100 - percent) % 50;
        r= Math.floor(255 + (((232 - 255) / 50) * (100 - percent)));
        g = Math.floor(255 + (((9 - 255) / 50) * (100 - percent)));
        b = Math.floor(255 + (((26 - 255) / 50) * (100 - percent)));
    }
    return RGBToHex(r, g, b);
}

function HSVtoRGB(h, s, v) {
    var r, g, b, i, f, p, q, t;
    if (arguments.length === 1) {
        s = h.s, v = h.v, h = h.h;
    }
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
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

function loadData(dir_name) {
    var path_pointer = "data/" + dir_name + "/sample_cover/data_pointer.json";
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var json = JSON.parse(xhttp.responseText);
            //console.log(json);
            document.getElementById("data_name").innerHTML = dir_name;
            document.getElementById("sample_num").innerHTML = json.sample_num;
            document.getElementById("frag_num").innerHTML = json.frag_num;

            sample_cover = json.sample_cover;
            loadSampleCoverTable(json.sample_cover);
            //loadSampleCoverGraph(json.sample_cover);
            // create color sheet by sample number
            for (var i = 0; i < json.sample_num; i ++) {
                color_sheet.push(dynamicColors());
            }
        }
    };
    xhttp.open("GET", path_pointer, true);
    xhttp.send();
}

function loadSampleCoverTable() {
    var table_body = "<tbody>";
    for (var i in sample_cover) {
        var each_sample = sample_cover[i];
        //console.log(each_sample);
        if (i == 0) {
            table_body += "<tr><th> 样本名称 </th>";
            for (var m in each_sample.depth_level) {
                if (each_sample.depth_level[m][0] == 0) {
                    table_body += "<th> =" + each_sample.depth_level[m][0] + " </th>";
                }else {
                    table_body += "<th> ≥" + each_sample.depth_level[m][0] + " </th>";
                }
            }
            table_body += "</tr></thead>";
        }
        table_body += "<tr><td><a href=\"#\" onclick=\"loadSampleDataPointer('" + each_sample.path + "');return false;\">" + each_sample.sample_name + "</a></td>";
        for (var j in each_sample.depth_level) {
            var percent = each_sample.depth_level[j][1];
            if (each_sample.depth_level[j][0] == 0){
                table_body += "<td style=\"background-color: " + getHeatColor(percent) + ";\"> " + Math.floor((100 - percent) * 100) / 100 + "% </td>";
            }else {
                table_body += "<td style=\"background-color: " + getHeatColor(percent) + ";\"> " + percent + "% </td>";
            }
        }
        table_body += "</tr>"
    }
    table_body += "</tbody>";
    document.getElementById("sample_cover_table").innerHTML = table_body;
}

function loadSampleCoverGraph() {
    var x_labels = new Array();
    var graph_datasets = new Array();
    var options = {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        max: 100,
                        min: 0,
                        stepSize: 10
                    }
                }]
            }
        };

    for (var i in sample_cover) {
        var r = color_sheet[i].r;
        var g = color_sheet[i].g;
        var b = color_sheet[i].b;

        var each_sample = sample_cover[i];
        var y_data = new Array();
        for (var j in each_sample.depth_level) {
            y_data.push(each_sample.depth_level[j][1]);
        }
        graph_data = {
                    label: each_sample.sample_name,
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
        graph_datasets.push(graph_data);
        if (i == 0) {
            for (var m in each_sample.depth_level) {
                x_labels.push("≥" + each_sample.depth_level[m][0]);
            }
        }
    }
    drawGraph("sample_cover_graph", {labels: x_labels, datasets: graph_datasets}, options);
}

function drawGraph(graph_id, graph_data, graph_options) {
    var ctx = document.getElementById(graph_id).getContext("2d");

    if(window.lineChart !== undefined && window.lineChart !== null){
            window.lineChart.destroy();
    }

    window.lineChart = new Chart(ctx, {
        type: 'line',
        data: graph_data,
        options: graph_options
    });
}

function loadSampleDataPointer(path_sdp) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var json = JSON.parse(xhttp.responseText);
            //console.log(json);
            document.getElementById("sample_name").innerHTML = json.sample_name;
            document.getElementById("aver_sample_depth").innerHTML = "<strong>平均深度 :</strong> " + json.aver_depth;
            document.getElementById("cutoff_sample_depth").setAttribute("class", "text-primary");
            document.getElementById("cutoff_sample_depth").innerHTML = "<strong>cutoff深度 :</strong> " + Math.floor(json.aver_depth*0.2 * 100) / 100;
            document.getElementById("max_sample_depth").innerHTML = "<strong>最大深度 :</strong> " + json.max_depth;
            document.getElementById("min_sample_depth").innerHTML = "<strong>最小深度 :</strong> " + json.min_depth;

            loadFragCoverTable(json.frag_cover_list);

            if (json.absent_frag.length == 0) {
                document.getElementById("sample_absent_frag").setAttribute("class", "panel panel-success");
                document.getElementById("sample_absent_frag_heading").innerHTML = "<strong>缺失片段 :</strong> 0";
                document.getElementById("sample_absent_frag_body").innerHTML = "";
            }else {
                document.getElementById("sample_absent_frag").setAttribute("class", "panel panel-danger");
                document.getElementById("sample_absent_frag_heading").innerHTML = "<strong>缺失片段 :</strong> " + json.absent_frag.length;

                var absent_frag_details = "";
                for (var i in json.absent_frag) {
                    absent_frag_details += "<p class=\"text-danger\">" + json.absent_frag[i] + "</p>";
                }
                document.getElementById("sample_absent_frag_body").innerHTML = absent_frag_details;
            }
        }
    };
    xhttp.open("GET", path_sdp, true);
    xhttp.send();
}

function loadFragCoverTable(data_list) {
    var table_body = "<tbody>";
    for (var i in data_list) {
        var each_frag = data_list[i];
        //console.log(each_frag);
        if (i == 0) {
            table_body += "<thead><tr><th><label><input type=\"radio\" name=\"frag_filter\" onclick=\"filterFrag('all')\"> Level All </label></th>";
            for (var n in each_frag.depth_level) {
                table_body += "<th><label><input type=\"radio\" name=\"frag_filter\" onclick=\"filterFrag('" + each_frag.depth_level[n][0] + "')\"> Level " + each_frag.depth_level[n][0] + " </label></th>";
            }
            table_body += "</tr><tr><th> 样本名称 </th>";
            for (var m in each_frag.depth_level) {
                if (each_frag.depth_level[m][0] == 0) {
                    table_body += "<th> =" + each_frag.depth_level[m][0] + " </th>";
                }else {
                    table_body += "<th> ≥" + each_frag.depth_level[m][0] + " </th>";
                }
            }
            table_body += "</thead></tr>"
        }
        table_body += "<tr class=\"" + tagLevel(each_frag.depth_level) + "\"><td><a href=\"#\" onclick=\"loadFragData('" + each_frag.path + "');return false;\">" + each_frag.frag_name + "</a></td>";
        for (var j in each_frag.depth_level) {
            var percent = each_frag.depth_level[j][1];
            if (each_frag.depth_level[j][0] == 0){
                table_body += "<td style=\"background-color: " + getHeatColor(percent) + ";\"> " + Math.floor((100 - percent) * 100) / 100 + "% </td>";
            }else {
                table_body += "<td style=\"background-color: " + getHeatColor(percent) + ";\"> " + percent + "% </td>";
            }
        }
        table_body += "</tr>"
    }
    table_body += "</tbody>";
    document.getElementById("frag_cover_table").innerHTML = table_body;
}

function tagLevel(depth_level) {
    var level_tag = "";
    for (var i in depth_level) {
        if (depth_level[i][1] == 100) {
            continue;
        }else {
            level_tag = "level-" + depth_level[i][0];
            break;
        }
    }
    return "level-all " + level_tag;
}

function filterFrag(l_index) {
    if (l_index != "all") {
        $(".level-all").hide();
        $(".level-" + l_index).show();
    }else {
        $(".level-all").show();
    }
}

function loadFragData(path_fd) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var json = JSON.parse(xhttp.responseText);
            //console.log(json);
            document.getElementById("frag_name").innerHTML = json.frag_name;
            document.getElementById("frag_chr_num").innerHTML = "<strong>Chr :</strong> " + json.chr_num;
            document.getElementById("frag_gene").innerHTML = "<strong>基因 :</strong> " + json.gene_name;
            document.getElementById("frag_pos").innerHTML = "<strong>位置 :</strong> " + json.pos_s + " - " + json.pos_e;
            document.getElementById("frag_len").innerHTML = "<strong>长度 :</strong> " + json.len;
            document.getElementById("aver_frag_depth").innerHTML = "<strong>平均深度 :</strong> " + json.aver_depth;
            document.getElementById("max_frag_depth").innerHTML = "<strong>最大深度 :</strong> " + json.max_depth;
            document.getElementById("min_frag_depth").innerHTML = "<strong>最小深度 :</strong> " + json.min_depth;

            // draw frag depth graph
            var r = color_sheet[0].r;
            var g = color_sheet[0].g;
            var b = color_sheet[0].b;
            var options = {
                responsive: true,
                maintainAspectRatio: false,
            };

            graph_data = [{
                    label: json.frag_name,
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
                    data: json.depths,
                    spanGaps: false
            }];
            drawGraph("frag_cover_graph", {labels: json.x_labels, datasets: graph_data}, options);
        }
    };
    xhttp.open("GET", path_fd, true);
    xhttp.send();
}
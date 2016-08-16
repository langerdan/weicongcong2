/**
 * PROGRAM  : loadAmpliconData
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 6 2016
 * VERSION  : v0.0.1a
 */

var color_sheet = new Array();
var sample_cover;

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
		percent = 100 - (100 - percent) % 51;
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
                table_body += "<th> ≥" + each_sample.depth_level[m][0] + " </th>";
            }
            table_body += "</tr>";
        }
        table_body += "<tr><td><a href=\"#\" onclick=\"loadSampleDataPointer('" + each_sample.path + "');return false;\">" + each_sample.sample_name + "</a></td>";
        for (var j in each_sample.depth_level) {
            var percent = each_sample.depth_level[j][1];
            table_body += "<td style=\"background-color: " + getHeatColor(percent) + ";\"> " + percent + "% </td>";
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
    drawGraph({labels: x_labels, datasets: graph_datasets}, "sample_cover_graph", options);
}

function drawGraph(graph_data, graph_id, graph_options) {
    var ctx = document.getElementById(graph_id).getContext("2d");

    var lineChart = new Chart(ctx, {
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
            document.getElementById("sample_depth_aver").innerHTML = "<strong>平均深度 :</strong> " + json.aver_depth;
            document.getElementById("sample_depth_max").innerHTML = "<strong>最大深度 :</strong> " + json.max_depth;
            document.getElementById("sample_depth_min").innerHTML = "<strong>最小深度 :</strong> " + json.min_depth;

            loadFragCoverTable(json.frag_cover_list);
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
            table_body += "<tr><th> 片段名称 </th>";
            for (var m in each_frag.depth_level) {
                table_body += "<th> ≥" + each_frag.depth_level[m][0] + " </th>";
            }
            table_body += "</tr>";
        }
        table_body += "<tr><td><a href=\"#\" onclick=\"loadFragData('" + each_frag.path + "');return false;\">" + each_frag.frag_name + "</a></td>";
        for (var j in each_frag.depth_level) {
            var percent = each_frag.depth_level[j][1];
            table_body += "<td style=\"background-color: " + getHeatColor(percent) + ";\"> " + percent + "% </td>";
        }
        table_body += "</tr>"
    }
    table_body += "</tbody>";
    document.getElementById("frag_cover_table").innerHTML = table_body;
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
            document.getElementById("frag_depth_aver").innerHTML = "<strong>平均深度 :</strong> " + json.aver_depth;
            document.getElementById("frag_depth_max").innerHTML = "<strong>最大深度 :</strong> " + json.max_depth;
            document.getElementById("frag_depth_min").innerHTML = "<strong>最小深度 :</strong> " + json.min_depth;

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
        	drawGraph({labels: json.x_labels, datasets: graph_data}, "frag_cover_graph", options);
        }
    };
    xhttp.open("GET", path_fd, true);
    xhttp.send();
}
/**
 * PROGRAM  : loadAmpliconData
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 6 2016
 * VERSION  : v0.0.1a
 */

var color_sheet = new Array();

function dynamicColors() {
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return {"r": r, "g": g, "b": b};
}

function getHeatColor(percent) {
    var h= Math.floor((100 - percent) * 120 / 100);
    var s = Math.abs(percent - 50)/50;
    var v = 1;
    var rgb = HSVtoRGB(h, s, v)
    return RGBToHex(rgb.r, rgb.g, rgb.b)
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
            loadSampleCoverTable(json.sample_cover);
            loadSampleCoverGraph(json.sample_cover_list);

            // create color sheet by sample number
            for (var i = 0; i < json.sample_num; i ++) {
                color_sheet.push(dynamicColors());
            }
        }
    };
    xhttp.open("GET", path_pointer, true);
    xhttp.send();
}

function loadSampleCoverTable(data_list) {
    var table_body = "<tbody>";
    for (var i in data_list) {
        var each_sample = data_list[i];
        //console.log(each_sample);
        if (i == 0) {
            table_body += "<tr><th> Sample Name </th>";
            for (var m in each_sample.depth_level) {
                table_body += "<th> ≥" + each_sample.depth_level[m][0] + " </th>";
            }
            table_body += "</tr>";
        }
        table_body += "<tr><td><a href=\"#\" onclick=\"loadFragCoverTable('" + each_sample.path + "');return false;\">" + each_sample.sample_name + "</a></td>";
        for (var j in each_sample.depth_level) {
            var percent = each_sample.depth_level[j][1]*100;
            table_body += "<td style=\"background-color: " + getHeatColor(percent) + ";\"> " + percent + "% </td>";
        }
        table_body += "</tr>"
    }
    table_body += "</tbody>";
    document.getElementById("sample_cover_table").innerHTML = table_body;
}

function loadSampleCoverGraph(data_list) {
    var x_labels = new Array(); 
    var graph_datasets = new Array(); 
    for (var i in data_list) {
        var r = color_sheet[i].r; 
        var g = color_sheet[i].g; 
        var b = color_sheet[i].b; 

        var each_sample = data_list[i];
        var y_data = new Array(); 
        for (var j in each_sample.depth_level) {
            y_data.push(each_sample.depth_level[j][1])*100;
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
    drawGraph({labels: x_labels, datasets: graph_datasets}, "sample_cover_graph")
}

function drawGraph(graph_data, graph_id) {
    var ctx = document.getElementById(graph_id).getContext("2d");
    //ctx.canvas.height = 300;

    var lineChart = new Chart(ctx, {
        type: 'line',
        data: graph_data,
        option: {
            responsive:false,
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
        }
    });
}

function loadFragCoverTable(sample_name) {
    var i = 0;
}
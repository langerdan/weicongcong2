/**
 * PROGRAM  : QC_Report_SD
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : September 1 2016
 * VERSION  : v0.0.1a
 */

function loadReport_QC_SD(sdp) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var json = JSON.parse(xhttp.responseText);

            // pass details
            var pass_details = "";
            if (!json.pass['0x_percent']) {
                pass_details += "<p>0x位点大于1% <strong style=\"color: red\">FAILED</strong></p>";
            }
            if (!json.pass.absent_frag) {
                pass_details += "<p>存在缺失片段 <strong style=\"color: red\">FAILED</strong></p>";
            }
            document.getElementById("pass_details").innerHTML = pass_details;

            // summary
            document.getElementById("sample_name").innerHTML = json.sample_name;
            document.getElementById("num_mapped_reads").innerHTML = json.mapped_reads;
            document.getElementById("per_mapped_reads").innerHTML = Math.floor((json.mapped_reads / json.total_reads) * 10000) / 100 + '%';
            document.getElementById("num_target_reads").innerHTML = json.target_reads;
            document.getElementById("per_target_reads").innerHTML = Math.floor((json.target_reads / json.total_reads) * 10000) / 100 + '%';
            document.getElementById("aver_sample_depth").innerHTML = json.aver_depth;
            document.getElementById("max_sample_depth").innerHTML = json.max_depth;
            document.getElementById("min_sample_depth").innerHTML = json.min_depth;

            // absent frag
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

            document.getElementById("num_target_bp").innerHTML = json.len_bp;
            document.getElementById("sample_depth_level").innerHTML = loadSampleDL(json.depth_level);

            // draw datatable 0x frag
            var export_filename_0xf = getBasename(getDirname(getDirname(getDirname(sdp)))) + "-(" + json.sample_name + ")-0xFRAG";
            if ($.fn.dataTable.isDataTable('#datatable_0x_frag')) {
                dt_0xf.destroy();
            }
            dt_0xf = $("#datatable_0x_frag").DataTable( {
                data: get0xFrag(json, sdp),
                drawCallback: function(settings) {
                    var td_obj = $("#datatable_0x_frag td");
                    for (var i = 0; i < td_obj.length; i ++) {
                        var cell = $("#datatable_0x_frag td:eq(" + i + ")");
                        var patt = /^[\d.]+%$/;
                        if (patt.test(cell.text())) {
                            var percent = cell.text().replace(/%/, "");
                            if (percent >= 1) {
                                cell.css("color", "red");
                            }
                        }
                    }
                },
                order: [[1, 'des']],
                dom: "lfrtipB",
                buttons: [
                    {
                        extend: "copy",
                        className: "btn-sm"
                    },
                    {
                        extend: "csv",
                        className: "btn-sm",
                        title: export_filename_0xf
                    },
                    {
                        extend: "excel",
                        className: "btn-sm",
                        title: export_filename_0xf
                    },
                    {
                        extend: "pdfHtml5",
                        className: "btn-sm",
                        title: export_filename_0xf
                    },
                    {
                        extend: "print",
                        className: "btn-sm",
                        title: export_filename_0xf
                        },
                    ],
                    responsive: true
            });

            document.getElementById("datatable_frag_DL").innerHTML = loadFragCoverTable(json.depth_level);
            // draw datatable frag depth level
            var export_filename_fc = getBasename(getDirname(getDirname(getDirname(sdp)))) + "-(" + json.sample_name + ")-FRAG_COVER";
            if ($.fn.dataTable.isDataTable('#datatable_frag_DL')) {
                dt_fc.destroy();
            }
            dt_fc = $("#datatable_frag_DL").DataTable( {
                data: getFragDL(json.frag_cover_list, sdp),
                drawCallback: function(settings) {
                    var td_obj = $("#datatable_frag_DL td");
                    for (var i = 0; i < td_obj.length; i ++) {
                        var cell = $("#datatable_frag_DL td:eq(" + i + ")");
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
                        title: export_filename_fc
                    },
                    {
                        extend: "excel",
                        className: "btn-sm",
                        title: export_filename_fc
                    },
                    {
                        extend: "pdfHtml5",
                        className: "btn-sm",
                        title: export_filename_fc
                    },
                    {
                        extend: "print",
                        className: "btn-sm",
                        title: export_filename_fc
                        },
                    ],
                    responsive: true
            });
        }
    };
    xhttp.open("GET", sdp, true);
    xhttp.send();
}

function loadSampleDL(data) {
    var table_body = "";
    for (var i in data) {
        if (i == 0) {
            table_body += "<thead><tr>";
            for (var m in data) {
                if (data[m][0] == 0) {
                    table_body += "<th> >" + data[m][0] + " </th>";
                }else {
                    table_body += "<th> ≥" + data[m][0] + " </th>";
                }
            }
            table_body += "</tr></thead><tbody><tr>";
        }
        var percent = data[i][1]
        table_body += "<td style=\"background-color: " + getHeatColor(percent) + ";\"> " + percent + "% </td>";
    }
    table_body += "</tr></tbody>";
    return table_body;
}

function get0xFrag(json, sdp){
    var frag_0x = json["0x_frag"];
    var data = new Array();
    var frag_0x_sorted = Object.keys(frag_0x).map(function(key) {
        return [key, frag_0x[key]];
    });
    frag_0x_sorted.sort(function(first, second) {
        return second[1] - first[1];
    });
    for (var i in frag_0x_sorted) {
        var row = new Array();
        row.push("<a href=\"#\" onclick=\"openFragBaseCoverGraph('" + getFragJsonUrl(sdp, frag_0x_sorted[i][0]) + "');return false;\">" + frag_0x_sorted[i][0] + "</a>");
        row.push(frag_0x_sorted[i][1] + "%");
        data.push(row);
    }
    return data;
}

function getFragDL(frag_cl, sdp) {
    var data = new Array();
    for (var i in frag_cl) {
        var row = new Array();
        for (var j in frag_cl[i].depth_level) {
            if (j == 0) {
                row.push("<a href=\"#\" onclick=\"openFragBaseCoverGraph('" + getFragJsonUrl(sdp, frag_cl[i].frag_name) + "');return false;\">" + frag_cl[i].frag_name + "</a>");
            }
            row.push(frag_cl[i].depth_level[j][1] + "%");
        }
        data.push(row);
    }
    return data;
}

function getFragJsonUrl(sdp, frag_name) {
    return getDirname(sdp) + "/" + frag_name + ".json";
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

function getDirname(path) {
     return path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '');
}

function getBasename(path) {
     return path.replace(/\\/g,'/').replace( /.*\//, '' );
}

function loadFragCoverTable(data) {
    table_head = "<thead><tr><th>片段名称</th>";
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

function openFragBaseCoverGraph(frag_d_url) {
    if ((typeof frag_d_url=='string')&&frag_d_url.constructor==String) {
        window.open("frag_base_cover_graph.php?u0=" + frag_d_url);
    }else if ((typeof frag_d_url=='object')&&frag_d_url.constructor==Array) {
        var param = "";
        for (var i = 0; i < frag_d_url.length; i ++) {
            if (i == 0)  {
                param += "u" + i + "=" + frag_d_url[i];
            }else {
                param += "&u" + i + "=" + frag_d_url[i];
            }
        }
        window.open("frag_base_cover_graph.php?"+ param);
    }   
}

function compSap_QC_SD() {
    var input_sdp_obj = $("input[name='sdp']:checked");
    var param = "";
    for (var i = 0; i < input_sdp_obj.length; i ++) {
        var sdp = $("input[name='sdp']:checked:eq(" + i + ")");
        if (sdp.val() != 0) {
            if (param == "") {
                param += "u" + i + "=" + sdp.val();
            }else {
                param += "&u" + i + "=" + sdp.val();
            }
        }
    }
    if (param == "") {
        new PNotify({
            title: '所选样本没有相关数据',
            type: 'error',
            hide: false,
            styling: 'bootstrap3'
            });
    }else {
        window.open("sap_comp_qc_sd.php?"+ param);
    }
}
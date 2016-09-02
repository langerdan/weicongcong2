/**
 * PROGRAM  : QC_Report_SD
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : September 1 2016
 * VERSION  : v0.0.1a
 */

 function loadReport_SD(sdp) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var json = JSON.parse(xhttp.responseText);

            // pass details
            var pass_details = "";
            if (!json.pass['0xfrag']) {
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
            document.getElementById("0x_frag").innerHTML = loadZeroFrag(json["0x_frag"]);
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

function RGBToHex(r, g, b) {
    function componentToHex(c) {
        var hex = c.toString(16);
        return hex.length == 1 ? "0" + hex : hex;
    }
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function loadZeroFrag(data) {
	table_body = "<thead><tr><th>片段名称</th><th>0x百分比</th></tr></thead><tbody>";
	var data_sorted = Object.keys(data).map(function(key) {
	    return [key, data[key]];
	});
	data_sorted.sort(function(first, second) {
	    return second[1] - first[1];
	});
	for (var i in data_sorted) {
		table_body += "<tr><td>" + data_sorted[i][0] + "</td><td>" + data_sorted[i][1] + "</td></tr>";
	}
	table_body += "</tbody>";
	return table_body;
}
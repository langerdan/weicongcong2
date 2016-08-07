/* 
 * PROGRAM  : loadData
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 6 2016
 * VERSION  : v0.0.1a
 */

var color_sheet = new Array();;

function loadData(dir_name) {
  var path_pointer = "data/" + dir_name + "/data_pointer.json";
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
	  var json = JSON.parse(xhttp.responseText);
	  //console.log(json);
      document.getElementById("data_name").innerHTML = dir_name;
	  document.getElementById("sample_num").innerHTML = json.sample_number;
	  document.getElementById("amplicon_num").innerHTML = json.amplicon_number;
	  var amplicon_data = json.amplicon_data;
	  loadTable(amplicon_data);
	  
	  // create color sheet by sample number
	  for (var i = 0; i < json.sample_number; i ++) {
		color_sheet.push(dynamicColors());
	    //console.log(color_sheet[color_sheet.length-1].r);
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
	each_amplicon = data_list[i];
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

function dynamicColors() {
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return {"r": r, "g": g, "b": b};
}
/**
 * PROGRAM  : DB_queryDBlab
 * PURPOSE  :
 * AUTHOR   : codeunsolved@gmail.com
 * CREATED  : August 23 2016
 * VERSION  : v0.0.1a
 */

$('#search_go').click(function () {
    var project = $("select[name='project']").children(':selected').val();
    var search_term = $("input[name='search_term']").val();
    var search_type = $("input[name='search_type']:checked").val();
    console.log(project+search_term+search_type);
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            document.getElementById('datatable-buttons').innerHTML = xhttp.responseText;
        }
    };
    xhttp.open("GET", "db_lab_query.php?f=db&p=" + project + "&term=" + search_term + "&type=" + search_type, true);
    xhttp.send();
})
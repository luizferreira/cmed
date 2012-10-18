$(document).ready(function(){
    var url = window.location.pathname;
    var id = url.split("/");
    id = "div#"+id[5];
    if (id == "div#") id = "div#chart_folder_view";
    $(id).addClass("portlet_selected");

});
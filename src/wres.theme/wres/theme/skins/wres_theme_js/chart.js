$(document).ready(function(){
    var url = window.location.pathname;
    var id = url.split("/");
    id = "div#"+id[5];
    $(id).addClass("portlet_selected");

});
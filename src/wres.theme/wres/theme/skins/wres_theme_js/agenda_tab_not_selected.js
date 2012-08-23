$(document).ready(function(){
	$("li#portaltab-agenda a").css("background", "#ddd");
	$("li#portaltab-agenda a").css("color", "#205C90");
	$("li#portaltab-agenda a").mouseover(function(){
	    $(this).css("background-color", "#205c90");
	    $(this).css("color", "white");
    })
	$("li#portaltab-agenda a").mouseout(function(){
        $(this).css("background-color", "#ddd");
        $(this).css("color", "#205c90");
    })	
})
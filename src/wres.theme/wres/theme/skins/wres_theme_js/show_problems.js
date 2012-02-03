
function fill_hidden_end_date() {

	shown_end = $("input#shown_reported");
	hidden_end = $("input#hidden_reported");
	shown_end_date = shown_end.val();

	if(shown_end_date) {
	str_split = shown_end_date.split("/");
	day = str_split[0];
	month = str_split[1];
	year = str_split[2];

	end_f = year.concat("/", month, "/", day);

	hidden_end.val(end_f);
	}

	$(this).hide();
	$("#loadergif").show();		
}

function fill_hidden_start_date() {
	shown_start = $("input#started");
	hidden_start = $("input#hidden_started");
	shown_start_date = shown_start.val();

	if(shown_start_date) {
		str_split = shown_start_date.split("/");
		day = str_split[0];
		month = str_split[1];
		year = str_split[2];

		start_f = year.concat("/", month, "/", day);		

		hidden_start.val(start_f);
	}	
}

function date_higher_1900() {
    shown_start = $("input#started").val();
    str_split = shown_start.split("/");
	day = str_split[0];
	month = str_split[1];
	year = str_split[2];
    if(year < 1900){
        $("input#started").val("");
        $("#erro_date").show();
        }
    else $("#erro_date").hide();
    
}


$(document).ready(function(){
    $("#erro_date").hide();

	$("input#add_new").click(fill_hidden_start_date)

	$("input#add_new").click(fill_hidden_end_date)

//	$("input#add_prescription").click(fill_hidden_end_date)

//	$("input#add_prescription").click(fill_hidden_end_date)

});

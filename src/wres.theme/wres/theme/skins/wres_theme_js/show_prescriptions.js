
function fill_hidden_end_date() {

	shown_end = $("input#end_date");
	hidden_end = $("input#hidden_end_date");
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
	shown_start = $("input#date");
	hidden_start = $("input#hidden_date");
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

function calculateDeltaTime(){
	delta = parseInt($("input#delta").val());
	radio_val = $(":checked.date").val();
	shown_end = $("input#end_date");
	start_date = $("input#hidden_date").val();
	start_date = new Date(start_date);
	end_date = new Date();
	end_date.setDate(start_date.getDate());
	end_date.setMonth(start_date.getMonth());
	end_date.setFullYear(start_date.getFullYear());	
	d = 0; m = 0;
	switch(radio_val) {
		case 'days':
			end_date.setDate(end_date.getDate() + delta);
			break;
		case 'weeks':
			d = end_date.getDate() + delta*7;
			end_date.setDate(d);
			break;
		case 'months':
			end_date.setMonth(end_date.getMonth() + delta);
			break;
	}
	d = end_date.getDate();
	if (d < 10) {
		d = "0" + d;
	}
	m = end_date.getMonth();
	// mes de 0-11 para 1-12
	m++;
	if (m < 10) {
		m = "0" + m;
	}		
	end_date = d + "/" + m + "/" + end_date.getFullYear();
	shown_end.val(end_date);
}

$(document).ready(function(){

	fill_hidden_start_date();

	$("input#date").change(fill_hidden_start_date)

	$("input#add_prescription").click(fill_hidden_end_date)

	// botão "Salvar" do edit_prescription.cpt
	$("input#save_edit").click(fill_hidden_end_date)

	$("input#delta").change(calculateDeltaTime)

	$("input.date").change(calculateDeltaTime)

});
function show_note(){
    $("table#note_table").fadeIn();
    }
    
function hide_note(){
    $("table#note_table").fadeOut();
    }
    
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
        document.getElementById('erro_date').style.display = "inline"
        }
    else document.getElementById('erro_date').style.display = "none"
    
}

/*=======================================================
recebe valor, lista1 e lista2 - localiza valor na lista 1 
e pega o valor correspondente (de mesmo indice) da lista 2
========================================================*/
function get_correspondent(campo, lista1, lista2) {
    var index;
    var i = 0;
    while (i < lista1.length) {
        if (lista1[i] == campo.value) {
            index = i;
            break;
        }
        i++;
    }
    if (campo.id == 'problem') {
        var campo2 = $("input#code");
    }
    else {
        var campo2 = $("input#problem");
    }
    if (index != undefined) {
        campo2.val(lista2[index]);
    }
}


$(document).ready(function(){
	$("input#add_new").click(fill_hidden_start_date);

	$("input#add_new").click(fill_hidden_end_date);


    huge_CIDdesc = null;
    huge_CIDcode = null;

    // carrega o autocomplete
    $.get("./getCID_desc", function(data){
        huge_CIDdesc = eval(data);
        $( "#problem" ).autocomplete({minLength: 3, source: huge_CIDdesc});
    });

    // carrega o autocomplete
    $.get("./getCID_code", function(data){
        huge_CIDcode = eval(data);
        $( "#code" ).autocomplete({minLength: 1, source: huge_CIDcode});
    });

    // blur é disparado quando o elemento perde o foco
    $("#problem").blur(function() {
        get_correspondent(this, huge_CIDdesc, huge_CIDcode);
    });
    
    // assim que ele perde o foco ele pega a descrição equivalente ao código e preenche o outro campo
    $("#code").blur(function() {
        get_correspondent(this, huge_CIDcode, huge_CIDdesc);
    });

});

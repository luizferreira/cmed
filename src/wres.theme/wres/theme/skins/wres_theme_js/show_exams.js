//function show_note(){
    //$("table#note_table").fadeIn();
    //}
//function hide_note(){
    //$("table#note_table").fadeOut();
    //}
//function fill_hidden_end_date() {

	//shown_end = $("input#shown_reported");
	//hidden_end = $("input#hidden_reported");
	//shown_end_date = shown_end.val();

	//if(shown_end_date) {
	//str_split = shown_end_date.split("/");
	//day = str_split[0];
	//month = str_split[1];
	//year = str_split[2];

	//end_f = year.concat("/", month, "/", day);

	//hidden_end.val(end_f);
	//}

	//$(this).hide();
	//$("#loadergif").show();		
//}

//function fill_hidden_start_date() {
	//shown_start = $("input#started");
	//hidden_start = $("input#hidden_started");
	//shown_start_date = shown_start.val();

	//if(shown_start_date) {
		//str_split = shown_start_date.split("/");
		//day = str_split[0];
		//month = str_split[1];
		//year = str_split[2];

		//start_f = year.concat("/", month, "/", day);		

		//hidden_start.val(start_f);
	//}	
//}

//function date_higher_1900() {
    //shown_start = $("input#started").val();
    //str_split = shown_start.split("/");
	//day = str_split[0];
	//month = str_split[1];
	//year = str_split[2];
    //if(year < 1900){
        //$("input#started").val("");
        //document.getElementById('erro_date').style.display = "inline"
        //}
    //else document.getElementById('erro_date').style.display = "none"
    
//}

//GLOBAL VARS
var counter = 0
var counter_trash = []

function get_upper_row(row,n_rows){
    var rows = $("#table_form")[0].rows
    var before = 0
    var row_id = null
    for(i=1;i<=n_rows;i++){
        row_id = parseInt(rows[i].id.split("linha")[1])
        if (row == row_id){
            return before
            }
            before = row_id
        }
    return null
    }

function remove_form_row(row){
    var n_rows = $("#table_form")[0].rows.length
    var upper_row = get_upper_row(row,n_rows)
    
    if(row == counter){
        $("form").find("tbody").find('#linha'+row).remove();
        //Devolve o poder de adicionar a linha acima unbind evita multiple fires
        $("#exam_form"+upper_row).unbind('focus').bind("focus",add_form_row)
        counter--
        }
    
    else{
        $("form").find("tbody").find('#linha'+row).remove();
        counter_trash.push(row)
        //Devolve o poder de adicionar a linha acima unbind evita multiple fires
        if(upper_row == 0 && n_rows==3){
                $("#exam_form"+upper_row).unbind('focus').bind("focus",add_form_row)
            }
        }
    }

function add_form_row(){
    
    counter++
    var classe = ""
    
    
    //Pintar fundo
    if ((counter % 2) == 1){
        classe = "odd"
        }
    else {
        classe = ""
        }
    //Linha na tabela
    
    var hidden_input = "<input id />"
    
    var remove_button = "<td>"+
                        "<span align='left'>"+
                        "<b id='remove"+counter+"'><a href='javascript:void(0)' onClick='add_form_row()'>+&nbsp</a></b>"+
                        "<b id='add"+counter+"'><a href='javascript:void(0)' onClick='remove_form_row("+counter+")'>&nbsp-</a></b>" +
                        "</span></td>" 
    var table_row = "<tr "+
                            'id="linha'+counter+'"'+
                            " class="+classe+">" +
                            remove_button + 
                            "<td>" +
                                '<input id="exam_form'+counter+'"' +' type="text" name="exam_form'+counter+'"' +
                                'onFocus="add_form_row()"' +
                                'tal:attributes="value data/exam | nothing" /> '+
                            '</td>'+
                            '<td>'+
                                '<input id="value_form'+counter+'"' +' type="text" name="value_form'+counter+'"' +
                                'tal:attributes="value data/value | nothing" />'+
                            '</td>'+
                            '<td>'+
                                '<input id="date_form'+counter+'"' +' type="text" name="date_form'+counter+'"' +
                                'tal:attributes="value data/date | python:context.getTodayDate().strftime('+"'%d/%m/%Y'" + ')"/>' +
                            '</td>'+
                        '</tr>"'
    
    $("form").find("tbody").append(table_row)
    
    //Remove poder de adcionar focus na linha acima
    var n_rows = $("#table_form")[0].rows.length
    $("#exam_form"+get_upper_row(counter,n_rows)).attr("onfocus","").unbind("focus")
    
    //Coloca a data do primeiro
    
    $("#date_form"+counter).val($("#date_form0").val())
    
    }


$(document).ready(function(){
//  $("input#exam"+counter).focus(add_form_row)

//	$("input#add_prescription").click(fill_hidden_end_date)

//	$("input#add_prescription").click(fill_hidden_end_date)

});

function getResidencial(){
	ddd = $("select#ahomePhone").val();
	phone = $('input[name="ahomePhone"]').val();

	if(ddd == "--" || phone == "") {
		alert("Por favor, preencha corretamente o campo 'Telefone Residencial'.");
		$("input#cphone_residencial").removeAttr("checked");
		$("input#cphone_number").val("");
		$("div#cphone_field").hide('slow');
	}
	else {
		$("select#acontactPhone").val(ddd);
		$("input#cphone_number").val(phone);
		$("div#cphone_field").show('slow');
		updateCPhone(ddd+phone);
	}
}

function getCell(){
	ddd = $("select#amobile").val();
	phone = $('input[name="amobile"]').val();

	if(ddd == "--" || phone == "") {
		window.alert("Por favor, preencha corretamente o campo 'Celular'.");
		$("input#cphone_cell").removeAttr("checked");
		$("input#cphone_number").val("");
		$("div#cphone_field").hide('slow');		
	}
	else {
		$("select#acontactPhone").val(ddd);
		$("input#cphone_number").val(phone);
		$("div#cphone_field").show('slow');
		updateCPhone(ddd+phone);
	}
}

function other(){
	$("input#cphone_number").val("");
	$("div#cphone_field").show('slow');
}


function updateCPhoneQuickRegister(){
	hidden_cphone = $('input[name="contactPhone"]');
	ddd = $("select#acontactPhone").val();
	phone = $('input[name="acontactPhone"]').val();
	hidden_cphone.val(ddd+phone);
}

/* funcao que atualiza o telefone de contato da visita de acordo
   com o paciente selecionado */
function updateCPhone(cphone) {
	area_code = cphone.substring(0,2);
	phone = cphone.substring(2);
	$('select[name="acontactPhoneVisit"]').val(area_code);
	$('input[name="acontactPhoneVisit"]').val(phone);
	$('input[name="contactPhoneVisit"]').val(area_code+phone);
	updateCPhoneQuickRegister()
}


$(document).ready(function(){

	if($("input#cphone_number").val() != "") {
                $("div#cphone_field").show();	
	}

	$("input#cphone_residencial").click(getResidencial)

	$("input#cphone_cell").click(getCell)

	$("input#cphone_other").click(other)

	// para o quick register template
	$("input#registerButton").click(updateCPhone)

});

$(document).ready(function(){
	$("#popup_search_patient").hide();
	$("#popup_quick_register_patient").hide();
    /* o que será exibido depede se está editando ou adicionando uma visita,
    caso esteja editando (URL contém 'SFAjax_base_edit'), deve-se esconder
    a pesquisa de paciente e aparecer o formulário de edição. */
    if(document.URL.indexOf("SFAjax_base_edit") !== -1) {
        $("#searchPatient").hide();
    }
    else {
        $("#visitBody").hide();
    }
	$("#createPatientBody").hide();

	$("#registerButton").click(function(){
		firstName = $("#firstName").val();
		lastName = $("#lastName").val();
		contactPhone = $('input[name="contactPhone"]').val();
		path = $("#visitFolderURL").val();
		$.post(path + "/saveNewDataPatient",
			{"firstName":firstName,"lastName":lastName,"contactPhone":contactPhone},
			function(data){
				data = JSON.parse(data);
				$("#newPatientMSG").fadeIn();
				choosePatient(data.name,data.url);
		});
	});
});

function choosePatient(patient_name, patient_url){
	$("#searchPatient").hide();
    $("#createPatientBody").hide();
    $("#visitBody").show();
    populate(patient_name,patient_url);
}

function createPatient(){
	$("#searchPatient").hide();
    $("#createPatientBody").fadeIn();
}

// =========================================================================
// PARTE DO ANTIGO buildingblockswidget.js ---------------------------------
// =========================================================================

function triggerEvent(element, eventType, canBubble) {
    canBubble = (typeof(canBubble) == undefined) ? true : canBubble;
    if (element.fireEvent) {
        element.fireEvent('on' + eventType);
    }
    else {
        var evt = document.createEvent('HTMLEvents');
        evt.initEvent(eventType, canBubble, true);
        element.dispatchEvent(evt);
    }
}

/* função faz uma requisição GET, usando json no patient.py do archetypes para pegar carregar informaçoes do mesmo. */
function getAttributesFromRemoteObj(path, handler){
    var url = path + "/getInformation";
    $.get(url,function(result){
        result = JSON.parse(result);
        handler(result);
    });

}

/* função que controla o processo de seleção do item (e.g paciente) */
function populate(title, path){
    var handler = function(result){

		addOption(document, 'patient:list', title, result.UID);
		selectOption(document, 'patient:list', result.UID);
        setTextElement(document, 'contactPhone', result.getContactPhone);
        updateCPhone(result.getContactPhone);
        setTextElement(document, 'lastOfficeVisit', result.getLastVisitDate);
        setTextElement(document, 'insurance', result.getInsurance);
        $("#patientFullName").html(result.fullName);
    };
	getAttributesFromRemoteObj(path, handler);
}

/* altera o texto de um determinado elemento htlm do schema. */
function setTextElement(doc, id, value){
//	alert("Funcao: " + "setTextElement\n" + "doc: " + doc + "\n" + "id: " + id + "\n" + "value: " + value);
    var txt_element = doc.getElementById(id);
	if(txt_element){
		txt_element.value = value;
		triggerEvent(txt_element, 'blur', false);
	}
}

/* pega o elemento html correspondente a seleção (e.g patient:list) e 
 * procura pela opção contida em value, caso a opção já exista, retorna 
 * o índice da mesma, caso contrário retorna -1 */
function findOption(mdocument, id_selection, value){
//    alert("Funcao: " + "findOption\n" + "mdocument: " + mdocument + "\n" + "id_selection: " + id_selection + "\n" + "value: " + value);
	var myList = mdocument.getElementById(id_selection)
	for (var x = 0; x < myList.length; x++){
		if (myList[x].value == value){
			return (x)
		}
	}
	return(-1)
}

/* seleciona a opção correspodente ao item em questão (e.g um paciente). 
 * Retorna falso caso não tenha encontrado a opção. */
function selectOption(mdocument, id_selection, value){
	var num_value = findOption(mdocument, id_selection,value);
	if(num_value!=-1){
		myList = mdocument.getElementById(id_selection);
		if(num_value<=myList.length){
			myList[num_value].selected="selected";
			return(true);
		}
	}
	return(false);
}

/* caso a opção do item (e.g paciente) não exista na seleção, essa função
 * adiciona a opção. */
function addOption(mdocument, id_selection, text, value){
//    alert("Funcao: " + "addOption\n" + "mdocument: " + mdocument + "\n" + "id_selection: " + id_selection + "\n" + "text:" + text + "\n" + "value: " + value);
	if(findOption(mdocument,id_selection,value)==-1){
		var opt = mdocument.createElement('option');
		opt.text = text;
		opt.value = value;
                $("#nomePacienteLabel").html(text)
		var my_list = mdocument.getElementById(id_selection);
		my_list.options.add(opt);
	}
}


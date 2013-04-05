/* this file depends of the uemr_js.js because of the triggerEvent function */

/* Fire an event in a browser-compatible manner -> stolen from selenium*/
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

function getXmlHttpRequest(){
//    alert("Funcao: " + "getXmlHttpRequest");
    if (window.XMLHttpRequest)
    {
        // pra quem tem XMLHttpRequest (gecko, opera, safari)
        return new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        // pro porcao que usa ActiveX
        // componentes porcos de activex, como nao adivinho qual o componente que o
        // amigo ta usando eu prefiro testar todos ate achar um que de certo
        // REVOLTA
        var aXmlIds = ["MSXML2.XMLHTTP.5.0", "MSXML2.XMLHTTP.4.0",
                       "MSXML2.XMLHTTP.3.0", "MSXML2.XMLHTTP", 
                       "MICROSOFT.XMLHTTP.1.0", "MICROSOFT.XMLHTTP.1", 
                       "MICROSOFT.XMLHTTP"];

        for (var i = 0; i < aXmlIds.length; i++)
        {
            try
            {
                // nao arrumei jeito melhor pra fazer!!!
                // aceito ideias!!!
                return new ActiveXObject(aXmlIds[i]);
            }
            catch(e)
            {
            }
        }
    }
    else
        throw new Error ('Browser not supported.');
}

/* função faz uma requisição GET, usando json no patient.py do archetypes para pegar carregar informaçoes do mesmo. */
function getAttributesFromRemoteObj(path, attrs, handler){
//    alert("Funcao: " + "getAtributesFromRemoteObj\n" + "attrs: " + attrs + "\n" + "handler: " + handler + "\n\n\n" + "path: " + path);
//	var url = 'getattributesfromremoteobj?path=' + path;
    
    var url = path + "/getPatientInformation";
    
	var xml_request = getXmlHttpRequest();
	xml_request.onreadystatechange = function () {
        if(xml_request.readyState == 4) {
            eval('var result = ' + xml_request.responseText);
//            alert("responseText = " + xml_request.responseText);    
//            alert("result = " + result);    
            if(handler) {
                handler(result);
            }
        }
	}
    
//    alert(xml_request);
//    url1 = 'http://localhost:8093/wres1/Patients'
//    alert("URL: " + url);    
	xml_request.open('GET', url, true);
	xml_request.send(null);
}

function EditpopulateOpenerField(fieldname, title, path){
	startPopulatingField(window, title, path);
}

function populateOpenerField(fieldname, title, path){
//    alert("Funcao: " + "populateOpenerField\n" + "title: " + title + "\n" + "path: " + path);
	if(fieldname == 'patient:list'){
		selectPatient(title, path);
	}
	else{
		document.body.style.cursor = 'progress';
		window.opener.defaultStartPopulatingField(fieldname, title, path);
		setTimeout("window.close()", 100);
	}
}


function defaultStartPopulatingField(fieldname, title, path){
//    alert("Funcao: " + "defaultStartPopulatingField\n" + "fieldname: " + fieldname + "\n" + "title: " + title + "\n" + "path: " + path);
	var start_populating = function (){
		defaultPopulate(fieldname, title, path);
	}
	setTimeout(start_populating, 100);
}

function defaultPopulate(fieldname, title, path){
//    alert("Funcao: " + "defaultPopulate\n" + "fieldname: " + fieldname + "\n" + "title: " + title + "\n" + "path: " + path);
	var handler = function(result){
		addOption(document, fieldname, title, result.UID);
		selectOption(document, fieldname, result.UID);
    	var closeWindow = function(){
			document.getElementById(fieldname).focus();
    	};
    	setTimeout(closeWindow, 100);
	}
	var attrs = ['UID'];
	getAttributesFromRemoteObj(path, attrs, handler);
}

function selectPatient(path,title){
//    alert("Funcao: " + "selectPatient\n" + "title: " + title + "\n" + "path: " + path);
	startPopulatingField(window, title, path);
}
/* Função inicial, ela que inicia o processo de preenchimento do campo
 * no schema */
function startPopulatingField(popup_window, title, path){
//	alert("Funcao: " + "startPopulatingField\n" + "popup_window: " + popup_window + "\n" + "title: " + title + "\n" + "path: " + path);
    var start_populating = function (){
		populate(title, path);
	}
	setTimeout(start_populating, 100);
}

/* funcao que atualiza o telefone de contato da visita de acordo
   com o paciente selecionado */
function updateCPhone(cphone) {
	area_code = cphone.substring(0,2);
	phone = cphone.substring(2);
	$("select#acontactPhone").val(area_code);
	$('input[name="acontactPhone"]').val(phone);
	$('#contactPhone').val(area_code+phone);
}

/* função que controla o processo de seleção do item (e.g paciente) */
function populate(title, path){
//	alert("Funcao: " + "populate\n" + "title: " + title + "\n" + "path: " + path);
    var handler = function(result){
//        alert("entrei no handler");
		addOption(document, 'patient:list', title, result.UID);
		selectOption(document, 'patient:list', result.UID);
	    setTextElement(document, 'contactPhone', result.getContactPhone);
	    updateCPhone(result.getContactPhone);
    	setTextElement(document, 'lastOfficeVisit', result.getLastVisitDate);
    	setTextElement(document, 'ext', result.getExt);
	}
	var attrs = ['UID', 'getContactPhone', 'getLastVisitDate', 'getExt'];
	getAttributesFromRemoteObj(path, attrs, handler);
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

function addElementAndCloseWindow(mwindow, id_selection, text, value){
	addOption(mwindow.opener.document, id_selection, text, value);
	selectOption(mwindow.opener.document, id_selection, value);
	mwindow.close();
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

//----------------------------- MyObject
function MyObject(inner_object, related_field, template_url, onclick_template){
	this.inner_object = inner_object;
	this.related_field = related_field;
	this.template_url = template_url;
	this.onclick_template = onclick_template;
}

MyObject.prototype.changeQs = function(evt){
	/* as instrucoes abaixo sao necessarias pq o modelo de eventos do IE eh
	diferente daquele do Mozilla */
	if(!evt){
		var evt = window.event;
		var target = evt.srcElement;
	}
	else{
		var target = evt.target;
	}

	var onclick_str = this.onclick_template;
	onclick_str = onclick_str.replace('\$' + this.related_field, target.value);
	this.inner_object.onclick = function(){eval(onclick_str)};
}

//----------------------------- VocabularyController
function VocabularyController(vocabulary_source, current_key){
	this.select_field = document.getElementById(vocabulary_source);
	this.current_key = current_key;
	this.biggest_text = 0;
	for(var i=2; i<arguments.length; i++){
		this[arguments[i]] = new Array();
	}
}

VocabularyController.prototype.addElementVocabulary = function(key, elem){
	var list = this[key];
	list[list.length] = elem;
}

VocabularyController.prototype.refreshList = function(){
	var num_itens = this.select_field.options.length;
	var current_list = this[this.current_key];
	for(var i=0; i<num_itens; i++){
		current_list[i] = new Array();
		current_list[i][0] = this.select_field[i].value;
		current_list[i][1] = this.select_field[i].text;
	}
}

VocabularyController.prototype.changeList = function(evt){
	/* as instrucoes abaixo sao necessarias pq o modelo de eventos do IE eh
	diferente daquele do Mozilla */
	if(!evt){
		var evt = window.event;
		var target = evt.srcElement;
	}
	else{
		var target = evt.target;
	}
	
	/* necessario pq no IE o onchange nao funciona direito, ai tive que associar 
	ao evento onclick */
	if(this.current_key == target.value) return;

	/* necessrio para evitar a perda de items adicionados aps o 
	VocabularyController ter sido criado*/
	this.refreshList();

	//limpa o select
	var num_itens = this.select_field.options.length;
	for(var i=0; i<num_itens; i++){
		this.select_field.remove(0);
	}

	//obtm a lista com os elementos a serem colocados no select
	this.current_key = target.value;
	var list = this[this.current_key];

	//coloca lista no select
	for(i=0; i<list.length; i++){
		var opt = document.createElement('option');
		opt.value = list[i][0];
		opt.text = list[i][1];

		/* As duas linhas abaixo sao necessarias porque a instrucao
		this.select_field.add(opt, null); nao funciona no IE.*/
		var opts = this.select_field.options
		opts[opts.length] = opt;
	}
}

//TODO:Gambiarra para pegar o telefone
$(document).ready(function(){
if($("#acontactPhone")[0]){
                if($("#hiddenPhone")[0]){
                updateCPhone($("#hiddenPhone")[0].value)
                }
        }
});

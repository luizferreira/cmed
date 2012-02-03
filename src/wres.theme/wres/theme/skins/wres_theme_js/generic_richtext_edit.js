
$(document).ready(function(){
	
	/*	As duas funcoes a seguir controlam as tabs 'ANTERIORES'
		e 'MODELOS'.
	*/
	$("#previous_button").click(function(){
		$("#templates").hide("slow");
		$("#previous_docs").show("slow");
	})
	$("#templates_button").click(function(){
		$("#previous_docs").hide("slow");
		$("#templates").show("slow");
	})		

	/*	Evento de incluir um documento anterior no corpo do documento. 
		doc_content eh apenas o conteudo do documento. O 2 children()
		sao usados para retirar as divs pais, o que estava
		causando bugs.	
		'body_gdoc' eh o corpo do documento, que recebera o conteudo
		incluido. Essa forma diferente de seleciona-lo eh pelo fato 
		de ele ser um iframe. O .find("#content") seleciona o body
		dentro da iframe gdocument_body_ifr.	
	*/
	$("#document_include_button").click(function(event){
		event.preventDefault();
//		doc_content = $("#doc_content");
//		doc_content = $(".docs_content:visible")
//		aqui eu pego apenas o conteúdo da div neta.
		doc_content = $(".docs_content:visible").children().children();
		body_gdoc = $("#gdocument_body_ifr").contents().find("#content");
		body_gdoc.fadeOut("slow");
		doc_content.clone().appendTo(body_gdoc);
		body_gdoc.fadeIn("slow");
	})

	/*	Evento de incluir um template no corpo do documento. 
		'doc_content' eh apenas o conteudo do documento. O 2 children()
		sao usados para retirar as divs pais, o que estava
		causando bugs.
		'body_gdoc' eh o corpo do documento, que recebera o conteudo
		incluido. Essa forma diferente de seleciona-lo eh pelo fato 
		de ele ser um iframe. O .find("#content") seleciona o body
		dentro da iframe gdocument_body_ifr.
	*/
	$("#template_include_button").click(function(event){
		event.preventDefault();
//		doc_content = $("#template_content");
//		doc_content = $(".templates_content:visible");
//		aqui eu pego apenas o conteúdo da div neta.
		doc_content = $(".templates_content:visible").children().children();
		body_gdoc = $("#gdocument_body_ifr").contents().find("#content");
		body_gdoc.fadeOut("slow");
		doc_content.clone().appendTo(body_gdoc);
		body_gdoc.fadeIn("slow");
	})	
	
	/* As duas funcoes a seguir controlam o <select> de documentos
		anteriores e modelos. 
	*/
	$("#doc_select").change(function(){		
		var selector = "#" + this.value;
		$(".docs_content").hide()
		//$(".docs_content").hide()
		//$(selector).show("slow");
		$(selector).fadeIn();
	})
	$("#template_select").change(function(){
		var selector = "#" + this.value;
		//$(".templates_content").hide()
		$(".templates_content").hide()
		//$(selector).show("slow");
		$(selector).fadeIn();
	})
	

	/*	As duas funcoes a seguir sao apenas efeitos no botao
		"Incluir".
	*/
	$("th.include_button").mouseover(function(){
		$(this).css("background-color", "#75AD0A");
		$(this).css("color", "white");
	})
	$("th.include_button").mouseout(function(){
		$(this).css("background-color", "#205c90");
		$(this).css("color", "white");
	})	
		
});


	


function include_document_or_template(event) {
	/*	Inclui um documento anterior (ou modelo) no corpo do documento. 
		doc_content eh apenas o conteudo do documento. O 2 children()
		sao usados para retirar as divs pais, o que estava
		causando bugs.	
		'body_gdoc' eh o corpo do documento, que recebera o conteudo
		incluido. Essa forma diferente de seleciona-lo eh pelo fato 
		de ele ser um iframe. O .find("#content") seleciona o body
		dentro da iframe gdocument_body_ifr.	
	*/	
	event.preventDefault();
	/* caso tenha algum documento anterior visivel, ele sera incluido.
	 caso contrario, um modelo sera incluido. */
	if ($(".docs_content:visible").length) {
		/* aqui eu pego apenas o conteúdo da div neta. */
		doc_content = $(".docs_content:visible").children().children();
	}
	else {
		/* aqui eu pego apenas o conteúdo da div neta. */
		doc_content = $(".templates_content:visible").children().children();
	}

	/* a selecao abaixo eh diferente porque o elemento 'content' esta dentro
	de um iframe (a richtext widget) */
	body_gdoc = $("#gdocument_body_ifr").contents().find("#content");
	body_gdoc.fadeOut("slow");
	/* se ja existe conteudo na richtext widget, da um append, caso contrario
	utiliza html() para preencher tudo (inclusive o <p> vazio inicial) */
	if(body_gdoc.find("br[mce_bogus]").length) {
        /*existe um bug que impede o atributo 'rows' da RichTextWidget de funcionar quando
        nao se esta na aba Principal (como eh o caso do document_body), por isso o trecho
        a seguir aumenta o tamanho do corpo do documento na marra.*/
        gdoc_iframe = $("#gdocument_body_ifr");
        gdoc_iframe.css("height", "350");        
		body_gdoc.html(doc_content.clone());
	}		
	else {
		doc_content.clone().appendTo(body_gdoc);
	}
	body_gdoc.fadeIn("slow");	
}

function setPreviousModelsColor(previous_selected){
        //Unbind eventos antigos
        $("#previous_button").unbind("mouseout");
        $("#previous_button").unbind("mouseover");
        $("#templates_button").unbind("mouseout");
        $("#templates_button").unbind("mouseover");
        if(previous_selected){
                //Default color para Today selecionado
                $("#previous_button").css("background-color", "#205c90")
                $("#previous_button").css("color", "white")
                $("#templates_button").css("background-color", "white")
                $("#templates_button").css("color", "#205c90")
                
                $("#templates_button").mouseover(function(){
                        $(this).css("background-color", "#205c90");
                        $(this).css("color", "white");
                        })
                $("#templates_button").mouseout(function(){
                        $(this).css("background-color", "white");
                        $(this).css("color", "#205c90");
                        })	
                
                $("#previous_button").mouseover(function(){
                        $(this).css("text-decoration", "underline");
                        })
                $("#previous_button").mouseout(function(){
                        $(this).css("text-decoration", "none");
                        })
                }
        else{                
                //Default color para Amanha selecionado
                $("#templates_button").css("background-color", "#205c90")
                $("#templates_button").css("color", "white")
                $("#previous_button").css("background-color", "white")
                $("#previous_button").css("color", "#205c90")
                
                $("#previous_button").mouseover(function(){
                        $(this).css("background-color", "#205c90");
                        $(this).css("color", "white");
                        })
                $("#previous_button").mouseout(function(){
                        $(this).css("background-color", "white");
                        $(this).css("color", "#205c90");
                        })	
                
                $("#templates_button").mouseover(function(){
                        $(this).css("text-decoration", "underline");
                        })
                $("#templates_button").mouseout(function(){
                        $(this).css("text-decoration", "none");
                        })
                }
        }


$(document).ready(function(){

    /*existe um bug que impede o atributo 'rows' da RichTextWidget de funcionar quando
    nao se esta na aba Principal (como eh o caso do document_body), por isso o trecho
    a seguir aumenta o tamanho do corpo do documento na marra.*/
    $("#fieldsetlegend-corpo-do-documento").click(function(){
        $("#gdocument_body_ifr").contents().find("#content").click(function(){
            gdoc_iframe = $("#gdocument_body_ifr");
            gdoc_iframe.css("height", "350");
            $(this).unbind("click");
        });
    })
	
	/*	As duas funcoes a seguir controlam as tabs 'ANTERIORES'
		e 'MODELOS'.
	*/
	//Default colors to buttons
        var previous_selected = true;
        setPreviousModelsColor(previous_selected)
        
        $("#previous_button").click(function(){
                previous_selected = true;
                setPreviousModelsColor(previous_selected)
		$("#templates").hide("slow");
		$("#previous_docs").show("slow");
	})
	$("#templates_button").click(function(){
                previous_selected = false;
                setPreviousModelsColor(previous_selected)
		$("#previous_docs").hide("slow");
		$("#templates").show("slow");
	})		

	/* os dois eventos abaixo referem-se ao botoes de inclusao de documento anterior e
	modelo, respectivamente */
	$("#document_include_button").click(include_document_or_template)
	$("#template_include_button").click(include_document_or_template)	
	
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


	

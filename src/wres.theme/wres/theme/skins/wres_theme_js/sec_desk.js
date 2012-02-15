
function escondeMostraVisitas(){
	var doctor_id = this.value;
	if (this.selected == true) {
		var selector = "tr." + doctor_id;
		$(selector).fadeIn("slow");
	}
	else {
		if(doctor_id != '') {
			var selector = "tr." + doctor_id;
			$(selector).fadeOut("slow");
		}
	}	
}

$(document).ready(function(){
	
	var show_visits_reloaded = false;
	/*var fez_requisicao = false;*/
	
	$("#show_tomorrow_visits").hide();
	
	$("#doctor_select").change(function(){
	
		if($("option:selected").get(0).value == "") {
			$("tr").fadeIn("slow");
		}
		else {
			$("option").each(escondeMostraVisitas)
		}
	})
	
	$("span.button").mouseover(function(){
		$(this).css("background-color", "#205c90");
		$(this).css("color", "white");
	})
	$("span.button").mouseout(function(){
		$(this).css("background-color", "white");
		$(this).css("color", "#205c90");
	})	
	$("#today_button").click(function(){
		$("#show_tomorrow_visits").hide("slow");
		$("#show_today_visits").show("slow");
		
		if($("option:selected").get(0).value == "") {
			$("tr").fadeIn("slow");
		}
		else {
			$("option").each(escondeMostraVisitas)
		}		
	})
	$("#tomorrow_button").click(function(){
		$("#show_today_visits").hide("slow");
		$("#show_tomorrow_visits").show("slow");
		
		if($("option:selected").get(0).value == "") {
			$("tr").fadeIn("slow");
		}
		else {
			$("option").each(escondeMostraVisitas)
		}		
	})	
	
	
	$(".show_visits").delegate("a.change_state_link", "click", function(event) {
        event.preventDefault();		

        /* esconde links e mostra loader gif */
        pai = $(this).parent();
        avo = pai.parent();
        avo.children("img").show();
        pai.hide();	
        
        href = $(this).attr('href');
        $.post(href, function(data) {
        	  if ($("#show_today_visits").is(":visible")) {
        		  $("#show_today_visits").load(location.href + " #show_today_visits");
        	  }
        	  else {
        		  $("#show_tomorrow_visits").load(location.href + " #show_tomorrow_visits");
        	  }
        }) 
	})	

	$('.show_visits').ajaxComplete(function(e, xhr, settings) {
		
		if($("option:selected").get(0).value == "") {
			$("tr").fadeIn("slow");
		}
		else {
			$("option").each(escondeMostraVisitas)
		}
	})			

});

function patientClick(){
	var data = {};
	var url = document.getElementById("patient_url").value;
	var extra = '/SFLight_patient_view';
	var titulo = 'Detalhes do Paciente';
	$dialog_content = $('#dialog_content');
	$dialog_content.empty();
	$dialog_content.dialog( "destroy" );
	$.get(url+extra, data,
	      function (msg) {
	          $dialog_content.append(msg);
	          $dialog_content.dialog({
	            width: 'auto',
	            autoOpen: true,
	            modal: true,
	            title: titulo,
	          });
	     }
	);
	
}
    
function timeClick(){
	var data = {};
	var url = document.getElementById("visit_url").value;
	var extra = '/SFLight_visittemp_view';
	var titulo = 'Detalhes da Consulta';
	$dialog_content = $('#dialog_content');
	$dialog_content.empty();
	$dialog_content.dialog( "destroy" );
	$.get(url+extra, data,
	      function (msg) {
	          $dialog_content.append(msg);
	          $dialog_content.dialog({
	            width: 'auto',
	            autoOpen: true,
	            modal: true,
	            title: titulo,
	          });
	     }
	);
}

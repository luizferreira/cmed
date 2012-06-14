
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

function loadPatientTip(index){

     var patient_url = $("#patient_url"+index).val()
     var AmIDoctor = $("#AmIDoctor").val()
     if (AmIDoctor == 1){
        $("#patient_link"+index).qtip({ 
            content: "<a href='"+patient_url+"'>Dados</a><br><a href='"+patient_url+"/chartFolder"+"'>Prontuário</a>",
            position:{
                corner: "rigthMiddle",
                adjust:
                    {
                        x: 100,
                        y: 0
                    }
    
            },
            style: { 
                padding: 2,
                background: '#DDDDDD',
                color: 'black',
                textAlign: 'center',
                fontSize: 13,
                border: {
                    radius: 2
                }
            },
            show: 'click',
            hide: {
                fixed: true,
                when: {
                    event: 'unfocus'
                }
            }
    
            })
        }
    else {
        $("#patient_link"+index).qtip({ 
            content: "<a href='"+patient_url+"'>Dados</a>",
            position:{
                corner: "rigthMiddle",
                adjust:
                    {
                        x: 100,
                        y: 0
                    }
    
            },
            style: { 
                padding: 2,
                background: '#DDDDDD',
                color: 'black',
                textAlign: 'center',
                fontSize: 13,
                border: {
                    radius: 2
                }
            },
            show: 'click',
            hide: {
                fixed: true,
                when: {
                    event: 'unfocus'
                }
            }
    
            })
        }
        
    }

function setTodayTomorrowColor(today_selected){
        if(today_selected){
                //Unbind eventos antigos
                $("#today_button").unbind("mouseout");
                $("#today_button").unbind("mouseover");
                $("#tomorrow_button").unbind("mouseout");
                $("#tomorrow_button").unbind("mouseover");
                
                //Default color para Today selecionado
                $("#today_button").css("background-color", "#205c90")
                $("#today_button").css("color", "white")
                $("#tomorrow_button").css("background-color", "white")
                $("#tomorrow_button").css("color", "#205c90")
                
                $("#tomorrow_button").mouseover(function(){
                        $(this).css("background-color", "#205c90");
                        $(this).css("color", "white");
                        })
                $("#tomorrow_button").mouseout(function(){
                        $(this).css("background-color", "white");
                        $(this).css("color", "#205c90");
                        })	
                
                $("#today_button").mouseover(function(){
                        $(this).css("text-decoration", "underline");
                        })
                $("#today_button").mouseout(function(){
                        $(this).css("text-decoration", "none");
                        })
                }
        else{
                //Unbind eventos antigos
                $("#today_button").unbind("mouseout");
                $("#today_button").unbind("mouseover");
                $("#tomorrow_button").unbind("mouseout");
                $("#tomorrow_button").unbind("mouseover");
                
                //Default color para Amanha selecionado
                $("#tomorrow_button").css("background-color", "#205c90")
                $("#tomorrow_button").css("color", "white")
                $("#today_button").css("background-color", "white")
                $("#today_button").css("color", "#205c90")
                
                $("#today_button").mouseover(function(){
                        $(this).css("background-color", "#205c90");
                        $(this).css("color", "white");
                        })
                $("#today_button").mouseout(function(){
                        $(this).css("background-color", "white");
                        $(this).css("color", "#205c90");
                        })	
                
                $("#tomorrow_button").mouseover(function(){
                        $(this).css("text-decoration", "underline");
                        })
                $("#tomorrow_button").mouseout(function(){
                        $(this).css("text-decoration", "none");
                        })
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
	//Hoje por default selecionado
        var today_selected = true;
        setTodayTomorrowColor(today_selected)
        $("#today_button").click(function(){
                var today_selected = true;
                setTodayTomorrowColor(today_selected)
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
                var today_selected = false;
                setTodayTomorrowColor(today_selected)
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

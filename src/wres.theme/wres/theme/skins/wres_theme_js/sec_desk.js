
function hideOrShowDoctorVisits(){
    /* this function is called for each option.
    If the option is the selected one, The function
    fadeIn all trs (visits) of the doctor, else,
    the function hide all trs (visits) of the doctor.
    Using "slow" effect here causes unpredictable
    behaviors, since this effect has a considerable
    delay, and the element will be in a state that was
    not expected by the hideTableOrNot steps.
    */
	var doctor_id = this.value;
    //if selected, show (fadeIn), else hide.
	if (this.selected == true) {
		var selector = "tr." + doctor_id;
		$(selector).show();
	}
	else {
		if(doctor_id != '') {
			var selector = "tr." + doctor_id;
			$(selector).hide();
		}
	}
}

function hideTableOrNotStep1() {
    /*the table need to be visible, so hideOrShowDoctorVisits
    can show trs of the selected doctor.
    */
    $(".visits_table").show();
    $(".visits-message").show();
    $(".not-for-this-doctor").hide();
}

function hideTableOrNotStep2() {
    /* hide table if there is not any visit being
    showed.
    */
    if ($(".visit:visible").length == 0) {
        $(".visits_table").hide("slow");
        $(".visits-message").hide("slow");
        /* avoid duplication of "non exists" message */
        if($("#no-visits:visible").length == 0) {
            $(".not-for-this-doctor").show("slow");
        }
    }
    else {
        $(".visits_table").show("slow");
    }
}

function reloadVisitsOnScreen() {
    /* Show or hide doctors visits depending on
    which doctor is selected.
    if 'Todos os medicos' selected, show all trs
    else: pass throw all options and leave showing
    only the selected one.
    */
    hideTableOrNotStep1();
    if($("option:selected").get(0).value == "") {
        $("tr").show();
    }
    else {
        $("option").each(hideOrShowDoctorVisits);
    }
    hideTableOrNotStep2();
    hideAppointments();
}

function loadPatientTip(index){

     var patient_url = $("#patient_url"+index).val()
     var AmIDoctor = $("#AmIDoctor").val()
     if (AmIDoctor == 1){
        $("#patient_link"+index).qtip({
            content: "<a href='"+patient_url+"'>Dados</a><br><a href='"+patient_url+"/initChart"+"'>Prontuário</a>",
            show: {
                event: 'click',
            },
            position: {
                    my: 'left center',
                    at: 'right center',
                },

            hide: {
                effect: function(offset) {
                $(this).slideDown(1000); // "this" refers to the tooltip
                },
                event: false,
                inactive: 3000
            },
            style: {
                    classes: 'ui-tooltip-shadow ui-tooltip-' + 'blue'
                }

            })
        }
    else {
        $("#patient_link"+index).qtip({ 
            content: "<a href='"+patient_url+"'>Dados</a><br>",
            show: 'click',
            position: {
                    my: 'left center',
                    at: 'right center',
                },
            hide: {
                effect: function(offset) {
                $(this).slideDown(100); // "this" refers to the tooltip
                },
                event: false,
                inactive: 2000
            },
            style: {
                    classes: 'ui-tooltip-shadow ui-tooltip-' + 'blue'
                }

            })
        }

    }

function hideAppointments(){
    //hide today visists
    today_table = $("#show_today_visits");
    visits_rows = today_table.find(".visit");
    hided = 0;
    for(row = 0; row < visits_rows.length; row++){
        row_tag = visits_rows[row]
        status_tag = row_tag.getElementsByTagName("td")[2];
        if(status_tag.textContent == "Escondido"){
            today_table.find("#"+row_tag.id).hide();
            hided++;
        }
    }
    if(visits_rows.length == hided && visits_rows.length != 0){
        today_table.find("#visit_table").hide();
        today_table.find(".not-for-this-doctor").show();
    }

    //hide tomorrow visists
    tomorrow_table = $("#show_tomorrow_visits");
    visits_rows = tomorrow_table.find(".visit");
    hided = 0;
    for(row = 0; row < visits_rows.length; row++){
        row_tag = visits_rows[row]
        status_tag = row_tag.getElementsByTagName("td")[2];
        if(status_tag.textContent == "Escondido"){
            tomorrow_table.find("#"+row_tag.id).hide();
            hided++;
        }
    }
    if(visits_rows.length == hided && visits_rows.length != 0){
        tomorrow_table.find("#visit_table").hide();
        tomorrow_table.find(".not-for-this-doctor").show();
    }

}

$(document).ready(function(){
    
	var show_visits_reloaded = false;
        /*var fez_requisicao = false;*/

	$("#doctor_select").change(function(){
	   reloadVisitsOnScreen();
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
        /* this avoid reloadVisitsOnScreen to be executed in Doctor sec_desk, since
        the doctor already see only his visits. */
        if($("option:selected").length > 0) {
            reloadVisitsOnScreen();
        }
        hideAppointments();
	})

    //Hide Appointment according WorkFlow
     hideAppointments();

     var path_ = window.location.pathname.split('/');
     var url_ = window.location.protocol + "//" + window.location.host + "/" + path_[1];
    if((path_[path_.length-1]=="Agenda")||((path_[path_.length-1]=="")&&(path_[path_.length-2]=="Agenda"))){
        $("head").append("<link rel='stylesheet' type='text/css' href='cmed.css' media='screen'/>");
        $("#content").append("<div style='position: absolute; top:75px; right:5px' class='aprenda'><a href='"+url_+"?tourId=3_d_configurando_calendario-configurando-o-seu&skinId=sunburst' class='btn btn-info'>Aprenda +</a></div>");
    }

    $(".visit_link").click(function() {
        event.preventDefault();
        var data = {};
        var url = $("#visit_url", $(this).parent()).val();
        var extra = '/SFLight_visit_view';
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
    });

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

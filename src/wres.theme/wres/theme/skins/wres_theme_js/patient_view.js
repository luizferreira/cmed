    function acende(id){
        document.getElementById(id).style.backgroundColor="#205c90";
        document.getElementById(id).style.color="white";
        }
    function apaga(id){
        document.getElementById(id).style.backgroundColor="white";
        document.getElementById(id).style.color="#205c90";
        }

function closeDialog(){
    $("#buttons_modal").dialog('close')
}
function askConfirmation(inactivate){
    //htmlContent = "<div id='buttons_modal' title='Você realmente deseja desativar este paciente?'><center><form><button type='button' style='margin-right:100px;width:70px' onclick=\"parent.location='"+ document.URL +"/patient_status_modify?workflow_action=inactivate';\" >Sim</button><button type='button' style='width:70px' onclick=\"closeDialog();\">Cancelar</button></form></center></div>"
    htmlContent = "<div id='buttons_modal' title='Você realmente deseja desativar este paciente?'></div>"
    $(htmlContent).dialog({
    height: "200px",
    width: "380px",
    buttons:[
        {
            text:'Sim',
            class:'save',
            click: function(){
                index = document.URL.indexOf("chartFolder");
                var newURL = "";
                if (document.URL.indexOf("chartFolder_hidden") != -1) {
                    // Desativando prontuário.
                    patientURL = document.URL.substring(0, index);
                    newURL = patientURL + "chartFolder_hidden/patient_status_modify?workflow_action=inactivate";
                }
                else {
                    // Desativando pelo view do paciente.
                    patientURL = document.URL;
                    if (patientURL.charAt(patientURL.length-1) == "/") {
                        newURL = patientURL + "patient_status_modify?workflow_action=inactivate";
                    }
                    else {
                        // Caso a URL esteja 'pteste/template_view' dará um NotFound, mas isso não acontece. (hopefully)
                        newURL = patientURL + "/patient_status_modify?workflow_action=inactivate";
                    }

                }
                parent.location = newURL;
            }
        },
        {
            text:'Cancelar',
            class:'cancel',
            click: function() {                     
                  $(this).dialog("close"); 
               }
        }
    ]})
}

    $(document).ready(function(){
        $("#Complementar").hide();
        $("#Demografico").hide();
        document.getElementById("principal_button").style.backgroundColor="#205c90";
        document.getElementById("principal_button").style.color="white";

        $("#principal_button").click(function(){
                acende("principal_button");

                apaga("complementar_button");
                apaga("demografico_button");

                $("#Complementar").hide();
                $("#Demografico").hide();
                $("#Principal").fadeIn();
            });

        $("#complementar_button").click(function(){

                acende("complementar_button");

                apaga("principal_button");
                apaga("demografico_button");

                $("#Principal").hide();
                $("#Demografico").hide();
                $("#Complementar").fadeIn();
            });

        $("#demografico_button").click(function(){
                acende("demografico_button");

                apaga("complementar_button");
                apaga("principal_button");

                $("#Principal").hide();
                $("#Complementar").hide();
                $("#Demografico").fadeIn();
            });
        });


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
                parent.location= document.URL + "/patient_status_modify?workflow_action=inactivate";
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


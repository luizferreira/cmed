    function acende(id){
        document.getElementById(id).style.backgroundColor="#205c90";
        document.getElementById(id).style.color="white";
        }
    function apaga(id){
        document.getElementById(id).style.backgroundColor="white";
        document.getElementById(id).style.color="#205c90";
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


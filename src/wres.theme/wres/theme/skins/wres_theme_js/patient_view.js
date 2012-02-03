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
        $("#Titular").hide();
        $("#Demografico").hide();
        $("#Contato").hide();
        $("#Planos").hide();
        document.getElementById("principal_button").style.backgroundColor="#205c90";
        document.getElementById("principal_button").style.color="white";
        
        $("#principal_button").click(function(){
                acende("principal_button");
                
                apaga("complementar_button");
                apaga("titular_button");
                apaga("plano_button");
                apaga("demografico_button");
                apaga("contato_button");
                
                $("#Complementar").hide();
                $("#Titular").hide();
                $("#Planos").hide();
                $("#Demografico").hide();
                $("#Contato").hide();
                $("#Principal").fadeIn();
            });
        
        $("#complementar_button").click(function(){
            
                acende("complementar_button");
                
                apaga("principal_button");
                apaga("titular_button");
                apaga("plano_button");
                apaga("demografico_button");
                apaga("contato_button");
                
                $("#Principal").hide();
                $("#Titular").hide();
                $("#Planos").hide();
                $("#Demografico").hide();
                $("#Contato").hide();
                $("#Complementar").fadeIn();
            });
        $("#titular_button").click(function(){
                acende("titular_button");
                
                apaga("complementar_button");
                apaga("principal_button");
                apaga("plano_button");
                apaga("demografico_button");
                apaga("contato_button");
            
                $("#Principal").hide();
                $("#Complementar").hide();
                $("#Demografico").hide();
                $("#Contato").hide();
                $("#Planos").hide();
                $("#Titular").fadeIn();
            });
        $("#plano_button").click(function(){
            acende("plano_button");
                
            apaga("complementar_button");
            apaga("titular_button");
            apaga("principal_button");
            apaga("demografico_button");
            apaga("contato_button");
            
            $("#Principal").hide();
            $("#Complementar").hide();
            $("#Demografico").hide();
            $("#Contato").hide();
            $("#Titular").hide();
            $("#Planos").fadeIn();
        });
        $("#demografico_button").click(function(){
                acende("demografico_button");
                
                apaga("complementar_button");
                apaga("titular_button");
                apaga("plano_button");
                apaga("principal_button");
                apaga("contato_button");
            
                $("#Principal").hide();
                $("#Complementar").hide();
                $("#Titular").hide();
                $("#Planos").hide();
                $("#Contato").hide();
                $("#Demografico").fadeIn();
            });
        $("#contato_button").click(function(){
                acende("contato_button");
                
                apaga("complementar_button");
                apaga("titular_button");
                apaga("plano_button");
                apaga("demografico_button");
                apaga("principal_button");
            
                $("#Principal").hide();
                $("#Complementar").hide();
                $("#Titular").hide();
                $("#Planos").hide();
                $("#Demografico").hide();
                $("#Contato").fadeIn();
            });
        });


$(document).ready(function (){
					$("#pictures").PikaChoose({carouselVertical:true,autoPlay:false});
                    $("#pictures2").PikaChoose({carouselVertical:true,autoPlay:false});
                
                //Add class to big images
                $("#gallery1").find("img").first().attr("class","changed1");
                $("#gallery2").find("img").first().attr("class","changed2");
                });
    //Add class to chosen image
     $(window).load(function() {
        
               $("#gallery1").find(".clip").click(function(){
                    $(".changed1").attr("class","");
                    var imageTag = $("#gallery1").find("img").first();
                    imageTag.attr("class","changed1");
                    });
                    
                $("#gallery2").find(".clip").click(function(){
                    $(".changed2").attr("class","");
                    var imageTag = $("#gallery2").find("img").first();
                    imageTag.attr("class","changed2");
                    }); 
            });

function changeName(){
                    images = $("#gallery1")[0].getElementsByTagName("a");
                    imagem = images[0]
                     if(images.length == 0){
                            $("#selection").text("Não há imagens")
                            $("#selection2").text("Não há imagens")
                        }
                    else if(imagem.hasAttribute("class")){
                        $("#selection").text("Não há imagens")
                        $("#selection2").text("Não há imagens")
                        }
                    else{                    
                         link_tokens = imagem.getAttribute("href").split("/")
                         image_name = link_tokens[link_tokens.length-1].split(".")[0]
                         $("#selection").text(image_name)
                    
                         imagem2 = $("#gallery2")[0].getElementsByTagName("a")[0];
                         link_tokens2 = imagem2.getAttribute("href").split("/")
                         image_name2 = link_tokens2[link_tokens2.length-1].split(".")[0]
                         $("#selection2").text(image_name2)
                         }
                    
                    
                }  
             

function changeName(){
                    images = $(".pikachoose")[0].getElementsByTagName("a");
                    imagem = images[0]
                    
                    if(images.length == 0){
                            $("#selection").text("Não há imagens")
                        }
                    else if(imagem.hasAttribute("class")){
                        $("#selection").text("Não há imagens")
                        }
                    else{                    
                    link_tokens = imagem.getAttribute("href").split("/")
                    image_name = link_tokens[link_tokens.length-1].split(".")[0]
                    $("#selection").text(image_name)
                    }
                }
			$(document).ready(function (){
                    changeName()
					$("#pictures").PikaChoose({autoPlay:false})
                });

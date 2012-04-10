$(document).ready(function (){
					$("#pictures").PikaChoose({carousel:true, carouselVertical:true,autoPlay:false});
                    $("#pictures2").PikaChoose({carousel:true, carouselVertical:true,autoPlay:false});
                    $(function(){
                        $('#container').beforeAfter();
                    });
                });
            
            var imageTag = $("#gallery1").find("img").first().clone();
            var imageTag2 = $("#gallery2").find("img").first().clone();
            var image = new Image();
            var image2 = new Image();
            
                    image.src = imageTag.attr("src");
                    imageTag.attr("width",image.width)
                    imageTag.attr("height",image.height)
                    imageTag.attr("style","")
                    imageTag.attr("id","before")
                    imageTag.attr("alt","before")
                    $("#divBefore").append(imageTag);
                    
                    image2.src = imageTag2.attr("src");
                    imageTag2.attr("width",image.width)
                    imageTag2.attr("height",image.height)
                    imageTag2.attr("style","")
                    imageTag2.attr("id","after")
                    imageTag.attr("alt","after")
                    $("#divAfter").append(imageTag2);
            
            $(window).load(function() {
        
                $("#gallery1").find(".clip").click(function(){
                    $("#before").remove()
                    var imageTag = $("#gallery1").find("img").first().clone();
                    image.src = imageTag.attr("src");
                    imageTag.attr("width",image.width)
                    imageTag.attr("height",image.height)
                    imageTag.attr("style","")
                    imageTag.attr("id","before")
                    $("#divBefore").append(imageTag);
                    $('#container').beforeAfter();
                    });
                    
                $("#gallery2").find(".clip").click(function(){
                    $("#after").remove()
                    var imageTag = $("#gallery2").find("img").first().clone();
                    image.src = imageTag.attr("src");
                    imageTag.attr("width",image.width)
                    imageTag.attr("height",image.height)
                    imageTag.attr("style","")
                    imageTag.attr("id","after")
                    $("#divAfter").append(imageTag);
                    $('#container').beforeAfter();
                    }); 
            });
             

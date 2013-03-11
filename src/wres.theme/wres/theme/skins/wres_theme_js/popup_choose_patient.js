 function selectPatient(title, path) {
     document.body.style.cursor = 'progress';
     window.opener.startPopulatingField(window, title, path);
     setTimeout("window.close()", 200);
 }

function stopEnterKey(evt) { 
  var evt = (evt) ? evt : ((event) ? event : null); 
  var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null); 
  if ((evt.keyCode == 13) && (node.type=="text"))  {return false;} 
} 
document.onkeypress = stopEnterKey; 

 $(document).ready(function(){
  
    $(document).bind('keyup', function(e) {
         if (e.which == 13) {
             li = $(".LSHighlight")
             li.children("a").click()
         }
     });
 });
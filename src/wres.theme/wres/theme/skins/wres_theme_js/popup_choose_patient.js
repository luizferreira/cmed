 function selectPatient(title, path){
            document.body.style.cursor = 'progress';
            window.opener.startPopulatingField(window, title, path);
            setTimeout("window.close()", 100);
        }
        
$(document).bind('keyup', function(e) {
    if (e.which == 13) {
        e.preventDefault();
        li = $(".LSHighlight")
        li.children("a").click()
        window.close()
    }
});
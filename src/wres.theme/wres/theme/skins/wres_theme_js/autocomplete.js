/*    Caret Functions     */
function getCaretEnd(obj){
    if(typeof obj.selectionEnd != "undefined"){
        return obj.selectionEnd;
    }else if(document.selection&&document.selection.createRange){
        var M=document.selection.createRange();
        var Lp=obj.createTextRange();
        Lp.setEndPoint("EndToEnd",M);
        var rb=Lp.text.length;
        if(rb>obj.value.length){
            return -1;
        }
        return rb;
    }
}
function getCaretStart(obj){
    if(typeof obj.selectionStart != "undefined"){
        return obj.selectionStart;
    }else if(document.selection&&document.selection.createRange){
        var M=document.selection.createRange();
        var Lp=obj.createTextRange();
        Lp.setEndPoint("EndToStart",M);
        var rb=Lp.text.length;
        if(rb>obj.value.length){
            return -1;
        }
        return rb;
    }
}
function setCaret(obj,l){
    obj.focus();
    if (obj.setSelectionRange){
        obj.setSelectionRange(l,l);
    }else if(obj.createTextRange){
        m = obj.createTextRange();      
        m.moveStart('character',l);
        m.collapse();
        m.select();
    }
}
/* ----------------- */

/*    Escape function   */
String.prototype.addslashes = function(){
    return this.replace(/(["\\\.\|\[\]\^\*\+\?\$\(\)])/g, '\\$1');
}
String.prototype.trim = function () {
    return this.replace(/^\s*(\S*(\s+\S+)*)\s*$/, "$1");
}; 
function actb_convert_escape_chars(str) {
    // Thanks to Ak Sorpa for this function
    // When a string is assigned to innerHTML, it will be converted
    // to contain escape sequences. For example,
    // word1 & word2 is converted into word1 &amp; word2
    // The following string
    // ~!@#$%^&*()_+=-{}][:;'/><|
    // is converted into
    // ~!@#$%^&amp;*()_+=-{}][:;'/&gt;&lt;|
    // Based on this test, only conversion of & < > signs is supported
    // by this function. Improve more if necessary.

    if (!str) {
        return str;
    }

    var escape_sequences = new Object();

    escape_sequences["&lt;"] = "<";
    escape_sequences["&gt;"] = ">";
    escape_sequences["&amp;"] = "&";

    var converted = str;
    for (var esc in escape_sequences) {
        converted = converted.replace(esc, escape_sequences[esc]);
    }

    return converted;
}


function actb(obj,evt,ca){
    /* ---- Variables ---- */
    var actb_timeOut = 2250; // Autocomplete Timeout in ms (-1: autocomplete never time out)
    var actb_lim = 5;    // Number of elements autocomplete can show (-1: no limit)
    var actb_firstText = 1; // should the auto complete be limited to the beginning of keyword?
    var actb_mouse = true; // Enable Mouse Support
    var actb_delimiter = new Array(';',',');  // Delimiter for multiple autocomplete. Set it to empty array for single autocomplete
    var actb_expand_onfocus = 1;
    var actb_complete_on_tab = 1;
    /* ---- Variables ---- */

    /* --- Styles --- */
    var actb_bgColor = '#888888';
    var actb_textColor = '#FFFFFF';
    var actb_hColor = '#000000';
    var actb_fFamily = 'Verdana';
    var actb_fSize = '11px';
    var actb_hStyle = 'color:blue;text-decoration:underline;font-weight="bold"';
    /* --- Styles --- */

    /* ---- Don't touch :P---- */
    var actb_delimwords = new Array();
    var actb_cdelimword = 0;
    var actb_delimchar = new Array();
    var actb_keywords = new Array();
    var actb_display = false;
    var actb_pos = 0;
    var actb_total = 0;
    var actb_curr = null;
    var actb_rangeu = 0;
    var actb_ranged = 0;
    var actb_bool = new Array();
    var actb_pre = 0;
    var actb_toid;
    var actb_tomake = false;
    var actb_getpre = "";
    var actb_mouse_on_list = true;
    var actb_kwcount = 0;
    var actb_caretmove = false;

    
    /* ---- "Constants" ---- */

    
    actb_keywords = ca;
    actb_curr = obj;
    
    var oldkeydownhandler = document.onkeydown;
    var oldblurhandler = obj.onblur;
    var oldkeyuphandler = obj.onkeyup;

    document.onkeydown = actb_checkkey;
    obj.onblur = actb_clear;
    obj.onkeyup = actb_keypress;

    if (!document.getElementById('tat_table') && actb_expand_onfocus) setTimeout(function(){actb_tocomplete(188)},150);

    
    function actb_clear(evt){
        if (!evt) evt = event;
        document.onkeydown = oldkeydownhandler;
        actb_curr.onblur = oldblurhandler;
        actb_curr.onkeyup = oldkeyuphandler;
        actb_removedisp();
    }
    function actb_parse(n){
        if (actb_delimiter.length > 0){
            var t = actb_delimwords[actb_cdelimword].trim().addslashes();
            var plen = actb_delimwords[actb_cdelimword].trim().length;
        }else{
            var t = actb_curr.value.addslashes();
            var plen = actb_curr.value.length;
        }
        var tobuild = '';
        var i;

        if (actb_firstText){
            var re = new RegExp("^" + t, "i");
        }else{
            var re = new RegExp(t, "i");
        }
        var p = n.search(re);
                
        for (i=0;i<p;i++){
            tobuild += n.substr(i,1);
        }
        tobuild += "<span class='actb_regex_match'>";
        for (i=p;i<plen+p;i++){
            tobuild += n.substr(i,1);
        }
        tobuild += "</span>";
        for (i=plen+p;i<n.length;i++){
            tobuild += n.substr(i,1);
        }
        return tobuild;
    }
    function curTop(){
        actb_toreturn = 0;
        obj = actb_curr;
        while(obj){
            actb_toreturn += obj.offsetTop;
            obj = obj.offsetParent;
        }
        return actb_toreturn;
    }
    function curLeft(){
        actb_toreturn = 0;
        obj = actb_curr;
        while(obj){
            actb_toreturn += obj.offsetLeft;
            obj = obj.offsetParent;
        }
        return actb_toreturn;
    }
    
    function determineWidth(){
       var max=0;
       for (i=0;i<actb_keywords.length;i++){
          lenkw=actb_keywords[i].length;
          if (lenkw>max)
          { max = lenkw }
       }
       max++;
       return max.toString()+'em';
    }
    
    function actb_generate(){

        /*if (document.getElementById('tat_rm_link')) document.body.removeChild(document.getElementById('tat_rm_link'));
        l = document.createElement('a');
        l.style.position='absolute';
        l.style.top = eval(curTop() + 1) + "px";
        l.innerHTML = 'vider';
        l.style.left = eval(curLeft() + actb_curr.offsetWidth + 3) + "px";
        l.id = 'tat_rm_link';
        l.onclick = function () {
            actb_curr.value="";
            setTimeout("document.getElementById('"+actb_curr.id+"').focus()", 250);
        };

        document.body.appendChild(l);*/

        
        if (document.getElementById('tat_table')){ actb_display = false;document.body.removeChild(document.getElementById('tat_table')); } 
        if (actb_kwcount == 0){
            actb_display = false;
            return;
        }
        a = document.createElement('table');
        a.className='actb_table';
        //a.cellSpacing='1px';
        //a.cellPadding='2px';
        a.style.position='absolute';
        a.style.top = eval(curTop() + actb_curr.offsetHeight) + "px";
        a.style.left = curLeft() + "px";
        a.style.width=determineWidth();
        //a.style.backgroundColor=actb_bgColor;
        a.id = 'tat_table';
        document.body.appendChild(a);
        var i;
        var first = true;
        var j = 1;
        if (actb_mouse){
            a.onmouseout= actb_table_unfocus;
            a.onmouseover=actb_table_focus;
        }
        var counter = 0;

        r = a.insertRow(-1);
        c = r.insertCell(-1);
        c.align='center';
        c.className='actb_arrow_placeholder';
        c.innerHTML='&nbsp;';
        
        for (i=0;i<actb_keywords.length;i++){
            if (actb_bool[i]){
                counter++;
                r = a.insertRow(-1);
                if (first && !actb_tomake){
                    r.className = 'actb_active';
                    //r.style.backgroundColor = actb_hColor;
                    first = false;
                    actb_pos = counter;
                }else if(actb_pre == i){
                    r.className = 'actb_active';
                    //r.style.backgroundColor = actb_hColor;
                    first = false;
                    actb_pos = counter;
                }else{
                    //r.style.backgroundColor = actb_bgColor;
                    r.className='';
                }
                r.id = 'tat_tr'+(j);
                c = r.insertCell(-1);
                //c.style.color = actb_textColor;
                //c.style.fontFamily = actb_fFamily;
                //c.style.fontSize = actb_fSize;
                c.innerHTML = actb_parse(actb_keywords[i]);
                c.id = 'tat_td'+(j);
                c.setAttribute('pos',j);
                if (actb_mouse){
                    c.onclick=actb_mouseclick;
                    c.onmouseover = actb_table_highlight;
                }
                j++;
            }
            if (j - 1 == actb_lim && j < actb_total){
                r = a.insertRow(-1);
                //r.style.backgroundColor = actb_bgColor;
                c = r.insertCell(-1);
                c.className = 'actb_arrow_down';
                //c.style.color = actb_textColor;
                //c.style.fontFamily = 'arial narrow';
                //c.style.fontSize = actb_fSize;
                c.align='center';
                //c.innerHTML = '\\/';
                c.innerHTML = '&nbsp;';
                if (actb_mouse){
                    c.onclick = actb_mouse_down;
                }
                break;
            }
            
        }
        actb_rangeu = 1;
        actb_ranged = j-1;
        actb_display = true;
        if (actb_pos <= 0) actb_pos = 1;
    }
    function actb_remake(){
        document.body.removeChild(document.getElementById('tat_table'));

        a = document.createElement('table');
        a.className='actb_table';
        a.cellSpacing='1px';
        a.cellPadding='2px';
        a.style.position='absolute';
        a.style.top = eval(curTop() + actb_curr.offsetHeight) + "px";
        a.style.left = curLeft() + "px";
        a.style.width=determineWidth(); 
        //a.style.backgroundColor=actb_bgColor;
        a.id = 'tat_table';
        if (actb_mouse){
            a.onmouseout= actb_table_unfocus;
            a.onmouseover=actb_table_focus;
        }
        document.body.appendChild(a);
        var i;
        var first = true;
        var j = 1;
        if (actb_rangeu > 1){
            r = a.insertRow(-1);
            //r.style.backgroundColor = actb_bgColor;
            c = r.insertCell(-1);
            c.className = 'actb_arrow_up';
            //c.style.color = actb_textColor;
            //c.style.fontFamily = 'arial narrow';
            //c.style.fontSize = actb_fSize;
            c.align='center';
            //c.innerHTML = '/\\';
            c.innerHTML='&nbsp;';
            if (actb_mouse){
                c.onclick = actb_mouse_up;
            } 
        }
        else
        {
            r = a.insertRow(-1);
            c = r.insertCell(-1);
            c.align='center';
            c.className='actb_arrow_placeholder';
            c.innerHTML='&nbsp;';
        }
        //alert('actb_rangeu:'+actb_rangeu+' actb_ranged:'+actb_ranged);
        //alert('total:'+actb_total);
        //alert(j);
        for (i=0;i<actb_keywords.length;i++){
            if (actb_bool[i]){
                if (j >= actb_rangeu && j <= actb_ranged){
                    r = a.insertRow(-1);
                    //r.style.backgroundColor = actb_bgColor;
                    r.id = 'tat_tr'+(j);
                    c = r.insertCell(-1);
                    //c.style.color = actb_textColor;
                    //c.style.fontFamily = actb_fFamily;
                    //c.style.fontSize = actb_fSize;
                    c.innerHTML = actb_parse(actb_keywords[i]);
                    c.id = 'tat_td'+(j);
                    c.setAttribute('pos',j);
                    if (actb_mouse){
                        c.onclick=actb_mouseclick;
                        c.onmouseover = actb_table_highlight;
                    }
                    //alert('j:'+j+' kwd:'+actb_keywords[i]);
                    j++;
                }else{
                    j++;
                }
            }
            if (j > actb_ranged) break;
        }
        
        if (actb_ranged < actb_total){
            r = a.insertRow(-1);
            c = r.insertCell(-1);
            c.className = 'actb_arrow_down';
            c.align='center';
            c.innerHTML= '&nbsp;';
            if (actb_mouse){
                c.onclick = actb_mouse_down;
            }
        }
        else
        {
            r = a.insertRow(-1);
            c = r.insertCell(-1);
            c.align='center';
            c.innerHTML='&nbsp;';
            c.className='actb_arrow_placeholder';
        }       
    }
    function actb_goup(){
        if (!actb_display) return;
        if (actb_pos == 1) return;
        document.getElementById('tat_tr'+actb_pos).className = '';
        //document.getElementById('tat_tr'+actb_pos).style.backgroundColor = actb_bgColor;
        actb_pos--;
        if (actb_pos < actb_rangeu) actb_moveup();
        //document.getElementById('tat_tr'+actb_pos).style.backgroundColor = actb_hColor;
        document.getElementById('tat_tr'+actb_pos).className = 'actb_active';
        if (actb_toid) clearTimeout(actb_toid);
        if (actb_timeOut > 0) actb_toid = setTimeout(function(){actb_mouse_on_list=0;actb_removedisp();},actb_timeOut);
    }
    function actb_godown(){
        if (!actb_display) return;
        if (actb_pos == actb_total) return;
        //document.getElementById('tat_tr'+actb_pos).style.backgroundColor = actb_bgColor;
        document.getElementById('tat_tr'+actb_pos).className = '';
        actb_pos++;
        if (actb_pos > actb_ranged) actb_movedown();
        //document.getElementById('tat_tr'+actb_pos).style.backgroundColor = actb_hColor;
        document.getElementById('tat_tr'+actb_pos).className = 'actb_active';
        if (actb_toid) clearTimeout(actb_toid);
        if (actb_timeOut > 0) actb_toid = setTimeout(function(){actb_mouse_on_list=0;actb_removedisp();},actb_timeOut);
    }
    function actb_movedown(){
        actb_rangeu++;
        actb_ranged++;
        actb_remake();
    }
    function actb_moveup(){
        actb_rangeu--;
        actb_ranged--;
        actb_remake();
    }

    /* Mouse */
    function actb_mouse_down(){
        document.getElementById('tat_tr'+actb_pos).className = '';
        //document.getElementById('tat_tr'+actb_pos).style.backgroundColor = actb_bgColor;
        actb_pos++;
        actb_movedown();
        document.getElementById('tat_tr'+actb_pos).className = 'actb_active';
        //document.getElementById('tat_tr'+actb_pos).style.backgroundColor = actb_hColor;
        actb_curr.focus();
        actb_mouse_on_list = 0;
        if (actb_toid) clearTimeout(actb_toid);
        if (actb_timeOut > 0) actb_toid = setTimeout(function(){actb_mouse_on_list=0;actb_removedisp();},actb_timeOut);
    }
    function actb_mouse_up(evt){
        if (!evt) evt = event;
        if (evt.stopPropagation){
            evt.stopPropagation();
        }else{
            evt.cancelBubble = true;
        }
        document.getElementById('tat_tr'+actb_pos).className = '';
        //document.getElementById('tat_tr'+actb_pos).style.backgroundColor = actb_bgColor;
        actb_pos--;
        actb_moveup();
        document.getElementById('tat_tr'+actb_pos).className = 'actb_active';
        //document.getElementById('tat_tr'+actb_pos).style.backgroundColor = actb_hColor;
        actb_curr.focus();
        actb_mouse_on_list = 0;
        if (actb_toid) clearTimeout(actb_toid);
        if (actb_timeOut > 0) actb_toid = setTimeout(function(){actb_mouse_on_list=0;actb_removedisp();},actb_timeOut);
    }
    function actb_mouseclick(evt){
        if (!evt) evt = event;
        if (!actb_display) return;
        actb_mouse_on_list = 0;
        actb_pos = this.getAttribute('pos');
        actb_penter();
    }
    function actb_table_focus(){
        actb_mouse_on_list = 1;
    }
    function actb_table_unfocus(){
        actb_mouse_on_list = 0;
        if (actb_toid) clearTimeout(actb_toid);
        if (actb_timeOut > 0) actb_toid = setTimeout(function(){actb_mouse_on_list = 0;actb_removedisp();},actb_timeOut);
    }
    function actb_table_highlight(){
        actb_mouse_on_list = 1;
        document.getElementById('tat_tr'+actb_pos).className = '';
        //document.getElementById('tat_tr'+actb_pos).style.backgroundColor = actb_bgColor;
        actb_pos = this.getAttribute('pos');
        while (actb_pos < actb_rangeu) actb_moveup();
        while (actb_pos > actb_ranged) actb_mousedown();
        document.getElementById('tat_tr'+actb_pos).className = 'actb_active';
        //document.getElementById('tat_tr'+actb_pos).style.backgroundColor = actb_hColor;
        if (actb_toid) clearTimeout(actb_toid);
        if (actb_timeOut > 0) actb_toid = setTimeout(function(){actb_mouse_on_list = 0;actb_removedisp();},actb_timeOut);
    }
    /* ---- */

    function actb_insertword(a){
        if (actb_delimiter.length > 0){
            str = '';
            l=0;
            for (i=0;i<actb_delimwords.length;i++){
                if (actb_cdelimword == i){
                    str += a;
                    l = str.length;
                }else{
                    str += actb_delimwords[i];
                }
                if (i != actb_delimwords.length - 1){
                    str += actb_delimchar[i];
                }
            }
            // Ak Sorpa's fix to prevent &amp;, &lt; and &gt; to appear in the input box
            str = actb_convert_escape_chars(str);
            actb_curr.value = str;
            setCaret(actb_curr,l);
        }else{
            actb_curr.value = a;
        }
        if (actb_curr.onchange) {
            actb_curr.onchange()
        }
        actb_mouse_on_list = 0;
        actb_removedisp();
    }
    function actb_penter(){
        if (!actb_display) return;
        actb_display = false;
        var word = '';
        var c = 0;
        for (var i=0;i<=actb_keywords.length;i++){
            if (actb_bool[i]) c++;
            if (c == actb_pos){
                word = actb_keywords[i];
                break;
            }
        }
        actb_insertword(word);
    }
    function actb_removedisp(){
        if (!actb_mouse_on_list){
            actb_display = false;
            if (document.getElementById('tat_table')){ 
                document.body.removeChild(document.getElementById('tat_table')); 
            }
            /*if (document.getElementById('tat_rm_link')){ 
                setTimeout("document.body.removeChild(document.getElementById('tat_rm_link'))", 250);
            }*/
            if (actb_toid) clearTimeout(actb_toid);
        }
    }
    function actb_keypress(){
        return !actb_caretmove;
    }
    function actb_checkkey(evt){
        if (!evt) evt = event;
        a = evt.keyCode;
        caret_pos_start = getCaretStart(actb_curr);
        actb_caretmove = 0;
        switch (a){
            case 27:  // esc to show the menu
                setTimeout(function(){actb_tocomplete(a)},50);
                break
            case 38:
                actb_goup();
                actb_caretmove = 1;
                return false;
                break;
            case 40:
                actb_godown();
                actb_caretmove = 1;
                return false;
                break;
            case 13:
                actb_penter();
                actb_caretmove = 1;
                return false;
                break;
            case 9:
                if (actb_complete_on_tab && actb_display) {
                    actb_penter();
                    actb_caretmove = 1;
                    return false;
                    break;
                } else {
                  break
                }
            default:
                setTimeout(function(){actb_tocomplete(a)},50);
                break;
        }
    }

    function actb_tocomplete(kc){
        if (kc == 38 || kc == 40 || kc == 13) return;
        var i;
        if (actb_display){ 
            var word = 0;
            var c = 0;
            for (var i=0;i<=actb_keywords.length;i++){
                if (actb_bool[i]) c++;
                if (c == actb_pos){
                    word = i;
                    break;
                }
            }
            actb_pre = word;
        }else{ actb_pre = -1};
        
        actb_mouse_on_list = 0;
        //if (actb_curr.value == ''){
            //actb_mouse_on_list = 0;
            //actb_removedisp();
            //return;
        //}
        if (actb_delimiter.length > 0){
            caret_pos_start = getCaretStart(actb_curr);
            caret_pos_end = getCaretEnd(actb_curr);
            
            delim_split = '';
            for (i=0;i<actb_delimiter.length;i++){
                delim_split += actb_delimiter[i];
            }
            delim_split = delim_split.addslashes();
            delim_split_rx = new RegExp("(["+delim_split+"])");
            c = 0;
            actb_delimwords = new Array();
            actb_delimwords[0] = '';
            for (i=0,j=actb_curr.value.length;i<actb_curr.value.length;i++,j--){
                if (actb_curr.value.substr(i,j).search(delim_split_rx) == 0){
                    ma = actb_curr.value.substr(i,j).match(delim_split_rx);
                    actb_delimchar[c] = ma[1];
                    c++;
                    actb_delimwords[c] = '';
                }else{
                    actb_delimwords[c] += actb_curr.value.charAt(i);
                }
            }

            var l = 0;
            actb_cdelimword = -1;
            for (i=0;i<actb_delimwords.length;i++){
                if (caret_pos_end >= l && caret_pos_end <= l + actb_delimwords[i].length){
                    actb_cdelimword = i;
                }
                l+=actb_delimwords[i].length + 1;
            }
            var t = actb_delimwords[actb_cdelimword].addslashes().trim();
        }else{
            var t = actb_curr.value.addslashes();
        }
        if (actb_firstText){
            var re = new RegExp("^" + t, "i");
        }else{
            var re = new RegExp(t, "i");
        }
        
        actb_total = 0;
        actb_tomake = false;
        actb_kwcount = 0;
        for (i=0;i<actb_keywords.length;i++){
            actb_bool[i] = false;
            if (re.test(actb_keywords[i])){
                actb_total++;
                actb_bool[i] = true;
                actb_kwcount++;
                if (actb_pre == i) actb_tomake = true;
            }
        }
        if (actb_toid) clearTimeout(actb_toid);
        if (actb_timeOut > 0) actb_toid = setTimeout(function(){actb_mouse_on_list = 0;actb_removedisp();},actb_timeOut);
        actb_generate();
    }
}


function actb_addValue(id) {
    var value = document.getElementById(id+'_toadd_widget').value;
    var obj = document.getElementById(id+'_widget_list');
    
    var value_tab = value.split(new RegExp("[;]+", "g"));
    for (var i = 0; i < value_tab.length; i++) {
        _actb_addValue(obj, value_tab[i], id);
    }
    
    actb_updateWidgetValue(id);
    actb_resetWidget(id);
}

function _actb_addValue(obj, value, id) {
    var model = document.getElementById(id+'_widget_delete');
    if (value=='') {
        return;
    }
    var nodes = obj.childNodes;
    for (var i = 0; i < nodes.length; i++) {
        node = nodes[i].firstChild;
        if (node && node.data == value) {
            return;
        }
    }

    var li = document.createElement('li');
    li.appendChild(document.createTextNode(value));
    var a = document.createElement('a');
    a.appendChild(document.createTextNode(' '));
    var sp = document.createElement('span');
    sp.appendChild(document.createTextNode(model.childNodes[0].nodeValue));
    a.title = model.title;
    a.appendChild(sp);
    a.onclick = actb_remove;
    a.className = 'delete_button';
    li.appendChild(a);
    obj.appendChild(li);
}

function actb_remove(e) {
    if (!e) {
        e = window.event;
    }
    var obj = (e.srcElement?e.srcElement:e.target).parentNode;
    var list = obj.parentNode;
    list.removeChild(obj);
    actb_updateWidgetValue(list.id.substr(0, list.id.length-12));
}

function actb_updateWidgetValue(id) {
    var list = document.getElementById(id+'_widget_list');
    var widget = document.getElementById(id+'_widget');
    var empty = document.getElementById(id+'_widget_empty');
    var value='';
    var nodes = list.childNodes;
    var has_items = false;
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i] && nodes[i].firstChild) {
            value = value + nodes[i].firstChild.data + ';';
            has_items = true;
        }
    }
    if (has_items) {
        empty.style.display='none';
    } else {
        empty.style.display='block';
    }    
    if (value.length > 0) {
        value = value.substring(0, value.length - 1);
    }
    widget.value = value;
}

function actb_updateListFromValue(id) {
    var list = document.getElementById(id+'_widget_list');
    var widget = document.getElementById(id+'_widget');
    if (widget.value.length == 0) {
        return;
    }
    var value_tab = widget.value.split(new RegExp("[;]+", "g"));
    for (var i=0; i<value_tab.length; i++) {
        _actb_addValue(list, value_tab[i], id);
    }
    actb_updateWidgetValue(id);
}

function actb_resetWidget(id) {
    var obj = document.getElementById(id+'_toadd_widget');
    obj.value="";
}

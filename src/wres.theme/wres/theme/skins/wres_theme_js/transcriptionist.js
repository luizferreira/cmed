function clean_textarea(textarea_id, div_id)
{
  var textarea = document.getElementById(textarea_id);
  textarea.value = "";
  set_as_modified(div_id)
}

function save_textarea(textarea_name, encounter_id, script, div_id)
{
  var textareas = document.getElementsByName(textarea_name);
  var extractElement = function(vector) {
    if (vector.length == 1) return vector[0];
    else alert("Error");
  }

  var textarea = extractElement(textareas);
  var xml_request = getXmlHttpRequest();

  data = 'encounter_id=' + encounter_id + '&note=' + textarea.value;
  xml_request.open('POST', script, true);
  xml_request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xml_request.send(data);
  set_as_saved(div_id)
}

function set_as_modified(div_id)
{
  var div = document.getElementById(div_id);
  div.style.display = 'block';
}

function set_as_saved(div_id)
{
  var div = document.getElementById(div_id);
    div.style.display = 'none';
}

function select_bar(information_id, frame_id, button_id, bar_id)
{	
  var information = document.getElementById(information_id);
  var button = document.getElementById(button_id);

  var frame = document.getElementById(frame_id);
  var bar = document.getElementById(bar_id);

  // iterar sobre bar colorindo todos de branco, apenas button de verde
  var tds = walkInNodes(bar, ['TD']);
  for (var i=0; i<tds.length; i++)
  {
    if (tds[i].id == button_id) tds[i].style.background = "#CDE2A7";
    else tds[i].style.background = "white";
  }
  
  // iterar sobre frame, ocultando todos, menos information
  var divs = walkInNodes(frame, ['SPAN']);
  for (var i=0; i<divs.length; i++)
  {
    if (divs[i].id == information_id) divs[i].style.display = "block";
    else divs[i].style.display = "none";
  }

  /*if(isHidden(elem)){
    showElement(elem);
  }
  else{
    hideElement(elem);
  }*/

}

function walkInNodes(root_node, nodeName_list){
	var ret = [];
    var newlist = [];
    for(var i=0; i<nodeName_list.length; i++){
        newlist[i] = nodeName_list[i].toUpperCase();
    }
	if(isInList(root_node.nodeName, newlist)){
		ret[0] = root_node;
	}
	if(root_node.nodeName != '#text'){
		if(root_node.hasChildNodes()){
			for(var i=0; i < root_node.childNodes.length; i++){
				var ret_child_nodes = walkInNodes(root_node.childNodes[i], nodeName_list);
				if(ret_child_nodes.length > 0){
					for(var j=0; j < ret_child_nodes.length; j++){
						ret[ret.length] = ret_child_nodes[j];
					}
				}
			}
		}
	}
	return(ret);
}

/* verifica se um item estuma lista */
function isInList(item, list){
	var index = indexof(item, list);
	return index != -1;
}

/* retorna o indice de um item numa lista. -1 se o item nao esta na lista. */
function indexof(item, list){
	for(var i=0; i < list.length; i++){
		if(item == list[i]){
			return i;
		}
	}
	return -1;
}



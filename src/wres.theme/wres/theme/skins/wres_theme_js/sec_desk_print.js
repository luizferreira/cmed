function secDeskPrint(){
	if($(".selected")[1].id == "fieldsetlegend-tomorrow"){
		hoje = $("#hoje-table")[0].outerHTML
		$("#hoje-table").remove()
		print()
		$("#day-tables").append(hoje)
	}
	else{
		amanha = $("#amanha-table")[0].outerHTML
		$("#amanha-table").remove()
		print()	
		$("#day-tables").append(amanha)
	}
}

$(document).ready(function(){

	var other_document = "outro";
	var fieldname = $("span#js_data fieldname").text();
	var select_selector = "select#" + fieldname;

	$(select_selector).change(function(){		
		if (this.value == other_document) {
			$("input#other_document_type").fadeIn();
			$("input#other_document_type").focus();
		}
		else {
			$("input#other_document_type").fadeOut();	
		}
	})

	$("input#other_document_type").change(function(){		
		new_document_type = $("input#other_document_type").val()
/*		if (other_document == "") {
			$("select#document_type").fadeOut();
			$('option[value="outro"]').text(new_document_type);
			$('option[value="outro"]').val(new_document_type);
			$("select#document_type").fadeIn();
		}
		else {*/
		$(select_selector).fadeOut();
		$('option[value="'+other_document+'"]').text("Outro: " + new_document_type);
		$('option[value="'+other_document+'"]').val(new_document_type);				
		$(select_selector).fadeIn();

		other_document = new_document_type;
	})

});

$(document).ready(function(){
	var other_field = "outro";
	var select_selector = "select#insurance";

	$(select_selector).change(function(){		
                if (this.value == other_field) {
			$("input#other_insurance").fadeIn();
			$("input#other_insurance").focus();
		}
		else {
			$("input#other_insurance").fadeOut();	
		}
	})

	$("input#other_insurance").change(function(){		
		new_insurance = $("input#other_insurance").val()
		$(select_selector).fadeOut();
		$('option[value="'+other_field+'"]').text("Outro: " + new_insurance);
		$('option[value="'+other_field+'"]').val(new_insurance);				
		$(select_selector).fadeIn();
                other_field = new_insurance;
	})
});

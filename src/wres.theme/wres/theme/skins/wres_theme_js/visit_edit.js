$(document).ready(function(){
	// TODO: Remover estes campos no buildingblocks.pt
	$("#popup_search_patient").hide()
	$("#popup_quick_register_patient").hide()
	$("#visitBody").hide()
	$("#createPatientBody").hide()

	$("#registerButton").click(function(){
		firstName = $("#firstName").val()
		lastName = $("#lastName").val()
		contactPhone = $("#contactPhone").val()
		patientID = $("#patientID").val()

		$.get("/Plone3/Appointments/dteste/save_quick_patient",
			{"firstName":firstName,"lastName":lastName,"contactPhone":contactPhone,"patientID":patientID},
			function(data){
				data = JSON.parse(data)
				choosePatient(data.name,data.url)
		})
	})
});

function choosePatient(patient_name, patient_url){	
	$("#searchPatient").hide()
    $("#createPatientBody").hide()
    $("#visitBody").show()
    populate(patient_name,patient_url)
    selectPatient(patient_url,patient_name)
}

function createPatient(){	
	$("#searchPatient").hide()
    $("#createPatientBody").fadeIn()
}

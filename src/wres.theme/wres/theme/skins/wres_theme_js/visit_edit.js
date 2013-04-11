//define the table search object, which can implement both functions and properties
// tableSearch = {};


// //initialize the search, setup the current object
// tableSearch.init = function() {
//     //define the properties I want on the tableSearch object
//     this.Rows = document.getElementById('data').getElementsByTagName('tr');
//     this.RowsLength = tableSearch.Rows.length;
//     this.RowsText = [];

//     //loop through the table and add the data to the table search object
//     for (var i = 0; i < tableSearch.RowsLength; i++) {
//         this.RowsText[i] = (tableSearch.Rows[i].innerText) ? tableSearch.Rows[i].innerText.toUpperCase() : tableSearch.Rows[i].textContent.toUpperCase();
//         }
//     }

    

// //onlys shows the relevant rows as determined by the search string
//     tableSearch.runSearch = function() {
//         //get the search term
//         this.Term = document.getElementById('textBoxSearch').value.toUpperCase();
//         lines = tableSearch.RowsLength
//         tabela = document.getElementById('tabela')
//         resultado = document.getElementById('semResultado')
//         //loop through the rows and hide rows that do not match the search query
//         for (var i = 0, row; row = this.Rows[i], rowText = this.RowsText[i]; i++) {
//             if ((rowText.indexOf(this.Term) != -1) || this.Term === ''){
//                 tabela.style.display = "";
//                 resultado.style.display = "none"
//                 row.style.display = 'inline'
//             }
//             else{
//                 row.style.display = 'none' 
//                 lines--  
//             }
//         }
//         if(lines == 0){
//             tabela.style.display = "none";
//             resultado.style.display = "inline"
//         }

//         total = document.getElementById('total')
//     total.innerText = "Total: " + (lines)
//     }

//     //handles the enter key being pressed
//     //Check if there is more than 3 letters to start search
//     tableSearch.search = function(e) {
//     input = $("#textBoxSearch")
//     if(input.val().length >= 3) tableSearch.runSearch();
//     }

// $(document).unbind("keypress.key13");

$(document).ready(function(){
//-------------Search table stuff----------------------
// tableSearch.init();
// total = document.getElementById('total')
// total.innerText = "Total: " + tableSearch.RowsLength

// tabela = document.getElementById('tabela')
// resultado = document.getElementById('semResultado')
// if(tableSearch.RowsLength == 0){
//             tabela.style.display = "none";
//             resultado.style.display = "inline"
//         }

//------------------------------------------------------
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

$("#registerButton2").click(function(){
	
	
})

});

function choosePatient(patient_name, patient_url){	
	$("#searchPatient").hide()
    $("#createPatientBody").hide()
    $("#visitBody").show()
    populate(patient_url,patient_name)
debugger;
    selectPatient(patient_url,patient_name)
}

function createPatient(){	
	$("#searchPatient").hide()
    $("#createPatientBody").fadeIn()
}

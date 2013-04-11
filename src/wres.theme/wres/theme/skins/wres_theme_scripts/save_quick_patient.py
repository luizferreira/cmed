try:
	firstName = context.REQUEST.get("firstName")
	lastName = context.REQUEST.get("lastName")
	contactPhone = context.REQUEST.get("contactPhone")
	patient = context.saveNewDataPatient(firstName,lastName,contactPhone)
	#TODO: Descobrir porque json.dumps nao funciona
	return '{"url":"' + "/".join(patient.getPhysicalPath()) + '","name":"' + patient.getFullName() + '"}'
except:
	return 0


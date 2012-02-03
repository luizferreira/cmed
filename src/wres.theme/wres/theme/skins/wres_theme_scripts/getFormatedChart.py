template_data = context.family_history_template_data()
result = template_data

def prepareFamilyHistoryData(template):
	if not template['entries']:
		return []
	entries = template['entries'][0]['data']['fh']
	entries = [dict(entry) for entry in entries]
	for entry in entries:
		temp = [key for key in entry.keys() if entry[key]]
		if len(temp) > 1:
			entry['filled'] = temp
		else:
			entry['filled'] = []
	return entries
									
def prepareFamilyDiseasesData(template):
	if not template['entries']:
		return []
	entries = template['entries'][0]['data']['fd']
	entries = [dict(entry) for entry in entries]
	count = 0
	for entry in entries:
		temp = []
		integer = 0
		for number in entry['number']:
			if (number):
				temp.append(str(number)+' - '+str(entry['disease'][integer]))
			integer = integer + 1
		entry['filled'] = temp
		count = count + 1
	return entries

def prepareMedicamentAndAllergies():
	data = context.get_formatted_questionnaire_data()
##	from Products.zdb import set_trace; set_trace()
	taking = []
	allergic = []
	for medicine in data['medications']:
		if medicine['taking_or_allergic'] == 'taking':
			taking.append(medicine['medicine'])
		elif medicine['taking_or_allergic'] == 'allergic':
			allergic.append(medicine['medicine'])
	return {"taking_list": taking, "allergic_list": allergic}

def preparePastMedicalHistory():
	#set_trace()
	addill = context.get_formatted_questionnaire_data()['additional_illness']
	hospit = context.get_formatted_questionnaire_data()['hospitalizations']
	if not addill:
		addill = []
	if not hospit:
		hospit = []
	def cleanAdditionalIllnessList(list):
		return [item for item in list if item]
	def cleanHospitalizationsList(list):
		built = []
		for item in list:
			built.append([name for name in item.keys() if item[name]])
		return [list[i] for i in xrange(len(list)) if built[i]]
	return {'addill': cleanAdditionalIllnessList(addill), 'hospit': cleanHospitalizationsList(hospit)}

def prepareSocialHistory():
	returned = {}
	temporary = context.getSocialHistory()
	for key_date, item in temporary.items():
		if item.get('came_from','nichts')=='questionnaire':
			returned = item['data']
	return returned

result['FormatedHistory'] = prepareFamilyHistoryData(template_data)
result['FormatedDiseases'] = prepareFamilyDiseasesData(template_data)
result['FormatedQuest'] = prepareMedicamentAndAllergies()
result['FormatedPMH'] = preparePastMedicalHistory()
result['FormatedSocialHistory'] = prepareSocialHistory()

return result

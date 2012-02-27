#TODO Limpar script
#def filter_duplicated(allergies):
    #aux = {}
    #result = []
    #for allergy in allergies:
        #allergy_id = allergy['allergy']
        #if allergy_id not in aux:
            #aux[allergy_id] = 0
            #result.append(allergy)
        #aux[allergy_id] = aux[allergy_id] + 1
    #return result

#def change_representation(allergy_entry):
    #result = {}
    #result.update(allergy_entry)
    #result['data'] = []
    #for allergy in allergy_entry['data']:
        #if same_type(allergy, ''):
            #result['data'].append({'allergy': allergy,
                                   #'reaction': 'Non Specified'})
        #else:
            #result['data'].append(allergy)
    #return result

#def addStatusInformation(allergies, status):
    #for allergy in allergies:
        #allergy['status'] = status
        #allergy['not_signed'] = (status == 'not_signed')

#patient = context.getPatient()

#allergies_dict = patient.getAllergies()
#allergies_entries = allergies_dict.values()
#allergies = []

#for allergies_entry in allergies_entries:
    #came_from = ''.join(allergies_entry['came_from'])
    #if came_from.lower() != 'questionnaire':
        #allergies.extend(allergies_entry['data'])

#allergies = filter_duplicated(allergies)
#addStatusInformation(allergies, 'signed')
#not_signed_dict = patient.getNotSignedAllergies()
#not_signed_allergies = []

#for allergies_entry in not_signed_dict.values():
    #came_from = ''.join(allergies_entry['came_from'])
    #if came_from.lower() != 'questionnaire':
        #not_signed_allergies.extend(allergies_entry['data'])

#addStatusInformation(not_signed_allergies, 'not_signed')
#allergies = allergies + not_signed_allergies
#allergies = filter_duplicated(allergies)
allergies = context.chart_data.get_entry('allergies')
allergies = allergies.values()
results = []
for allergy in allergies:
    results.append(allergy['data'])
return results

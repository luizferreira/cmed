#questionnaire = context.questionnaire_data()

#def transformFamilyHistory(family_history):
    #return [transformMemberHistory(member) for member in family_history]

#def transformMemberHistory(data):
    #new = dict(data)
    #for key in data.keys():
        #if key.startswith('health_condition'):
            #del new[key]
            #new['health_condition'] = data[key]
    #return new

#def transformFamilyDiseases(family_diseases):
    #new = {}
    #for item in family_diseases:
        #entity_id = item['entity'].split()[0]
        #temp = {}
        #for key, value in zip(item['disease'], item['number']):
            #temp[key] = value
        #new[entity_id] = temp
    #return new

#def getQuestionsAnswers():
    #questions = context.get_questions()
    ##import pdb;pdb.set_trace()
    #for question in questions:
        #meaning, answer = questionnaire.get(question.get('id','nope'),('', ''))
        #question['answer'] = answer
    #return questions

#def transformShots(shots):
    #if not shots:
        #return []
    #preresult = []
    #for key, value in shots.items():
        #if len(value) == 3:
            #position = getShotPosition(key)
            #year = value[1]
            #test = value[2]
            #preresult.append((position, {'year': year,
                                         #'id': test}))
    #preresult.sort()
    #result = [item[-1] for item in preresult]
    #return result

#transformTests = transformImmunizations = transformShots

###from Products.zdb import set_trace; set_trace()
#LIST_OF_SHOTS = context.list_of_tests() + context.list_of_immunizations()
#TEMP_SHOTS_STRUCTURE = {}
#for index, item in enumerate(LIST_OF_SHOTS):
    #TEMP_SHOTS_STRUCTURE[item['varname']] = index
#def getShotPosition(shot):
    #return TEMP_SHOTS_STRUCTURE[shot]

#def transformMedicines(medicines):
    #if not medicines:
         #return []
    #preresult = []
    #for key, value in medicines.items():
        #if len(value) == 2:
            #pos = getMedicinePosition(key)
            #taking_or_allergic = value[0]
            #medicine = value[1]
            #preresult.append((pos, {'taking_or_allergic': taking_or_allergic,
                                    #'medicine': medicine}))
    #preresult.sort()
    #result = [item[-1] for item in preresult]
    #return result

#def isHospitalizationFilled(hosp):
    #for value in hosp.values():
        #if value != '':
            #return True
    #return False

#LIST_OF_MEDICINES = context.list_of_medicines()
#TEMP_MEDICINES_STRUCTURE = {}
#for index, item in enumerate(LIST_OF_MEDICINES):
    #TEMP_MEDICINES_STRUCTURE[item['varname']] = index
#def getMedicinePosition(medicine):
    #return TEMP_MEDICINES_STRUCTURE[medicine]

#result = {}
#family_history = transformFamilyHistory(questionnaire.get('family_history',[]))
#result['family_history'] = family_history
#result['questions_answers'] = getQuestionsAnswers()
#result['self_diseases'] = questionnaire.get('self_diseases', [])
#today = questionnaire.get('today', '')
#if today != '':
    #today = today.strftime('%m/%d/%Y')
#result['today'] = today
#result['user'] = questionnaire.get('user', [])
#family_diseases = questionnaire.get('family_diseases', [])
#result['family_diseases'] = transformFamilyDiseases(family_diseases)
#result['additional_illness'] = filter(lambda x: x, \
                                      #questionnaire.get('additional_illness',\
                                                        #[]))
#meaning, answer = questionnaire.get('additional_comments', ('', ''))
#result['additional_comments'] = answer.strip()
#mtfh = questionnaire.get('more_than_four_hospitalizations')
#result['more_than_four_hospitalizations'] = mtfh
#hospitalizations = questionnaire.get('hospitalizations', [])
#result['hospitalizations'] = filter(isHospitalizationFilled, hospitalizations)
#immunizations = questionnaire.get('immunizations', [])
#result['immunizations'] = transformImmunizations(immunizations)
#result['tests'] = transformTests(questionnaire.get('tests'))
#result['medications'] = transformMedicines(questionnaire.get('medicines',[]))
#return result
#TODO Remover
prescriptions = context.chart_data.get_entry('prescriptions')
prescriptions = prescriptions.values()
return prescriptions

#TODO remover a parte comentada
#from DateTime import DateTime

#def createStructure():
    #today = DateTime()

    #shown_start = today.strftime('%d/%m/%Y')
    #start = today.strftime('%d/%m/%Y')
    #member = context.portal_membership.getAuthenticatedMember()
    #allow_sign = member.has_role('Doctor')
    #return {'shown_start': shown_start,
            #'start': start,
            #'allow_sign': allow_sign,
            #}
#def createGroup(group_name):
    #return {'title': group_name[1],
            #'group_names': group_name,
            #'prescriptions': [],
            #}
#def addGroup(structure, group):
    #title = group['group_names'][0].lower()
    #structure[title] = group

#def isDateTime(obj):
    #return hasattr(obj, 'strftime')

#def addPrescription(group, **prescription):
    #new = dict()
    #new.update(prescription)
    #for key, value in new.items():
        #if isDateTime(value):
            #new[key] = context.format_birthdate(value, '%d/%m/%Y')
    #group['prescriptions'].append(new)

#def dividePrescriptions(prescriptions):
    #current = []
    #historical = []
    #innefective = []
    #for prescription in prescriptions:
        #state = prescription['state']
        #if state == 'current':
            #current.append(prescription)
        #elif state == 'historical':
            #historical.append(prescription)
        #else:
            #innefective.append(prescription)
    #return current, historical, innefective

#prescriptions = context.getPrescriptions()
#current, historical, innefective = dividePrescriptions(prescriptions)

#structure = createStructure()
#group = createGroup(('Current', 'Atual'))
#for prescription in current:
    #addPrescription(group, **prescription)
#addGroup(structure, group)

#group = createGroup(('Historical', 'Histórico'))
#for prescription in historical:
    #addPrescription(group, **prescription)
#addGroup(structure, group)

#group = createGroup(('Innefective', 'Ineficaz'))
#for prescription in innefective:
    #addPrescription(group, **prescription)
#addGroup(structure, group)

#return structure

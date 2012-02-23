from Products.CMFCore.utils import getToolByName

def getVitalSigns():
    vital_signs_data = context.getVitalSignsData()
    dicts = vital_signs_data['vitals']
    return dicts

def getProblemsList():
    problem_list_data = context.getProblemListData()
    active = problem_list_data['active']
    inactive = problem_list_data['inactive']
    active['title'] = 'active_summary_problems'
    inactive['title'] = 'inactive_summary_problems'
    return {'active': active, 'inactive': inactive}

def getMedicationsList():
    medication_data = context.getShowMedicationsData()
    return medication_data
    
def getLaboratory():
    labs_data = context.getLaboratoryData()
    dicts = labs_data['labs']
    return dicts

def getDocumentsList():
    pc = getToolByName(context, 'portal_catalog')
    pw = getToolByName(context, 'portal_workflow')

    brains = pc.searchResults(review_state='draft', path={'query':context.absolute_url(1)}) + \
    pc.searchResults(review_state='pending', path={'query':context.absolute_url(1)}) + \
    pc.searchResults(review_state='signed', path={'query':context.absolute_url(1)})

    retorno = []

    for doc in brains:
        obj = doc.getObject()
        item = {}
        item['type'] = obj.Title()
        item['date'] = obj.date.strftime('%d/%m/%Y')
        item['title'] = str(obj.getDoctor().Title()) + " - " + str(obj.Title())
        item['status'] = pw.getInfoFor(obj, 'review_state', '')
        item['link'] = obj.absolute_url(1)
        retorno.append(item)
    return retorno

def getNewDocumentsList():
    pc = getToolByName(context, 'portal_catalog')
    brains = pc.searchResults({'portal_type': 'GenericDocument', 'path': context.absolute_url(1), 'sort_on':'created', 'sort_order':'ascending'})
    retorno = []
    for doc in brains:
        obj = doc.getObject()
        item = {}
        item['type'] = obj.Title()
        item['date'] = obj.date.strftime('%d/%m/%Y')
        item['doctor'] = str(obj.getDoctor().Title())
        item['link'] = obj.absolute_url(1)
        retorno.append(item)
    return retorno

def getSignedDocumentsList():
    pc = getToolByName(context, 'portal_catalog')
    pw = getToolByName(context, 'portal_workflow')
    
    brains = pc.searchResults(review_state='signed', path={'query':context.absolute_url(1)})

    retorno = []

    for doc in brains:
        obj = doc.getObject()
        item = {}
        item['type'] = obj.getTitle()
        item['date'] = obj.date.strftime('%d/%m/%Y')
        item['title'] = str(obj.getDoctor().Title()) + " - " + str(obj.getTitle())
        item['status'] = pw.getInfoFor(obj, 'review_state', '')
        item['link'] = obj.absolute_url(1)
        retorno.append(item)
    return retorno

pm = getToolByName(context, 'portal_membership')
member= pm.getAuthenticatedMember()
roles_of_member = member.getRoles()
allowed_roles = ['Doctor', 'Manager', 'Transcriptionist', 'UemrAdmin']
authorize = False
for role in allowed_roles:
    if role in roles_of_member:
        authorize = True
        continue

if not authorize:
    from zope.security.interfaces import Unauthorized
    raise Unauthorized

result = {}
result['vital_signs'] = getVitalSigns()
result['problems_list'] = getProblemsList()
result['medications_list'] = getMedicationsList()
result['laboratory'] = getLaboratory()

isPatient = context.verifyRole(["Patient"])

if isPatient:
    result['documents_list'] = getSignedDocumentsList()
else:
    result['documents_list'] = getNewDocumentsList() #Retorna todos os documentos

return result

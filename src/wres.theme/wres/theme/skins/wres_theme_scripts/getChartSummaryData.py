from Products.CMFCore.utils import getToolByName

#TODO: Remover (03/07/2012)
#def getDocumentsList():
    #pc = getToolByName(context, 'portal_catalog')
    #pw = getToolByName(context, 'portal_workflow')

    #brains = pc.searchResults(review_state='draft', path={'query':context.absolute_url(1)}) + \
    #pc.searchResults(review_state='pending', path={'query':context.absolute_url(1)}) + \
    #pc.searchResults(review_state='signed', path={'query':context.absolute_url(1)})

    #retorno = []

    #for doc in brains:
        #obj = doc.getObject()
        #item = {}
        #item['type'] = obj.Title()
        #item['date'] = obj.date.strftime('%d/%m/%Y')
        #item['title'] = str(obj.getDoctor().Title()) + " - " + str(obj.Title())
        #item['status'] = pw.getInfoFor(obj, 'review_state', '')
        #item['link'] = obj.absolute_url(1)
        #retorno.append(item)
    #return retorno

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

#TODO: Remover (03/07/2012)
#def getSignedDocumentsList():
    #pc = getToolByName(context, 'portal_catalog')
    #pw = getToolByName(context, 'portal_workflow')
    
    #brains = pc.searchResults(review_state='signed', path={'query':context.absolute_url(1)})

    #retorno = []

    #for doc in brains:
        #obj = doc.getObject()
        #item = {}
        #item['type'] = obj.getTitle()
        #item['date'] = obj.date.strftime('%d/%m/%Y')
        #item['title'] = str(obj.getDoctor().Title()) + " - " + str(obj.getTitle())
        #item['status'] = pw.getInfoFor(obj, 'review_state', '')
        #item['link'] = obj.absolute_url(1)
        #retorno.append(item)
    #return retorno

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
result['problems'] = context.getProblemListData()
result['medications'] = context.getShowMedicationsData()
result['laboratory'] = context.getExamsData()
result['documents_list'] = getNewDocumentsList()

return result

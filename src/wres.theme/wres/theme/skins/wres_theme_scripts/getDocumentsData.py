#TODO verificar utilidade deste script
#from ZTUtils import Batch

#REQUEST = context.REQUEST
#NUM_RESULTS = 5

#def getSentDocuments():
    #documents = context.getAllDocumentTypes()
    #related_obj = context.getRelatedUserObject()
    ##import pdb; pdb.set_trace()
    #query = {'meta_type': documents,'getWorkflowStatus': 'Pending Review',}
    #return context.portal_catalog.search(query, sort_index='created', reverse=1)

#def getInboxDocuments():
    #related_obj = context.getRelatedUserObject()
    #query = {'getRouted_to': related_obj.UID(),
             #'meta_type': ['ProgressNotes',
                           #'EchoTemplate',
                           #'StressTestingLaboratory',],
              #'getWorkflowStatus': 'Pending Review',
             #}
    #return context.portal_catalog.search(query, sort_index='created', reverse=1)
    
#def getDraftDocuments():
    #member = context.portal_membership.getAuthenticatedMember()
    #query = {'Creator': member.id,
             #'meta_type': ['ProgressNotes',
                           #'EchoTemplate',
                           #'StressTestingLaboratory',
                           #],
             #'getWorkflowStatus': 'Draft',
             #}
    ##from Products.zdb import set_trace; set_trace()
    #return context.portal_catalog.search(query, sort_index='created', reverse=1)

#def extractInformation(brain):
    #def getPatient(pac):
        #dic = {}
        #if pac:
            #dic['title'] = pac.Title()
            #dic['link'] = pac.absolute_url_path() + "/chartFolder"
        #return dic
    #def getDoctor(doc):
        #if doc:
            #return doc.Title()
        #return ''
    #def getDocument(doc):
        #dic = {}
        #if doc:
            #dic['title'] = doc.archetype_name
            #if doc.archetype_name.lower() == 'progress notes':
                #dic['link'] = doc.absolute_url_path() + "/doctypeplastica"
            #else:
                #dic['link'] = doc.absolute_url_path()
        #return dic
    #if hasattr(brain, 'getObject'):
        #obj = brain.getObject()
    #else:
        ##there is a bug that allows duplicated entries of an object to be
        ##returned from catalog. I don't know why this happens.
        #obj = brain
    #info = {}
    #info['date'] = obj.created().strftime("%d/%m/%Y")
    #info['patient'] = getPatient(obj.getPatient())
    #info['doctor'] = getDoctor(obj.getDoctor())
    #info['document'] = getDocument(obj)
    #info['review_notes'] = obj.getReview_notes()
    #return info

#def createNavigationFooter(key, batch, result, start):
    #return {'previous': batch.previous,
            #'next': batch.next,
            #'begin': batch.start,
            #'end': batch.end,
            #'num_results': len(result),
            #'key': key,
            #'current': start+1,
            #}

#def addData(name, documents, destiny):
    #result = {}
    
    #start = int(REQUEST.get(name + '_start', 1)) - 1
    #batch = Batch(documents, size=NUM_RESULTS, start=start)
    #docs = [extractInformation(doc) for doc in batch]
    #result['navigationFooter'] = createNavigationFooter(name, batch, documents, start)
    
    #result['list'] = docs
    #destiny[name] = result

#result = {}
#addData('drafts', getDraftDocuments(), result)
#addData('inbox', getInboxDocuments(), result)
#addData('sent', getSentDocuments(), result)

#return result

## Script (Python) "getWorkflowActionsDocuments"
##bind container=container
##bind context=context
##parameters=document

#def getWorkflowActions():#TODO EXCLUIR
    #transitions = []
    #links = []
    #tuple = (transitions,links)
    #pw = document.portal_workflow
    #workflow = pw.getWorkflowsFor(document)[0]
    #estado_name = pw.getInfoFor(document,'review_state')
    #estado = getattr(workflow.states,estado_name)
    #for t in estado.transitions:
        #if t == 'review':
            #links.append('/route_to')
            #transitions.append(t)
        #if t == 'deny':
            #links.append('/deny_reason')
            #transitions.append(t)
        #if t == 'sign':
            #links.append('/sign_document')
            #transitions.append(t)
    #return tuple

#return getWorkflowActions()

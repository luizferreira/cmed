##parameters=patient

from DateTime import DateTime
return patient.getLastVisitDate()
##visits = patient.getBRefs(relationship='patient')
##dates = []
##
##if visits:
##    for visit in visits:
##        review_state = context.portal_workflow.getInfoFor(visit, 'review_state', '')
##        if review_state == 'running' or review_state == 'concluded':
##            dates.append((visit.getStartDate()).Date())
##    dates.sort()
##    dates.reverse()
##    if dates:
##        result = dates[0]
##        #Muda o formato da data para MM/DD/YYYY
##        result = result[5:] + '/' + result[:4]
##        return result
##return 'No visits concluded'    

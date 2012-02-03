##parameters=doctor_id=None
from DateTime import DateTime
from Products.CMFUEMR.secretary_desktop import VisitWrapper

def getRecentVisits(date):
    start = (date-5).earliestTime()
    end = date.latestTime()
    brains = getEvents(start, end)
    return [VisitWrapper(brain) for brain in brains]

def getEvents(start, end):
    query = {'start': {'query': [start, end],
                       'range': 'min:max'},
             'review_state': ['scheduled',
                              'confirmed',
                              'unconfirmed',
                              'left message',
                              'running',
                              'concluded'],
             }
    if doctor_id is not None:
        query['getProviderId'] = doctor_id
    return context.schedule_catalog.search(query, sort_index = 'LTitle')

##from Products.zdb import set_trace; set_trace()
date = DateTime()
visits = getRecentVisits(date)
visits = [visit for visit in visits if visit.getPatient().Title() != 'No Patient']
return visits

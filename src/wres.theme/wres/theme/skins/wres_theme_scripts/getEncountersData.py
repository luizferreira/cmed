from DateTime import DateTime
from ZTUtils import Batch

REQUEST = context.REQUEST
NUM_RESULTS = 5

def getFakeData1():
    data = {'id': 'fake1',
            'status': 'pending',
            'date': '02/04/2007',
            'patient': {'title': 'Heloisa Helena', 'link': 'helena'},
            'doctors': ['Luis Augsten', 'Ronald Flam'],
            'related_documents': [{'title': 'Progress Notes', 'link': 'notes'}],
            'note': 'texto 1'}
    return data

def getFakeData2():
    data = {'id': 'fake2',
            'status': 'done',
            'date': '12/24/2006',
            'patient': {'title': 'Jesus Christ', 'link': 'christ'},
            'doctors': ['Ronald Flam'],
            'related_documents': [{'title': 'Stress Test', 'link': 'stress'}, {'title': 'Echocardiogram', 'link': 'echo'}],
            'note': 'texto 2'}
    return data

def getRecentEncounters(date, status):
#    from Products.zdb import set_trace; set_trace()
    start = (date-5)
    end = date
    query = {'getDate_of_visit': {'query': [start, end],
                                  'range': 'min:max',
                                  },
             'getStatus': status,
             'meta_type': 'Encounter',
             }
    brains = context.portal_catalog.search(query,
                                           sort_index='getDate_of_visit',
                                           reverse=1)
    return brains

def extractInformation(encounter):
    def getDocuments(doc_list):
        lis = []
#        from Products.zdb import set_trace; set_trace()
        for doc in doc_list:
            dic = {}
            name = doc.archetype_name
            if name.lower() == 'progress notes':
                dic['link'] = doc.absolute_url_path() + "/doctype"
                dic['title'] = doc.getType()
            else:
                dic['link'] = doc.absolute_url_path()
                dic['title'] = name
            
            lis.append(dic)
        return lis
    
    def getPatientInfo(patient):
        dic = {'title': "%s %s" % (patient.getFirstName(), patient.getLastName()),
               'link': patient.absolute_url_path() + "/chartFolder"}
        return dic

    def getDoctors(visits):
        doctors = {}
        for visit in visits:
            doctor_name = visit.getProviderInfo()
            if doctor_name not in doctors:
                doctors[doctor_name] = 1
        return doctors.keys()

    data = {}
    encounter = encounter.getObject()
    patient = encounter.getPatient()
    data['path'] = '/'.join(encounter.getPhysicalPath())
    data['id'] = encounter.getId()
    data['status'] = encounter.getStatus() or 'pending'
    data['date'] = encounter.getDate_of_visit().strftime("%d/%m/%Y")
    data['patient'] = getPatientInfo(encounter.getPatient())
    data['doctors'] = getDoctors(encounter.getVisit())
    data['related_documents'] = getDocuments(encounter.getRelated_documents())
    data['note'] = encounter.getNote()
    return data

def addTableData(result, key):
    encounters = getRecentEncounters(date, key)
    start = int(REQUEST.get('%s_start' % key, 1)) - 1
    batch = Batch(encounters, size=NUM_RESULTS, start=start)

    info = [extractInformation(enc) for enc in batch]
    result[key] = {'list': info,
                   'navigation_footer': {'previous': batch.previous,
                                         'next': batch.next,
                                         'begin': batch.start,
                                         'end': batch.end,
                                         'num_results': len(encounters),
                                         'key': key,
                                         'current': start+1,
                                         },
                   }

def fixOtherCurrent(result):
    pending = result['pending']['navigation_footer']
    done = result['done']['navigation_footer']
    pending['other'] = 'done_start=%s' % done['current']
    done['other'] = 'pending_start=%s' % pending['current']

date = DateTime()
#from Products.zdb import set_trace; set_trace()
result = {}
addTableData(result, 'pending')
addTableData(result, 'done')
fixOtherCurrent(result)

return result

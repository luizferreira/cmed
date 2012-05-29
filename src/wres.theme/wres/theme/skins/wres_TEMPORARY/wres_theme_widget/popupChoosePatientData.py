#from Products.CMFUEMR.utils import do_transformation
from wres.policy.utils.utils import do_transformation
from ZTUtils import Batch

NUM_RESULTS = 20
REQUEST = context.REQUEST
INDEXES = []
def add_index(id, title):
    INDEXES.append({'id': id, 'title': title})
add_index('getParsedLastName', 'Last Name')
add_index('getSocialSecurity', 'SSN')
add_index('getChart', 'Chart Number')

def options():
    result = []
    search_index = REQUEST.get('search_index', 'getLastName')
    for index in INDEXES:
        new_option = {}
        new_option.update(index)
        new_option['selected'] = (search_index == index['id'])
        result.append(new_option)
    return result

def default_values():
    result = {}
    result['previous'] = []
    result['next'] = []
    result['batch'] = []
    result['options'] = options()
    result['search_string'] = REQUEST.get('search_string', '')
    result['search_index'] = REQUEST.get('search_index', 'getLastName')
    return result

def make_search(search_string, search_index):
#    import pdb; pdb.set_trace()
    if search_string == '@Todos':
        search_string = ''
    elif 'LastName' in search_index:
        search_string = do_transformation(search_string)
        search_string += '*'
    else:
        DIGITS = [str(d) for d in xrange(0, 10)]
        search_string = ''.join([c for c in search_string if c in DIGITS])
        if search_index == 'getChart':
            search_string = int(search_string)
    query = {'portal_type': 'Patient',
             search_index: search_string,
             }
    pc = context.portal_catalog
    return pc.search(query, sort_index='LTitle')

def add_item(container, number, item):
    if number % 2 == 0:
        css_class = 'even'
    else:
        css_class = 'odd'
        
    patient = item.getObject()
    
    new_item = {'class': css_class,
                'title': patient.Title,
                'ssn': patient.getSocialSecurity(),
                'chart_number': patient.getChart(),
                'path': item.getPath(),
                'phone': patient.getContactPhone(),
                }
    container.append(new_item)

result = default_values()
search_string = REQUEST.get('search_string', '')
search_index = REQUEST.get('search_index', 'getParsedLastName')
if search_string:
    brains = make_search(search_string, search_index)
    start = REQUEST.get('start', 0)
    batch = Batch(brains, size=NUM_RESULTS, start=start)
    result['batch'] = []
    for index, item in enumerate(batch):
        add_item(result['batch'], index+1, item)
    if batch.previous:
        result['previous'] = {'first': batch.previous.first}
    else:
        result['previous'] = {}
    if batch.next:
        result['next'] = {'first': batch.next.first}
    else:
        result['next'] = {}
    result['start'] = start
    result['result_length'] = len(brains)
return result
##from Products.zdb import set_trace; set_trace()

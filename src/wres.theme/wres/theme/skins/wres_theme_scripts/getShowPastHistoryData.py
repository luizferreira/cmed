GLOBAL_ID2TITLE = {
    'medical_history': 'Medical History',
    'surgical_history': 'Surgical History',
    'ob_gyn_history': 'OB/GYN History',
    'social_history': 'Social History',
    'family_history': 'Family History',
    }


def enum(itera):
    return zip(xrange(len(itera)), itera)
##    return [(i, itera[i]) for i in xrange(len(itera))]

def getHistoryDataSkeleton():
    skeleton = {'title': '',
                'id': '',
                }
    return skeleton

def getHistorySkeleton():
    skeleton = {'number': '',
                'class': '',
                'date': '',
                'came_from': {'href': '', 'content': ''},
                'history': '',
                }
    return skeleton

def fakePastHistory(num):
    result = getHistoryDataSkeleton()
    result['title'] = str(num) * 5
    result['id'] = str(num)
    result['histories'] = [fakeEntry(i) for i in xrange(1, num * 3)]
    return result

def fakeEntry(num):
    result = getHistorySkeleton()
    result['number'] = str(num).zfill(2)
    if num % 2 == 0:
        result['class'] = 'even'
    else:
        result['class'] = 'odd'
    result['date'] = '10/13/2006'
    result['came_from'] = {'href': '', 'content': 'Progress Note'}
    return result

def createHistoryData(id, data):
    result = getHistoryDataSkeleton()
    result['title'] = GLOBAL_ID2TITLE[id]
    result['id'] = id
    result['histories'] = [decorateEntry(i+1, entry) for i, entry \
                           in enum(data)]
    return result

def decorateEntry(number, entry):
    result = getHistorySkeleton()
    result['number'] = str(number).zfill(2)
    if number % 2 == 0:
        result['class'] = 'even'
    else:
        result['class'] = 'odd'
    result['date'] = entry['date'].strftime('%d/%m/%Y')
    came_from = entry['came_from']
    if same_type(came_from, (1,)):
        obj = context.restrictedTraverse(came_from)
        result['came_from']['href'] = obj.absolute_url()
        result['came_from']['content'] = obj.Title()
    else:
        result['came_from']['href'] = ''
        result['came_from']['content'] = ''
    history = entry['data']
    #backward compatibility. Do this to don't do a migration
    if same_type('', history):
        history = [history]
    result['history'] = history
    return result

##result = [fakePastHistory(1), fakePastHistory(2)]
histories = context.chart_data.histories
result = {}
for key, value in histories.items():
    data = createHistoryData(key, value)
    result[data['id']] = data
##from Products.zdb import set_trace; set_trace()
return result

##parameters=options=None
from ZTUtils import Batch
from Products.CMFCore.utils import getToolByName

def addInput(container, type, **kwargs):
    new_input = {}
    new_input['type'] = type
    for key, value in kwargs.items():
        new_input[key] = value
    container.append(new_input)

def createLettersQueryString(inputs):
    base_qs = ''
    for input in inputs:
        if ('name' in input):
            if input['type'] != 'text':
                base_qs += ('&%s=%s' % (input['name'], input['value']))
            else:
                text_var = input['name']
    import string
    letters = []
    for letter in string.ascii_uppercase:
        letter_qs = '%s=%s' % (text_var, letter)
        qs = letter_qs + base_qs
        letters.append({'letter': letter, 'qs': qs})
    return letters

def createBatchQueryString(inputs):
    base_qs = ''
    for input in inputs:
        if ('name' in input):
            base_qs += ('&%s=%s' % (input['name'], input['value']))
    return base_qs

def record2dict(record):
    result = {}
    for key, value in record.items():
        result[key] = value
    return result

result = {}
request = context.REQUEST

if options.get('args'):
    fieldId = options.get('fieldId')
    searchableText = options.get('searchableText')
    sortOn = options.get('sortOn')
    sortOrder = options.get('sortOrder')
    orderBy = options.get('orderBy')
else:
    fieldId = request.get('fieldId')
    searchableText = request.get('searchableText', '')
    sortOn = request.get('sortOn', 'id')
    sortOrder = request.get('sortOrder', 'ascending')
    orderBy = request.get('orderBy', '')
searchableText += '*'
if searchableText.startswith('*'):
    searchableText = ''

opener = context.popup_opener()
fieldName = '%s:list' % fieldId
field = opener.getField(fieldId)
widget = field.widget
block = widget.getBlock('popup_search')
metaType = field.allowed_types or None
kws = record2dict(request.get('filter_indexes', {}))
if metaType:
    resultsType = ' / '.join(metaType)
else:
    resultsType = 'all'
pc = getToolByName(context, 'portal_catalog')
if 'Patient' in metaType:
    kws.update({'getLastName': searchableText.lower()})
else:
    kws.update({'SearchableText': searchableText.lower()})
if sortOrder != 'ascending':
    reverse = True
else:
    reverse = False
results = pc.search(kws,
                    sort_index=sortOn,
                    reverse=reverse)

start = int(request.get('start', 0))
batch = Batch(results, size=20, start=start)
previous = batch.previous
next = batch.next
result['resultsType'] = resultsType
result['orderBy'] = orderBy
result['batch'] = batch
result['widget'] = widget
result['start'] = start
result['block'] = block
result['field'] = field
result['fieldName'] = fieldName
result['results'] = results
result['previous'] = previous
result['next'] = next
result['opener_type'] = opener.meta_type
inputs = []
addInput(inputs, 'hidden', name='sortOn', value=sortOn)
addInput(inputs, 'hidden', name='sortOrder', value=sortOrder)
addInput(inputs, 'hidden', name='fieldId', value=fieldId)
addInput(inputs, 'hidden', name='opener_type', value=opener.meta_type)
for meta_type in metaType:
    addInput(inputs, 'hidden', name='filter_indexes.meta_type:record:list',
             value=meta_type)
addInput(inputs, 'text', name='searchableText', value=searchableText.strip('*'),
         size=25)
addInput(inputs, 'submit', klass='searchButton', name='searchButton',
         value='Search')
result['inputs'] = inputs
result['letters'] = createLettersQueryString(inputs)
result['qs'] = createBatchQueryString(inputs)
return result

# from DateTime import DateTime
request = context.REQUEST

mapping = {'medication': 'Med',
           'sig': 'Sig',
#           'number': '#',
#           'refills': 'Refills',
           'start': 'Date',
#           'end': 'End Date',
           'dont_substitute': 'dont_substitute',
           }
special_ones = ['mgsol_text', 'mgsol']

vars = mapping.keys()
prescription = {}
for var in vars:
    prescription[var] = request.get(var, '')

if request['mgsol'] == 'mg':
    prescription['mg'], prescription['sol'] = request['mgsol_text'], ''
else:
    prescription['mg'], prescription['sol'] = '', request['mgsol_text']

#date_vars = ['start', 'end']
date_vars = ['start']
for var in date_vars:
    prescription[var] = DateTime(prescription[var])

return prescription


ENCOUNTERS = [encounter['date_of_visit'].strftime('%d/%m/%Y') for encounter in context.getEncounters()]

def formatEncounterDate(date):
    dd = date[0:2]
    mm = date[3:5]
    yyyy = date[6:10]
    return {'dd': dd, 'mm': mm, 'yyyy': yyyy}

def date2value(date):
    dic = formatEncounterDate(date)
    return dic['dd'] + '/' + dic['mm'] + '/' + dic['yyyy']

def date2text(date):
    dic = formatEncounterDate(date)
    return dic['dd'] + '/' + dic['mm'] + '/' + dic['yyyy']

result = {}
opts = [{'value': date2value(date), 'text': date2text(date)} for date in ENCOUNTERS]
result['reported_opts'] = opts

def isDateTime(obj):
    return hasattr(obj, 'strftime')

request = context.REQUEST
id = request['id']
problem = context.getProblem(id)
problem = problem['data']
#from Products.zdb import set_trace; set_trace()
for key, value in problem.items():
    if isDateTime(value):
        request.set(key, value.strftime('%d/%m/%Y'))
    else:
        request.set(key, value)
if same_type(problem['started'], ''):
    started = problem['started']
else:
    started = problem['started'].strftime('%d/%m/%Y')
request.set('shown_started', started)
result.update(problem)
return result

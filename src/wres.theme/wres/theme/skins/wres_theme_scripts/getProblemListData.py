#ENCOUNTERS = [encounter['date_of_visit'].strftime('%d/%m/%Y') for encounter in context.getEncounters()]

#def formatEncounterDate(date):
    #dd = date[0:2]
    #mm = date[3:5]
    #yyyy = date[6:10]
    #return {'dd': dd, 'mm': mm, 'yyyy': yyyy}

#def date2value(date):
    #dic = formatEncounterDate(date)
    #return dic['dd'] + '/' + dic['mm'] + '/' + dic['yyyy']

#def date2text(date):
    #dic = formatEncounterDate(date)
    #return dic['dd'] + '/' + dic['mm'] + '/' + dic['yyyy']

#def createStructure():
    #opts = [{'value': date2value(date), 'text': date2text(date)} for date in ENCOUNTERS]
    #return {'reported_opts': opts}

#def createGroup(group_name):
    #return {'title': group_name,
            #'problems': [],
###            'encounters': ENCOUNTERS,
            #}
#def addGroup(structure, group):
    #title = group['title'].lower()
    #structure[title] = group

#def isDateTime(obj):
    #return hasattr(obj, 'strftime')

##def getEncountersData(group, problem):
##    temp = {}
##    for encounter in problem['encounters']:
##        temp[encounter['date'].strftime('%m/%d/%Y')] = encounter['value']
##    return [temp.get(date, '') for date in group['encounters']] 

def addProblem(group, **problem):
    new = dict()
    new.update(problem)
    for key, value in new['data'].items():
        if isDateTime(value):
            new['data'][key] = context.format_birthdate(value, '%d/%m/%Y')
##    new['encounters'] = getEncountersData(group, problem)
    group['problems'].append(new)

def divideProblems(problems):
    active = []
    inactive = []
    problems = problems.values()
    for problem in problems:
        date = problem['data']['started']
        if hasattr(date, 'strftime'): #TODO Workaround - algumas datas sao str
            problem['data']['started'] = date.strftime('%d/%m/%Y')
        date = problem['data']['end_date']
        if hasattr(date, 'strftime'): #TODO Workaround - algumas datas sao str
            problem['data']['end_date'] = date.strftime('%d/%m/%Y')
        if problem.get('data').get('state') == 'active':
            active.append(problem)
        else:
            inactive.append(problem)
    return active, inactive

#def fakeProblem(number, state):
#    return {'problem': 'problem %s' % number,
#            'code': 'code %s' % number,
#            'started': 'started %s' % number,
#            'reported': 'reported %s' % number,
#            'submitted_by': 'submitted_by %s' % number,
#            'submitted_on': 'submitted_on %s' % number,
#            'chronicity': 'chronicity %s' % number,
#            'state': state,
#            }

problems = context.chart_data.get_entry('problems')
active, inactive = divideProblems(problems)

structure = {'active': active, 'inactive': inactive}

return structure

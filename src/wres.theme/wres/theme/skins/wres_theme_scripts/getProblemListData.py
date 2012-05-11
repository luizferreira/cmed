def addProblem(group, **problem):
    new = dict()
    new.update(problem)
    for key, value in new['data'].items():
        if isDateTime(value):
            new['data'][key] = DateTime(value).strftime('%d/%m/%Y')
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

problems = context.chart_data.get_entry('problems')
active, inactive = divideProblems(problems)

structure = {'active': active, 'inactive': inactive}

return structure

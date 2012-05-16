request = context.REQUEST
id = request['id']
problem = context.chart_data.get_entry_item(id, 'problems')
problem = problem['data']
if hasattr(problem['started'], 'strftime'):
    problem['started'] = problem['started'].strftime('%d/%m/%Y')
request.set('shown_started', problem['started'])
request.set('problem', problem['problem'])
request.set('code', problem['code'])
return problem

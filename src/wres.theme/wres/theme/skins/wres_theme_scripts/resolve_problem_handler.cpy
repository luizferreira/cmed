from DateTime import DateTime

request = context.REQUEST
id = request['id']
problem = context.getProblem(id)
problem['data']['note'] = request['note']
problem['data']['end_date'] = DateTime(request['end_date'])
problem['data']['state'] = 'inactive'
if 'id' in problem:
    del problem['id']
context.editProblem(id, **problem)
state.set(portal_status_message='Diagnóstico resolvido.')
return state

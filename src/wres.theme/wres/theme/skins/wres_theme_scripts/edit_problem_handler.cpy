from DateTime import DateTime

request = context.REQUEST
id = request['id']
whole_problem = context.getProblem(id)
problem = whole_problem['data']
vars = ['problem', 'code', 'started', 'id', 'submitted_on', 'submitted_by']
problem = {}
for var in vars:
    problem[var] = request[var]
problem['end_date'] = DateTime()
problem['state'] = request['state'][0] #TODO: Por algum motivo o form retorna uma lista com 2 states (debugar isso posteriormente)

date_vars = ['started', 'submitted_on']
for var in date_vars:
    problem[var] = DateTime(problem[var])
whole_problem['data'] = problem
if 'id' in whole_problem.keys():
    del whole_problem['id']
context.editProblem(id, **whole_problem)
state.set(portal_status_message='Diagnóstico editado.')
return state

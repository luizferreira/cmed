from DateTime import DateTime

request = context.REQUEST
id = request['id']
whole_problem = context.getProblem(id)
problem = whole_problem['data']
vars = ['problem', 'code', 'started', 'id', 'submitted_by','state','note']
problem = {}
for var in vars:
    problem[var] = request[var]
problem['end_date'] = DateTime()
date_vars = ['started']
#TODO:Comments Matheus date_vars = ['started', 'submitted_on']
for var in date_vars:
    problem[var] = DateTime(problem[var])
whole_problem['data'] = problem
if 'id' in whole_problem.keys():
    del whole_problem['id']
context.editProblem(id, **whole_problem)
state.set(portal_status_message='Diagnóstico editado.')
return state

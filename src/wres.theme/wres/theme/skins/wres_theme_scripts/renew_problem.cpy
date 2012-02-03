request = context.REQUEST
id = request['id']
problem = context.getProblem(id)

new_problem = {}
new_problem.update(problem['data'])
new_problem['state'] = 'active'
context.saveProblem(**new_problem)

problem['data']['state'] = 'renewed'
 ## from Products.zdb import set_trace; set_trace()
if 'id' in problem.keys():
    del problem['id']
context.editProblem(id, **problem)

state.set(portal_status_message="Diagnóstico Renovado.")
return state

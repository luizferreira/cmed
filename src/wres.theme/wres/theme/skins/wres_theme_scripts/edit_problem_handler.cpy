from DateTime import DateTime

request = context.REQUEST
id = request['id']
whole_problem = context.chart_data.get_entry_item(id, 'problems')
problem = whole_problem['data']
vars = ['problem', 'code', 'started', 'id', 'submitted_by','state','note']
problem = {}
for var in vars:
    problem[var] = request[var]
problem['end_date'] = DateTime()
#TODO:Comments Matheus date_vars = ['started', 'submitted_on']
whole_problem['data'] = problem
if 'id' in whole_problem.keys():
    del whole_problem['id']
context.chart_data.edit_entry(id, 'problems', **whole_problem)
state.set(portal_status_message='Diagnóstico editado.')
return state

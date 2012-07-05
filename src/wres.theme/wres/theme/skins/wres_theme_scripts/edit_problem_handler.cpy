from DateTime import DateTime

request = context.REQUEST
id = request['id']
whole_problem = context.chart_data.get_entry_item(id, 'problems')
vars = ['problem', 'code', 'started', 'id']
problem = whole_problem['data']
for var in vars:
    problem[var] = request[var]
    
date_vars = ['started']
for var in date_vars:
    problem[var] = DateTime(problem[var], datefmt="international")
    
member = context.portal_membership.getAuthenticatedMember()
problem['edited_by'] = member.id
problem['edited_on'] = DateTime()

whole_problem['data'] = problem
if 'id' in whole_problem.keys():
    del whole_problem['id']
context.chart_data.edit_entry(id, 'problems', **whole_problem)
state.set(portal_status_message='Diagnóstico editado.')
return state

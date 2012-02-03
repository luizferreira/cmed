from DateTime import DateTime

request = context.REQUEST
vars = ['problem', 'code', 'started', 'state']
problem = {}
for var in vars:
    problem[var] = request[var]

date_vars = ['started']
for var in date_vars:
    problem[var] = DateTime(problem[var], datefmt="international")

member = context.portal_membership.getAuthenticatedMember()
problem['submitted_by'] = member.id
problem['submitted_on'] = DateTime()
problem['end_date'] = DateTime()
context.saveProblem(**problem)

state.set(portal_status_message='Diagnóstico adicionado.')
return state

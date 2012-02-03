from DateTime import DateTime

request = context.REQUEST
vars = ['exam', 'value', 'date']
exam = {}
for var in vars:
    exam[var] = request[var]

member = context.portal_membership.getAuthenticatedMember()
exam['submitted_by'] = member.id
context.saveLaboratory(**exam)
state.set(portal_status_message='Exame adicionado.')
return state


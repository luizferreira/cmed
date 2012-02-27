from DateTime import DateTime

request = context.REQUEST
vars = ['allergy', 'reaction', 'date']
allergy = {}
for var in vars:
    allergy[var] = request[var]

member = context.portal_membership.getAuthenticatedMember()
allergy['submitted_by'] = member.id
context.chart_data.save_entry(context, 'allergies', **allergy)
state.set(portal_status_message='Alergia adicionada.')
return state


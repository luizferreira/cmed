
## Controller Python Script "save_medication"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=

from DateTime import DateTime

request = context.REQUEST
vars = ['medication', 'concentration', 'quantity', 'use', 'start', 'status']
medication = {}
for var in vars:
    medication[var] = request[var]

member = context.portal_membership.getAuthenticatedMember()
medication['submitted_by'] = member.id
medication['submitted_on'] = DateTime()
medication['note'] = ''
if medication['status'] == 'active':
    medication['end_date'] = ''
else:
    medication['end_date'] = DateTime().strftime('%d/%m/%Y')
    
context.chart_data.save_entry(context, 'medications', **medication)

state.set(portal_status_message='Medicamento adicionado.')
return state


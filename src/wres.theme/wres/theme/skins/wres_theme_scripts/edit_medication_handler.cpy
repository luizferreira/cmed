from DateTime import DateTime

request = context.REQUEST
id = request['id']
whole_medication = context.chart_data.get_entry_item(id, 'medications')
vars = ['medication', 'concentration', 'quantity', 'use', 'start', 'id', 'use_type']
new_medication = whole_medication['data']
for var in vars:
    new_medication[var] = request[var]
    
member = context.portal_membership.getAuthenticatedMember()
new_medication['edited_by'] = member.id
new_medication['edited_on'] = DateTime()

whole_medication['data'] = new_medication
if 'id' in whole_medication.keys():
    del whole_medication['id']
context.chart_data.edit_entry(id, 'medications', **whole_medication)
state.set(portal_status_message='Medicamento editado.')
return state

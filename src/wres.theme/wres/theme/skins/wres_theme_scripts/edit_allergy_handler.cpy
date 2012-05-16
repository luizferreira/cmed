from DateTime import DateTime

request = context.REQUEST
id = request['id']
whole_allergy = context.chart_data.get_entry_item(id, 'allergies')
vars = ['allergy', 'reaction', 'date', 'id']
new_allergy = whole_allergy['data']
for var in vars:
    new_allergy[var] = request[var]
    
member = context.portal_membership.getAuthenticatedMember()
new_allergy['edited_by'] = member.id
new_allergy['edited_on'] = DateTime()

whole_allergy['data'] = new_allergy
if 'id' in whole_allergy.keys():
    del whole_allergy['id']
context.chart_data.edit_entry(id, 'allergies', **whole_allergy)
state.set(portal_status_message='Alergia editada.')
return state

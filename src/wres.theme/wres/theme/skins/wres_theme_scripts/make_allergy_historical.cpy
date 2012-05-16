from DateTime import DateTime

request = context.REQUEST
id = request['id']
allergy = context.chart_data.get_entry_item(id, 'allergies')
member = context.portal_membership.getAuthenticatedMember()
allergy['data']['inactivated_by'] = member.id
allergy['data']['note'] = request['note']
allergy['data']['end_date'] = DateTime().strftime('%d/%m/%Y')
allergy['data']['state'] = 'inactive'
if 'id' in allergy:
    del allergy['id']
context.chart_data.edit_entry(id, 'allergies', **allergy)
state.set(portal_status_message='Alergia enviado para o histórico.')
return state

from DateTime import DateTime

request = context.REQUEST
id = request['id']
medication = context.chart_data.get_entry_item(id, 'medications')
member = context.portal_membership.getAuthenticatedMember()
medication['data']['inactivated_by'] = member.id
medication['data']['note'] = request['note']
medication['data']['end_date'] = DateTime().strftime('%d/%m/%Y')
medication['data']['status'] = 'inactive'
if 'id' in medication:
    del medication['id']
context.chart_data.edit_entry(id, 'medications', **medication)
state.set(portal_status_message='Medicamento enviado para o histórico.')
return state

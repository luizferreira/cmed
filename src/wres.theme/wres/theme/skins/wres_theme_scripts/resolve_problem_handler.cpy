from DateTime import DateTime

request = context.REQUEST
id = request['id']
problem = context.chart_data.get_entry_item(id, 'problems')
member = context.portal_membership.getAuthenticatedMember()
problem['data']['inactivated_by'] = member.id
problem['data']['note'] = request['note']
problem['data']['end_date'] = request['end_date']
problem['data']['state'] = 'inactive'
if 'id' in problem:
    del problem['id']
context.chart_data.edit_entry(id, 'problems', **problem)
state.set(portal_status_message='Diagnóstico resolvido.')
return state
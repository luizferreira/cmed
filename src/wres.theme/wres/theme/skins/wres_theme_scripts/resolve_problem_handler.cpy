from DateTime import DateTime

request = context.REQUEST
id = request['id']
problem = context.chart_data.get_entry_item(id, 'problems')
problem['data']['note'] = request['note']
problem['data']['end_date'] = DateTime(request['end_date'])
problem['data']['state'] = 'inactive'
if 'id' in problem:
    del problem['id']
context.chart_data.edit_entry(id, 'problems', **problem)
state.set(portal_status_message='Diagnóstico resolvido.')
return state
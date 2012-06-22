request = context.REQUEST
result = {}
id = request['id']
problem = context.chart_data.get_entry_item(id, 'problems')
result.update(problem['data'])
result['note'] = request.get('note', '')
if request.get('shown_end_date'):
    result['shown_end_date'] = request.get('shown_end_date')
    result['end_date'] = request.get('end_date')
else:
    right_now = DateTime()
    result['shown_end_date'] = right_now.strftime('%d/%m/%Y')
    result['end_date'] = right_now.strftime('%Y/%m/%d')
result['id'] = id
return result


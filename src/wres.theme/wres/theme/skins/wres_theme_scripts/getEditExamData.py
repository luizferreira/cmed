request = context.REQUEST
id = request['id']
exam = context.chart_data.get_entry_item(id, 'laboratory')
return exam['data']

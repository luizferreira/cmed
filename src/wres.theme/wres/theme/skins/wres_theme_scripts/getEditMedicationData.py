request = context.REQUEST
id = request['id']
medication = context.chart_data.get_entry_item(id, 'medications')
return medication['data']

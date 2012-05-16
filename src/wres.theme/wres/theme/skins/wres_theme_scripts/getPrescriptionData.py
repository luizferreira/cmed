request = context.REQUEST
id = request['id']
prescription = context.chart_data.get_entry_item(id, 'prescriptions')
return prescription
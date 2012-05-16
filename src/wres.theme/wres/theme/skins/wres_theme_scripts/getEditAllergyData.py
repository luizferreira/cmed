request = context.REQUEST
id = request['id']
allergy = context.chart_data.get_entry_item(id, 'allergies')
return allergy['data']

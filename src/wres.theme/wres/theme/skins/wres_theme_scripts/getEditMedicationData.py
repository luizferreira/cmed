request = context.REQUEST
id = request['id']
medication = context.getMedication(id)
return medication['data']

from DateTime import DateTime

request = context.REQUEST
id = request['id']
medication = context.getMedication(id)
medication['data']['note'] = request['note']
medication['data']['end_date'] = DateTime(request['end_date'])
medication['data']['status'] = 'inactive'
if 'id' in medication:
    del medication['id']
context.editMedication(id, **medication)
state.set(portal_status_message='Medicamento enviado para o histórico.')
return state

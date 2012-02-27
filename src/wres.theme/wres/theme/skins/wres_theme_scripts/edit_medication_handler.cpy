from DateTime import DateTime

request = context.REQUEST
id = request['id']
whole_medication = context.chart_data.get_entry_item(id, 'medications')
new_medication = whole_medication['data']
vars = ['medication', 'concentration', 'quantity', 'use', 'start', 'status', 'submitted_on', 'submitted_by', 'id']
new_medication = {}
for var in vars:
    new_medication[var] = request[var]
new_medication['end_date'] = DateTime()

whole_medication['data'] = new_medication
if 'id' in whole_medication.keys():
    del whole_medication['id']
context.chart_data.edit_entry(id, 'medications', **whole_medication)
state.set(portal_status_message='Medicamento editado.')
return state

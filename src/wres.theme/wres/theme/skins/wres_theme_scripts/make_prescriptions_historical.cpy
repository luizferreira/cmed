from DateTime import DateTime

request = context.REQUEST
prescriptions_ids = request['prescriptions']
reason = request['reason']
prescriptions = context.getPrescriptions(prescriptions_ids)
##from Products.zdb import set_trace; set_trace()
for prescription in prescriptions:
    id = prescription.pop('id')
    prescription['state'] = 'historical'
    prescription['reason'] = reason
    context.editPrescription(id, **prescription)
state.set(portal_status_message='As alterações foram salvas.')
return state

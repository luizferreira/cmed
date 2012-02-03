presc = context.createPrescriptionDict()
request = context.REQUEST
id = request['prescription_id']
prescription = context.getPrescription(id)



#from Products.zdb import set_trace; set_trace()
if prescription.get('signed', False):
    presc['id'] = context.generateUniqueId('prescription')
    presc['signed'] = False
    context.savePrescription(**presc)
else:
    context.editPrescription(id, **presc)
state.set(portal_status_message="As alterações foram salvas.")
return state

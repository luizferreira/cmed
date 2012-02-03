#request = context.REQUEST
#prescriptions_ids = request['historical']
#prescriptions = context.getPrescriptions(prescriptions_ids)
#TODO Excluir este script
#for prescription in prescriptions:
     #id = prescription.pop('id')
     #prescription['state'] = 'current'
     #prescription['renewed'] = False
     #context.editPrescription(id, **prescription)
     #prescription['id'] = context.generateUniqueId('prescription')
     #prescription['state'] = 'historical'
     #prescription['renewed'] = True
     #context.savePrescription(**prescription)
#state.set(portal_status_message='As alterações foram salvas.')
#return state

request = context.REQUEST
prescriptions_ids = request['innefective']
prescriptions = context.getPrescriptions(prescriptions_ids)
#TODO Excluir este script#TODO Excluir
#for prescription in prescriptions:
      este scriptid = prescription.pop('id')
     prescription['state'] = 'current'
     prescription['renewed'] = False
     context.editPrescription(id, **prescription)
     prescription['id'] = context.generateUniqueId('prescription')
     prescription['state'] = 'innefective'
     prescription['renewed'] = True
     context.savePrescription(**prescription)
state.set(portal_status_message='Changes Saved')
return state

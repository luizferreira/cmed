#presc = context.createPrescriptionDict()
#request = context.REQUEST
#id = request['prescription_id']
#prescription = context.getPrescription(id)

#if prescription.get('signed', False):
    #presc['id'] = context.generateUniqueId('prescription')
    #presc['signed'] = False
    #context.chart_data.save_entry(context, 'prescriptions', **presc)
#else:
    #context.chart_data.edit_entry(id, 'prescriptions', **presc)
#state.set(portal_status_message="As alterações foram salvas.")
#return state
#TODO EXCLUIR

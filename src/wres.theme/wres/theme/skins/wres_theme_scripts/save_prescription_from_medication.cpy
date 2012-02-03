context.script_to_save_prescription()
##prescription = context.createPrescriptionDict()
##prescription['id'] = context.generateUniqueId('prescription')
##prescription['submitted_by'] = context.portal_membership.getAuthenticatedMember().id
##context.savePrescription(**prescription)
#TODO Excluir este script
state.set(portal_status_message='New prescription added')
return state

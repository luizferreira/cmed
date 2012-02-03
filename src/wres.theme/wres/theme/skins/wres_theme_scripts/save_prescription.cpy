## Controller Python Script "save_prescription"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
#TODO Excluir este script
#prescription = context.createPrescriptionDict()
#prescription['id'] = context.generateId('prescription')
#prescription['submitted_by'] = context.portal_membership.getAuthenticatedMember().id
#context.savePrescription(**prescription)

# retorna mensagem de sucesso
state.set(portal_status_message='Nova prescrição adicionada com sucesso.')

return state
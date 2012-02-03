##parameters=current=[]
#TODO Excluir este script
#if len(current) == 0:
    message = 'Você deve selecionar pelo menos uma prescrição.'
    state.setError('current_error_message', message, new_status='failure')
    state.set(portal_status_message='Por favor, corrija o(s) erro(s) abaixo.')
#from Products.zdb import set_trace; set_trace()
# retirando restrição de assinatura
#for id in current:
#    if not context.getPrescription(id)['signed']:
#        message = 'Prescrições não assinadas não podem ser impressas.'
#        state.setError('current_error_message', message, new_status='failure')
#        state.set(portal_status_message='Por favor, corrija o(s) erro(s) abaixo.')
return state

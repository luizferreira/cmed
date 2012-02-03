##parameters=innefective=[]
#TODO Excluir este script
#if len(innefective) == 0:
    message = 'Você precisa selecionar pelo menos uma prescrição.'
    state.setError('innefective_error_message', message, new_status='failure')
    state.set(portal_status_message='Por favor, corrija o(s) erro(s) abaixo.')
return state
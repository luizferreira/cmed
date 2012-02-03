request = context.REQUEST
if request['medication'] == '' or request['quantity'] == '' or request['concentration'] == '' or request['use'] == '':
    state.setError('error_message', 'Preencha corretamente os dados do medicamento.', new_status='failure')
if not (context.TestRoles()):
    state.setError('error_message', 'Você não possui esta permissão.', new_status='failure')
return state
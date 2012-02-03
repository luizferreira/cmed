if not (context.TestRoles()):
    state.setError('error_message', 'Você não possui esta permissão.', new_status='failure')
try:
    context.REQUEST['checks']
except KeyError:
    state.setError('error_message', 'Pelo menos um medicamento deve ser selecionado.', new_status='failure')
return state
from DateTime import DateTime

request = context.REQUEST
if request['exam'] == '' or request['value'] == '' or request['date'] == '':
    state.setError('error_message', 'Preencha corretamente os dados do Exame.', new_status='failure')
if not (context.TestRoles()):
    state.setError('error_message', 'Você não possui esta permissão.', new_status='failure')
return state


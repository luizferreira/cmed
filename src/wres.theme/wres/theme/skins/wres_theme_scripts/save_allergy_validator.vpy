from DateTime import DateTime

request = context.REQUEST
if request['allergy'] == '' or request['reaction'] == '' or request['date'] == '':
    state.setError('error_message', 'Preencha corretamente os dados da alergia.', new_status='failure')
if not (context.TestRoles()):
    state.setError('error_message', 'Você não possui esta permissão.', new_status='failure')
def isValidDate(str_date):
    try:
        date = DateTime(str_date)
    except:
        return False
    if date.year() < 1900:
        return False
    return True

if not isValidDate(request['date']):
    state.setError('error_message', 'Data invalida.', new_status='failure')
    return state

return state


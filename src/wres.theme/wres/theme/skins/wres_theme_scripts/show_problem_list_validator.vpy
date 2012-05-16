from DateTime import DateTime
request = context.REQUEST
vars = ['problem', 'code', 'started']
empties = [var for var in vars if not request.get(var, '')]
if len(empties) > 0:
    message = 'Preencha corretamente o diagnóstico'
    state.setError('error_message', message, new_status='failure')
date_vars = ['started']
def isValidDate(str_date):
    try:
        date = DateTime(str_date)
        return True
    except:
        message = 'Data inválida.'
        state.setError('error_message', message, new_status='failure')
        return False
wrong_dates = [' '.join(var.split('_')) for var in date_vars \
               if not isValidDate(request.get(var))]
if len(wrong_dates) > 0:
    message = 'Data inválida.'
    state.setError('error_message', message, new_status='failure')
if not (context.TestRoles()):
    state.setError('error_message', 'Você não possui esta permissão.', new_status='failure')
return state

from DateTime import DateTime
request = context.REQUEST
vars = ['problem', 'code', 'started']
empties = [var for var in vars if not request.get(var, '')]
if len(empties) > 0:
##    from Products.zdb import set_trace; set_trace()
    message = 'Preencha corretamente o diagnóstico'
    state.setError('error_message', message, new_status='failure')
date_vars = ['started']
def isValidDate(str_date):
    try:
        date = DateTime(str_date)
        return True
    except:
        return False
wrong_dates = [var for var in date_vars if not isValidDate(request.get(var))]
##from Products.zdb import set_trace; set_trace()
if len(wrong_dates) > 0:
    message = 'Data inválida.'
    state.setError('error_message', message, new_status='failure')
if not (context.TestRoles()):
    state.setError('error_message', 'Você não possui esta permissão.', new_status='failure')
return state

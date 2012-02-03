from DateTime import DateTime
##from Products.zdb import set_trace; set_trace()
request = context.REQUEST
vars = ['note', 'end_date']
empties = [var for var in vars if not request.get(var, '')]
if len(empties) > 0:
##    from Products.zdb import set_trace; set_trace()
    message = 'Todos os campos são necessários: %s' % ', '.join(empties)
    state.setError('error_message', message, new_status='failure')
date_vars = ['end_date']
def isValidDate(str_date):
    try:
        date = DateTime(str_date)
        return True
    except:
        return False
wrong_dates = [' '.join(var.split('_')) for var in date_vars \
               if not isValidDate(request.get(var))]
##from Products.zdb import set_trace; set_trace()
if len(wrong_dates) > 0:
    message = 'Data inválida: %s' % ', '.join(wrong_dates)
    state.setError('error_message', message, new_status='failure')
return state

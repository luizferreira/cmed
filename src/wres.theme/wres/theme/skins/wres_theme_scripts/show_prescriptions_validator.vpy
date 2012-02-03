#TODO Excluir este script
#request = context.REQUEST
mapping = {'medication': 'Medicamento',
           'mgsol': 'Descrição',
           'sig': 'Instruções',
#           'number': '#',
#           'refills': 'Refils',
           'start': 'Início',
#           'end': 'Validade/Data',
           }

#vars = mapping.keys()


empties = [mapping[var] for var in vars if not request.get(var, '')]

if len(empties) > 0:
    message = 'Todos os campos devem ser preenchidos: %s' % ', '.join(empties)
    state.setError('error_message', message, new_status='failure')

#date_vars = ['start', 'end']
date_vars = ['start']
def isValidDate(str_date):
    try:
        date = DateTime(str_date)
        return True
    except:
        return False
        
wrong_dates = [mapping[var] for var in date_vars \
               if not isValidDate(request.get(var))]

if len(wrong_dates) > 0:
    message = 'Data inválida: %s' % ', '.join(wrong_dates)
    state.setError('error_message', message, new_status='failure')               

if state.status == 'failure':
    portal_status_message = 'Por favor, corrija o erro abaixo.'
    state.set(portal_status_message=portal_status_message)

return state

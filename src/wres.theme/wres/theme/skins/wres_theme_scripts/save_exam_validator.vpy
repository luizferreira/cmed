from DateTime import DateTime

request = context.REQUEST
all_items = request.items()

exams = []
values = []
dates = []


#Esta funcao existe para proteger caso o request nao venha ordenado.
def organize(exams,values,dates):
    for tuple in exams:
        number = tuple[0].split("exam_form")[1]
        for tuple_date in dates:
            if(tuple_date[0] == "date_form"+str(number)):
                dates.remove(tuple_date)
                dates.append(tuple_date)
        for tuple_value in values:
            if(tuple_value[0] == "value_form"+str(number)):
                values.remove(tuple_value)
                values.append(tuple_value)

for tupla in all_items:
    if("exam_form" in tupla[0]):
        exams.append(tupla)
    elif("value_form" in tupla[0]):
        values.append(tupla)
    elif("date_form" in tupla[0]):
        dates.append(tupla)

organize(exams,values,dates)


pack = zip(exams,values,dates)
exams_length = len(exams)

def isValidDate(str_date):
    try:
        date = DateTime(str_date)
    except:
        return False
    if date.year() < 1900:
        return False
    return True

n_items = len(pack)
n_empty = 0


for tuple in pack:
    exam = {}
    if (tuple[0][1] == "" and tuple[1][1] == ""):
        n_empty += 1
        continue
    if ((tuple[0][1] == "" and tuple[1][1] != "") or (tuple[0][1] != "" and tuple[1][1] == "")):
        state.setError('error_message', 'Preencha corretamente os dados do Exame.', new_status='failure')
        return state
    if not isValidDate(tuple[2][1]):
        state.setError('error_message', 'Data '+ tuple[2][1] +' invalida.', new_status='failure')
        return state
    
if n_empty == n_items:
        state.setError('error_message', 'Campos em branco', new_status='failure')
        return state
        
return state




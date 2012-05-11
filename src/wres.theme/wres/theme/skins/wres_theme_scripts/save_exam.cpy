from DateTime import DateTime

request = context.REQUEST

all_items = request.items()

exams = []
values = []
dates = []
all_exams_data = []

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

for tuple in pack:
    exam = {}
    #Ignorar possivel ultimo campo vazio
    if (tuple[0][1] == "" and tuple[1][1] == ""):
        continue
    exam["exam"] = tuple[0][1]
    exam["value"] = tuple[1][1]
    exam["date"] = tuple[2][1]
    all_exams_data.append(exam)
    
#///////////////////////////////////////////////////////////////////////////////////////
member = context.portal_membership.getAuthenticatedMember()
exam['submitted_by'] = member.id
exam['submitted_on'] = DateTime()

for exam in all_exams_data:
    context.chart_data.save_entry(context, 'laboratory', **exam)
state.set(portal_status_message='Exame adicionado.')
return state


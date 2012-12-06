## Script (Python) "create_encounter"
##

results = context.Doctors.list_doctors()

def get_vocabulary(obj):
    for f in obj.getSchemaFields():
        if f.getName() == 'specialty1':
            return f.vocabulary
    return None

doctors_list = []

for result in results:
    doc = result.getObject()
    dic = {}
    dic['title'] = doc.Title()
    dic['email'] = doc.getEmail()
    dic['curriculum'] = []
    dic['photo'] = doc.getPhoto()
    dic['photo_path'] = doc.getPhoto().absolute_url()

    vocabulary = get_vocabulary(doc)
    dic['specialty1'] = vocabulary.getValue(doc.getSpecialty1())
    if doc.getSpecialty2() == '':
        dic['specialty2'] = ''
    else:
        dic['specialty2'] = vocabulary.getValue(doc.getSpecialty2())

    for course_dic in doc.getCurriculum():
        string = ''
        if course_dic['tipo'] == '':
            continue
        elif course_dic['tipo'] == 'college':
            string = 'Formado em '
        else:
            string = 'Especialista em '

        string += course_dic['course'] + ' pelo(a) ' + course_dic['inst'] + '.'
        dic['curriculum'].append(string)    

    doctors_list.append(dic)

doctors_list.reverse()
return doctors_list

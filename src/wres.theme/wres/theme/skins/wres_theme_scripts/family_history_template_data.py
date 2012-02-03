def create_structure(title):
    return {'title': title,
            'entries': [],
            }

def add_entry(structure, entry):
    structure['entries'].append(entry)

def create_entry(came_from, date, data):
    return {'came_from': came_from,
            'date': date,
            'data': data,
            }

family_history = context.getFamilyHistory()
result = create_structure('Family History')
for data in family_history.values():
    came_from = data['came_from'].lower().capitalize()
    date = data['date']
    str_date = date.strftime('%d/%m/%Y')
    data = data['data']
    entry = create_entry(came_from, str_date, data)
    if came_from != 'Questionnaire':
        add_entry(result, entry)
return result

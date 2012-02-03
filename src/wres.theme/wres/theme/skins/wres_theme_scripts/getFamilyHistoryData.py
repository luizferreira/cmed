def relatives(formated_chart):
    data = formated_chart['FormatedHistory']
    result = []
    for relative in data:
        filled = relative['filled']
        if not filled:
            continue
        new = {}
        new.update(relative)
        new['kinship'] = relative_kinship(relative)
        new['name'] = relative_name(relative)
        new['health_condition'] = relative_health_condition(relative)
        new['dead_information'] = relative.get('age_cause_death', '')
        new['diseases'] = relative.get('diseases', [])
        result.append(new)
    return result

def relative_name(relative):
    entity = relative['entity']
    normal = entity.lower() in ('father', 'mother', 'child1', 'child2',
                                'child3', 'child4', 'spouse')
    if not normal:
        return entity
    return relative['%s_name'%entity.lower()]
def relative_kinship(relative):
    entity = relative['entity']
    normal = entity.lower() in ('father', 'mother', 'child1', 'child2',
                                'child3', 'child4', 'spouse')
    if not normal:
        return 'Brother / Sister'
    if entity.lower() in ('child1', 'child2', 'child3', 'child4'):
        return 'Daugther / Son'
    return entity
def relative_health_condition(relative):
    for key, value in relative.items():
        if key.startswith('health_condition'):
            return value
    return ''


formated_chart = context.getFormatedChart()
result = {}
result['relatives'] = relatives(formated_chart)
result['parents_diseases'] = formated_chart['FormatedDiseases']
return result
##from Products.zdb import set_trace; set_trace()

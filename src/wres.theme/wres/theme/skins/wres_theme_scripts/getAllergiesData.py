#coding utf-8
    
def divideAllergies(allergies):
    active = []
    inactive = []
    for allergy in allergies.values():
        allergy = allergy['data']
        if allergy.get('state') == 'active':
            active.append(allergy)
        else:
            inactive.append(allergy)
    return active, inactive

allergies = context.chart_data.get_entry('allergies')
active, inactive = divideAllergies(allergies)
results = {}
results['active'] = active
results['inactive'] = inactive
return results

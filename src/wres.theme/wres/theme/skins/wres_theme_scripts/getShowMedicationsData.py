#coding utf-8
    
def divideMedications(medications):
    active = []
    inactive = []
    for medication in medications.values():
        medication = medication['data']
        if medication.get('status') == 'active':
            active.append(medication)
        else:
            inactive.append(medication)
    return active, inactive

medications = context.chart_data.get_entry('medications')
active, inactive = divideMedications(medications)
results = {}
results['active'] = active
results['inactive'] = inactive
return results

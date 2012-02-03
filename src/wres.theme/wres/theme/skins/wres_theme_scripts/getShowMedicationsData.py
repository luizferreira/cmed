
def getChartMedications():
    result = []
    chart = context.chart_data
    medications = dict(chart.medications)
    for value in medications.values():
        result.append(value['data'])
    return result
    
def divideMedications(medications):
    active = []
    inactive = []
    for medication in medications:
        if medication.get('status') == 'active':
            active.append(medication)
        else:
            inactive.append(medication)
    return active, inactive

result = {}
medications = getChartMedications()
active, inactive = divideMedications(medications)
result['active'] = active
result['inactive'] = inactive
return result

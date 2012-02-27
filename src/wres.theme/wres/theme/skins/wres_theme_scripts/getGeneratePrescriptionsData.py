request = context.REQUEST
checks = request['checks']

medications = []
if isinstance(checks, str):
    medications.append(context.chart_data.get_entry_item(checks, 'medications'))
else:
    for check in checks:
        medications.append(context.chart_data.get_entry_item(check, 'medications'))
return medications

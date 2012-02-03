request = context.REQUEST
checks = request['checks']

medications = []
if isinstance(checks, str):
    medications.append(context.getMedication(checks))
else:
    for check in checks:
        medications.append(context.getMedication(check))
return medications

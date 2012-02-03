def isDateTime(obj):
    return hasattr(obj, 'strftime')

def formatPrescription(**prescription):
    new = dict()
    new.update(prescription)
    for key, value in new.items():
        if isDateTime(value):
            new[key] = context.format_birthdate(value, '%d/%m/%Y')
    return new

request = context.REQUEST
current = request['current']
result = {}
prescriptions = context.getPrescriptions(current)
prescriptions = [formatPrescription(**p) for p in prescriptions]
result['prescriptions'] = prescriptions
return result

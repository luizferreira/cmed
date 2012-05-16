def isDateTime(obj):
    return hasattr(obj, 'strftime')

def formatPrescription(**prescription):
    new = dict()
    new.update(prescription)
    for key, value in new.items():
        if isDateTime(value):
            new[key] = DateTime(value).strftime('%d/%m/%Y')
    return new

request = context.REQUEST
current = request['current']

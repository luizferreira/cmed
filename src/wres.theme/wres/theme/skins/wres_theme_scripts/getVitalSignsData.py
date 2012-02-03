def createDict(number, vital):
    date = vital['date']
    data = vital['data']
    result = {}
    if number % 2 == 0:
        result['class'] = 'even'
    else:
        result['class'] = 'odd'
    result['number'] = str(number).zfill(2)
    result['date'] = date.strftime('%d/%m/%Y')
    result['blood_pressure'] = data['blood_pressure']
    result['respiratory_rate'] = data['respiratory_rate']
    result['temperature'] = data['temperature']
    result['weight'] =  data['weight']
    result['height'] = data['height']
    result['bmi'] = data['IMC']
    return result

vitals = context.getVitalSigns()
result = {}
result['vitals'] = [createDict(i+1, vital) for i, vital in enumerate(vitals)]
return result

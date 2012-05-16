result = []

notes = dict(context.chart_data.follow_up_notes)
plans = dict(context.chart_data.plans)

temp = {}

for key, value in notes.items():
    note = value.get('data', {}).get('note')
    temp[key] = {'note': note, 'recommendation': key}

for key, value in plans.items():
    data = value.get('data')
    recommendation = data and data[0]
    if temp.has_key(key):
        temp[key]['recommendation'] = recommendation
    else:
        temp[key] = {'recommendation': recommendation, 'note': key}

result = temp.values()
return result;

result = []
labs = context.chart_data.get_entry('laboratory')
for lab in labs.values():
    result.append(lab['data'])
return result

def getExamsData():
    result = []
    chart = context.chart_data
    exams = dict(chart.laboratory)
    for value in exams.values():
        result.append(value['data'])
    return result
return getExamsData()

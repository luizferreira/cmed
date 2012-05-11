#def getQuestionnaireImmunizations():
    #data = context.get_formatted_questionnaire_data()
    #return data['immunizations']

#def getChartImmunizations():
    #result = []
    #chart = context.chart_data
    #immunizations = dict(chart.immunizations)
    #for value in immunizations.values():
        #if value['came_from'] != 'questionnaire':
            #date = value['date']
            #year = date.year()
            #data = value['data']
            #data = [{'id': i, 'year': year} for i in data]
            #result.extend(data)
    #return result

#immunizations = getChartImmunizations()
#result = {}
#result['immunizations'] = immunizations
#return result #TODO EXCLUIR

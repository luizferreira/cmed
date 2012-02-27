request = context.REQUEST
id = request['id']
prescription = context.chart_data.get_entry_item(id, 'prescriptions')
return prescription

#TODO Remover a parte comentada
#def isDateTime(obj):
    #return hasattr(obj, 'strftime')

#request = context.REQUEST
#prescription_id = request['prescription_id']
#prescription = context.getPrescription(prescription_id)
#result = {}
#result.update(prescription)
#start = result['start']
#result['shown_start'] = context.format_birthdate(start, '%d/%m/%Y')
#result['start'] = context.format_birthdate(start, '%Y/%m/%d')
#end = result['end']
#result['shown_date'] = context.format_birthdate(end, '%d/%m/%Y')
#result['end'] = context.format_birthdate(end, '%Y/%m/%d')
#if request.get('mgsol') is None:
    #if result['mg']:
        #result['mgsol_text'] = result['mg']
        #result['mgsol'] = 'mg'
        #request.set('mgsol', 'mg')
    #if result['sol']:
        #result['mgsol_text'] = result['sol']
        #result['mgsol'] = 'sol'
        #request.set('mgsol', 'sol')
    #result['delta'] = int(end - start)
    #request.set('is_what', 'days')
    #request.set('dont_substitute', result['dont_substitute'])
#return result

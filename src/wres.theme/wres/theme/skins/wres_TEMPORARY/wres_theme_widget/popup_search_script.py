## Script (Python) "popup_search_script"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field, searchable_text='', replace_variables=False, sort_on='id', order_by='id'
##title=Pop up search script
##
list_values = {}
qs = {}
qs['sortOn'] = sort_on
qs['sortOrder'] = 'ascending'
qs['orderBy'] = order_by
qs['fieldId'] = field.getName()
qs['searchableText'] = searchable_text
widget = field.widget
block = widget.getBlock('popup_search')
indexes = block.get('filter_indexes', {})
indexes.update({'meta_type': field.allowed_types})
for index, value in indexes.items():
    if same_type(value, ()) or same_type(value, []):
        str_index = "filter_indexes.%s:record:list" % index
        list_values[str_index] = value
##        for element in value:
##            qs[str_index] = element
    else:
        str_index = "filter_indexes.%s:record" % index
        if replace_variables:
            related = context.get_related_field(field)
            if related is not None:
                accessor = related.accessor
                qs[str_index] = context[accessor]()
            else:
                qs[str_index] = value
        else:
            qs[str_index] = value

saida = '&'.join(["%s=%s"%(key, value) for key, value in qs.items()])
for var_name, var_list in list_values.items():
    for value in var_list:
        saida += '&' + var_name + '=' + value
return saida
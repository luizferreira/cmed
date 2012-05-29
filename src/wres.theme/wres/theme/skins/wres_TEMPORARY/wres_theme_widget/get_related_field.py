##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field
##
result = None
widget = field.widget
block = widget.getBlock('popup_search')
filter = block.get('filter_indexes', False)
if filter:
    for value in filter.values():
        if same_type(value, 'string') and value.startswith('$'):
            result = context.getField(value[1:])
            break
return result

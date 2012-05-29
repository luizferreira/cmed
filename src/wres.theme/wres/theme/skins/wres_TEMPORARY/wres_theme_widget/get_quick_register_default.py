##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field
##
request = context.REQUEST
widget = field.widget
block = widget.getBlock('popup_quick_register')
default_values = block.get('default_values', {})
result = []
if default_values:
    for name, description  in default_values.items():
        result.append((name, request.get(name, '')))

return tuple(result)
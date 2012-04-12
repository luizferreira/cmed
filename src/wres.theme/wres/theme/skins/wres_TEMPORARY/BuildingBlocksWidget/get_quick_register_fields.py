##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=opener, field
def getRequiredFields(obj):
    schema = obj.Schema()
    fields = schema.filterFields(required=1)
    return fields

def filterDefaultValues(result, default_values):
    #Esta sendo utilizado somente em visit p/ o quick register de location
    #Verificar se nao deve ser removido depois
    if default_values:
        field_default = []
        for name, description  in default_values.items():
            field_default.append(context.getField(name))
        field_names = default_values.keys()
        func = lambda x: x.getName() not in field_names
        return filter(func, result)
    return result

def getExtraFields(obj, block):
    field_name = block.get('extra_fields', [])
    return [obj.getField(name) for name in field_name]

def getNames(schema):
    """Returns a list of all fields in the given schema."""
    return [f for f in schema.fields()]

def getSortedFields(obj, result):
    return [field for field in getNames(obj.Schema()) if field in result]

request = context.REQUEST
widget = field.widget
block = widget.getBlock('popup_quick_register')

default_values = block.get('default_values', {})

result = getRequiredFields(context)
result = filterDefaultValues(result, default_values)
result+= getExtraFields(context, block)
result = getSortedFields(context, result)

return tuple(result)
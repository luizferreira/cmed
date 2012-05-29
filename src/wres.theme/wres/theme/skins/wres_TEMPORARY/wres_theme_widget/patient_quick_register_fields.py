##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
def getRequiredFields(obj):
    return obj.Schema().filterFields(required=1)

def getExtraFields(obj):
    field_name = ('ext', 'middleName')
    return [obj.getField(name) for name in field_name]

def getNames(schema):
    """Returns a list of all fields in the given schema."""
    return [f for f in schema.fields()]

def getSortedFields(obj, result):
    return [field for field in getNames(obj.Schema()) if field in result]

result = getRequiredFields(context)
result+= getExtraFields(context)
result = getSortedFields(context, result)

return tuple(result)
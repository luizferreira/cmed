##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=record
##
result = {}
for key, value in record.items():
    result[key] = value
return result
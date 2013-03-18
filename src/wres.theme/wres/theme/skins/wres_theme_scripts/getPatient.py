## Script (Python) "getPatient"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None

def getPatient(obj):
    if obj.meta_type == 'Patient':
        return obj
    else:
        return getPatient(obj.aq_inner.aq_parent)


if context.meta_type == "Template":
	return None

if obj is None:
    obj = context
return getPatient(obj)



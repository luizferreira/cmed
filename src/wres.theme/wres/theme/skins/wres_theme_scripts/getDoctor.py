## Script (Python) "getDoctor"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None

def getDoctor(obj):
    if obj.meta_type == 'Doctor':
        return obj
    else:
        return getDoctor(obj.aq_inner.aq_parent)

if obj is None:
    obj = context
import pdb; pdb.set_trace()
return getDoctor(obj)

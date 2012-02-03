## Script (Python) "make_route_to_user"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state_change
##title=
##
def getObject():
    obj = state_change.object
    if obj.meta_type.lower() == 'documenttype':
        return obj.aq_parent
    return obj

def getFields(obj):
    if obj.meta_type.lower() == 'progressnotes':
        return obj.Schemata().get('default').fields()
    elif obj.meta_type.lower() in ['echotemplate', 'stresstestinglaboratory']:
        return obj.Schemata().get('Properties').fields()
    return None

def getSpecificField(name, fields):
    for field in fields:
        if field.getName() == name:
            return field
    return None

obj = getObject()
fields = getFields(obj)
field = getSpecificField('routable', fields)

field.widget.visible['edit'] = 'invisible'

routed = context.REQUEST.get('routable')
obj.setRouted_to(routed[0])
router = context.getRelatedUserObject()
obj.setRouted_by(router.UID())
obj.reindexObject()

return 'done'

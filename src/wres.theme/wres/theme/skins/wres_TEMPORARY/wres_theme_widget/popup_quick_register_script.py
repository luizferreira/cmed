##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field_id


opener = context.popup_opener()
field = opener.getField(field_id)
type_name = 'Patient'
widget = field.widget
#from Products.zdb import set_trace; set_trace()
block = widget.getBlock('popup_quick_register')
location = block.get('location')
path = context.portal_url.getPortalPath()
place_to_create = context.restrictedTraverse(path + location)

id = context.generateUniqueId(type_name)

if place_to_create.portal_factory.getFactoryTypes().has_key(type_name):
    o = place_to_create.restrictedTraverse('portal_factory/' + type_name + '/' + id)
else:
    new_id = place_to_create.invokeFactory(id=id, type_name=type_name)
    if new_id is None or new_id == '':
       new_id = id
    o = getattr(place_to_create, new_id, None)

return o.popup_quick_register_template(field_id=field_id)

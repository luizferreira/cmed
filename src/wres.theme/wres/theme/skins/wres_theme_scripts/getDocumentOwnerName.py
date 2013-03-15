from Products.CMFCore.utils import getToolByName
pc = getToolByName(context,"portal_catalog")
user_id = context.owner_info()['id']

if user_id == "admin":
	return "admin"
else:
 	brain = pc.searchResults({'id':user_id})[0]
 	obj = brain.getObject()
 	return obj.getFullName()

# TODO: Remover a partir de 01/06/2013. Este script foi substituido por um metodo
# no proprio contexto (classe Template em template.py).

# from Products.CMFCore.utils import getToolByName
# pc = getToolByName(context,"portal_catalog")
# user_id = context.owner_info()['id']

# if user_id == "admin":
# 	return "admin"
# else:
#  	brain = pc.searchResults({'id':user_id})[0]
#  	obj = brain.getObject()
#  	return obj.getFullName()

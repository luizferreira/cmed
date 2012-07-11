from Products.CMFCore.utils import getToolByName

path = '/'.join(context.getPhysicalPath())

pc = getToolByName(context, 'portal_catalog')
if path.rfind('documents') > 0:
	brains = pc.searchResults({'portal_type': 'GenericDocument','path': path, 'sort_on':'created', 'sort_order':'ascending'})
else:
	brains = pc.searchResults({'portal_type': 'Impresso', 'path': path, 'sort_on':'created', 'sort_order':'ascending'})
retorno = []
for doc in brains:
    obj = doc.getObject()
    retorno.append(obj)
return retorno
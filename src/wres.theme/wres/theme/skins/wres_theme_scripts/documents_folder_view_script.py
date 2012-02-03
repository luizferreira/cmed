from Products.CMFCore.utils import getToolByName

path = context.absolute_url_path()

pc = getToolByName(context, 'portal_catalog')
if path.rfind('documents') > 0:
	brains = pc.searchResults({'portal_type': 'GenericDocument','path': path, 'sort_on':'created', 'sort_order':'ascending'})
else:
	brains = pc.searchResults({'portal_type': 'Impresso', 'path': path, 'sort_on':'created', 'sort_order':'ascending'})
retorno = []
for doc in brains:
    obj = doc.getObject()
    retorno.append(obj)
    # item = {}
    # item['type'] = obj.Title()
    # item['date'] = obj.date.strftime('%d/%m/%Y')
    # item['doctor'] = str(obj.getDoctor().Title())
    # item['link'] = obj.absolute_url(1)
    # retorno.append(item)
return retorno
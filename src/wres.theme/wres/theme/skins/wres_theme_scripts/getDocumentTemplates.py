from Products.CMFCore.utils import getToolByName

catalog = getToolByName(context,"portal_catalog")
path = '/'.join(context.getPhysicalPath())
query = {'portal_type': 'Template', 'path': path}
results = catalog.searchResults(query)
docs = []
for brain in results:
	docs.append(brain.getObject())
return docs

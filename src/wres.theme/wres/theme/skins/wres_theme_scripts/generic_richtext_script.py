
pc = context.portal_catalog
path = context.absolute_url_path()
base_path = path[:path.find('Patients')]

if path.rfind('documents') > 0:
	document_query = {'portal_type': 'GenericDocument', 'path': path[:path.find('documents')], 'sort_on':'created', 'sort_order':'ascending'}
	template_query = {'portal_type': 'Template', 'path': base_path+'Templates/Consultas', 'sort_on':'created', 'sort_order':'ascending'}
else:
	document_query = {'portal_type': 'Impresso', 'path': path[:path.find('impressos')], 'sort_on':'created', 'sort_order':'ascending'}
	template_query = {'portal_type': 'Template', 'path': base_path+'Templates/Impressos', 'sort_on':'created', 'sort_order':'ascending'}
	
brains = pc.searchResults(document_query)
docs = []
for brain in brains:
	docs.append(brain.getObject())



brains = pc.searchResults(template_query)
templates = []
for brain in brains:
	templates.append(brain.getObject())

result = {}
result['documents'] = docs
result['templates'] = templates

return result

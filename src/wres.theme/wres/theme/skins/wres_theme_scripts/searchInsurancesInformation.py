## Script (Python) "searchInsurancesInformation"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=query='',searchField=''
##title=searchInsurancesInformation
##

def insuranceFields(insurance):
    fields = []
    #fields.append(insurance.getId())
    fields.append(insurance.getName())
    fields.append(insurance.getPhoneNumber())
#   fields.append(insurance.getTipo())
    fields.append(insurance.getWebPage())
#   fields.append(insurance.getFaxNumber())
#   fields.append(insurance.getEmail())
    return (insurance.getId(), fields)

pc = getattr(context, 'portal_catalog')
lis = []
insurances = context.objectValues('Insurance')
results = []

if searchField == 'code':
    results = pc.searchResults(meta_type='Insurance',
                               getId=query)
elif searchField == 'name':
    results = pc.searchResults(meta_type='Insurance',
                               Title=query)
elif searchField == 'type':
    results = pc.searchResults(meta_type='Insurance',
                               getType=query)
else:
    results = pc.searchResults(meta_type='Insurance', sort_on='id', sort_order='descending')

for insurance in insurances:
    if insurance in [brain.getObject() for brain in results]:
        lis.append(insuranceFields(insurance))

return lis

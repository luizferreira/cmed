## Script (Python) "filter_review_documents"
##bind container=container
##bind context=context
##bind script=script
##bind subpath=traverse_subpath
##parameters=items
##

retorno = []

for item in items:
    document_id = item['path'].split('/').pop()

    brains = context.portal_catalog.search({'getId': document_id})
    document_obj = brains[0].getObject()

    if document_obj.getDoctor().getId() == context.portal_membership.getAuthenticatedMember().getId():
        retorno.append(item)

return retorno


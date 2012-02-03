## Script (Python) "getAllDocumentsTypes"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

#Script padrao para buscar os nosso tipos documento

def listDocumentTypes():
    documents = ['InitialVisit', 'ProgressNotes', 'DocPlastica','DocBoletim']
    return documents

return listDocumentTypes()

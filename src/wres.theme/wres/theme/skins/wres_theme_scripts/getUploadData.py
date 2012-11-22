##bind context=context
from Products.CMFCore.utils import getToolByName

pc = getToolByName(context, 'portal_catalog')
imagens = []
other_files = []

def getPatientId(context):
    if context.meta_type == 'Patient':
        return context.getId()
    else:
        return getPatientId(context.aq_inner.aq_parent)

def getFilesAndImages(context):
    #Get Imagens
    portal = context.getPortal()
    patientPath = '/' + portal.getId() + '/Patients/' + getPatientId(context) + '/'
    brains = pc.search({'portal_type': 'Image','path': patientPath})
    index = 0
    for brain in brains:
        parts = brain.getPath().split("/")
        parts.pop(0)
        parts.pop(0)
        path = '/'.join(parts)
        date = brain.created.strftime("%y/%m/%d")
        name = parts[-1].split('.')[0]
        imagens.append((path,date,name,index))
        index = index + 1

    #Get Other Files
    brains += pc.search({'portal_type': 'File','path': patientPath})
    for brain in brains:
        filePath = brain.getURL()
        name = brain.Title
        icon = brain.getIcon
        file = (filePath,name,icon)
        other_files.append(file)
    return [imagens,other_files]

return getFilesAndImages(context)

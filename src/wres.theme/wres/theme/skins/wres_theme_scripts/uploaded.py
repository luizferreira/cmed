##bind context=context
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

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
    patientPath = '/wres/Patients/' + getPatientId(context) + '/'
    brains = pc.search({'portal_type': 'Image','path': patientPath})
    for brain in brains:
        imagePath = portal.absolute_url() + brain.getPath().replace("/"+portal.getId(),"")
        date = brain.created.strftime("%y/%m/%d")
        imagens.append((imagePath,date))

    #Get Other Files
    brains = pc.search({'portal_type': 'File','path': patientPath})
    for brain in brains:
        filePath = portal.absolute_url() + brain.getPath().replace("/"+portal.getId(),"")
        name = brain.id
        icon = brain.getIcon
        file = (filePath,name,icon)
        other_files.append(file)
    return [imagens,other_files]
    
return getFilesAndImages(context)

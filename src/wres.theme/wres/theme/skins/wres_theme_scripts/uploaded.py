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
def getUrl(path):
    url = ""
    for node in path:
        url = url + node + "/"
    return url[:-1] #Remove last slash
def checkOwner(tuple):
    if getPatientId(context) in tuple:
        return True
    return False
    

def getFilesAndImages():
    #Get Imagens
    brains = pc.search({'portal_type': 'Image'})
    for brain in brains:
        image = brain.getObject()
        path = image.getPhysicalPath()
        if not checkOwner(path):
            continue
        URL = "http://localhost:8080" + getUrl(path)
        date = DateTime(image.Date()).strftime("%y/%m/%d")
        imagens.append((URL,date,image.getWidth(),image.getHeight()))
    
    #Get Other Files
    brains = pc.search({'portal_type': 'File'})
    for brain in brains:
        other = brain.getObject()
        path = other.getPhysicalPath()
        if not checkOwner(path):
            continue
        name = other.getFilename()
        icon = other.getIcon()
        URL = "http://localhost:8080" + getUrl(path)
        file = (URL,name,icon)
        other_files.append(file)
    
    return [imagens,other_files]
return getFilesAndImages()

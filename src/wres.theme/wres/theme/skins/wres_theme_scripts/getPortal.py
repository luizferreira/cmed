from Products.CMFCore.utils import getToolByName

def getPortal(self):
    utool = getToolByName(self, 'portal_url')
    return utool.getPortalObject()

return getPortal(context)

from Products.CMFCore.utils import getToolByName

def getPortalURL(self):
    utool = getToolByName(self, 'portal_url')
    return utool

return getPortalURL(context)
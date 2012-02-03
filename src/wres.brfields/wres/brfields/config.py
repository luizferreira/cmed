"""Common configuration constants
"""

PROJECTNAME = 'wres.brfields'

SKINS_DIR = 'skins'
GLOBALS = globals()

try:
    from Products.CMFCore.permissions import AddPortalContent
except:
    from Products.CMFCore.CMFCorePermissions import AddPortalContent

ADD_CONTENT_PERMISSION = AddPortalContent


ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
}

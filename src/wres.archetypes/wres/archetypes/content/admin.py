"""Definition of the Admin content type
"""

from zope.app.component.hooks import getSite
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from AccessControl import ClassSecurityInfo

from wres.archetypes.content import wresuser
from wres.archetypes.interfaces import IAdmin
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.schemas.admin import AdminSchema

from wres.policy.utils.roles import UEMRADMIN_GROUP


schemata.finalizeATCTSchema(
    AdminSchema,
    folderish=True,
    moveDiscussion=False
)


class Admin(wresuser.WRESUser):
    """Admin type for WRES website"""
    implements(IAdmin)

    meta_type = "Admin"
    schema = AdminSchema
    
    security = ClassSecurityInfo()    
    
    def getGroup(self):
        return UEMRADMIN_GROUP    

    def get_home_url(self):
        portal = getSite()
        return '/'.join(portal.getPhysicalPath()) + '/view'
        

atapi.registerType(Admin, PROJECTNAME)

# coding=utf-8
"""Definition of the Secretary content type
"""

from zope.interface import implements

from zope.app.component.hooks import getSite
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from AccessControl import ClassSecurityInfo

from wres.archetypes.interfaces import ISecretary
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser

from wres.archetypes.content.schemas.secretary import SecretarySchema

from wres.policy.utils.roles import SECRETARY_GROUP

class Secretary(wresuser.WRESUser):
    """Secretary type for WRES website"""
    implements(ISecretary)

    meta_type = "Secretary"
    schema = SecretarySchema
    
    security = ClassSecurityInfo()
    
    def getGroup(self):
        return SECRETARY_GROUP

    def get_home_url(self):
        portal = getSite()
        return portal.absolute_url_path() + '/Appointments/sec_desk'

atapi.registerType(Secretary, PROJECTNAME)

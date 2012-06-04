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

from wres.policy.utils.roles import SECRETARY_GROUP, TRANSCRIPTIONIST_ROLE

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

    def at_post_create_script(self):
        wresuser.WRESUser.at_post_create_script(self)
        self.at_post_edit_script()

    def at_post_edit_script(self):
        # self.getIsTranscriptionist

        sec_id = self.getId()
        acl = self.acl_users
        if self.getIsTranscriptionist():
            acl.portal_role_manager.assignRoleToPrincipal(TRANSCRIPTIONIST_ROLE, sec_id)
        elif acl.getUserById(sec_id).has_role(TRANSCRIPTIONIST_ROLE):
            acl.portal_role_manager.removeRoleFromPrincipal(TRANSCRIPTIONIST_ROLE, sec_id)



atapi.registerType(Secretary, PROJECTNAME)

# coding=utf-8
"""Definition of the Transcriptionist content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from AccessControl import ClassSecurityInfo

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import ITranscriptionist
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.archetypes.content.schemas.transcriptionist import TranscriptionistSchema

from wres.policy.utils.roles import TRANSCRIPTIONIST_GROUP

schemata.finalizeATCTSchema(
    TranscriptionistSchema,
    folderish=True,
    moveDiscussion=False
)


class Transcriptionist(wresuser.WRESUser):
    """Transcriptionist type for WRES website"""
    implements(ITranscriptionist)

    meta_type = "Transcriptionist"
    schema = TranscriptionistSchema
    
    security = ClassSecurityInfo()
    
    def getGroup(self):
        return TRANSCRIPTIONIST_GROUP

    def get_home_url(self):
        return self.absolute_url_path() + '/transcriptionist_desktop_view'

atapi.registerType(Transcriptionist, PROJECTNAME)

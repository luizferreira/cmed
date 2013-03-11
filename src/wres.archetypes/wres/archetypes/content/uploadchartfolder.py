"""Definition of the UploadChartFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IUploadChartFolder
from wres.archetypes.config import PROJECTNAME
from wres.policy.utils.roles import DOCTOR_ROLE

UploadChartFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(
    UploadChartFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class UploadChartFolder(folder.ATFolder):
    """Folder to upload files in chart."""
    implements(IUploadChartFolder)

    meta_type = "UploadChartFolder"
    schema = UploadChartFolderSchema

    def manage_afterAdd(self, item=None, container=None):
		self.manage_permission('Delete objects', [DOCTOR_ROLE], acquire=False)
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(UploadChartFolder, PROJECTNAME)

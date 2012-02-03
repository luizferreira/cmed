"""Definition of the ReferringProviderFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IReferringProviderFolder
from wres.archetypes.config import PROJECTNAME

ReferringProviderFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

schemata.finalizeATCTSchema(
    ReferringProviderFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class ReferringProviderFolder(folder.ATFolder):
    """Folder of Referring Providers"""
    implements(IReferringProviderFolder)

    meta_type = "ReferringProviderFolder"
    schema = ReferringProviderFolderSchema

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(ReferringProviderFolder, PROJECTNAME)

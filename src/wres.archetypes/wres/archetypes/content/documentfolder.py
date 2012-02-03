"""Definition of the DocumentFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IDocumentFolder
from wres.archetypes.config import PROJECTNAME

DocumentFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(
    DocumentFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class DocumentFolder(folder.ATFolder):
    """Folder of Medical Documents"""
    implements(IDocumentFolder)

    meta_type = "DocumentFolder"
    schema = DocumentFolderSchema

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(DocumentFolder, PROJECTNAME)

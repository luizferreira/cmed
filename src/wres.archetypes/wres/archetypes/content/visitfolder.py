"""Definition of the VisitFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IVisitFolder
from wres.archetypes.config import PROJECTNAME

VisitFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(
    VisitFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class VisitFolder(folder.ATFolder):
    """Folder of visits"""
    implements(IVisitFolder)

    meta_type = "VisitFolder"
    schema = VisitFolderSchema

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(VisitFolder, PROJECTNAME)

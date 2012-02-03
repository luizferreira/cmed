"""Definition of the AdminFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IAdminFolder
from wres.archetypes.config import PROJECTNAME

AdminFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

AdminFolderSchema['title'].storage = atapi.AnnotationStorage()
AdminFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    AdminFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class AdminFolder(folder.ATFolder):
    """Admins' folder"""
    implements(IAdminFolder)

    meta_type = "AdminFolder"
    schema = AdminFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(AdminFolder, PROJECTNAME)

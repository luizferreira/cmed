"""Definition of the SecretaryFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import ISecretaryFolder
from wres.archetypes.config import PROJECTNAME

SecretaryFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

SecretaryFolderSchema['title'].storage = atapi.AnnotationStorage()
SecretaryFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    SecretaryFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class SecretaryFolder(folder.ATFolder):
    """Secretary's folder for WRES website"""
    implements(ISecretaryFolder)

    meta_type = "SecretaryFolder"
    schema = SecretaryFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(SecretaryFolder, PROJECTNAME)

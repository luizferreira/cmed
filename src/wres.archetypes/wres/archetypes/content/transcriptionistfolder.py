"""Definition of the TranscriptionistFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import ITranscriptionistFolder
from wres.archetypes.config import PROJECTNAME

TranscriptionistFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

TranscriptionistFolderSchema['title'].storage = atapi.AnnotationStorage()
TranscriptionistFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    TranscriptionistFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class TranscriptionistFolder(folder.ATFolder):
    """Transcriptionist's folder for WRES website"""
    implements(ITranscriptionistFolder)

    meta_type = "TranscriptionistFolder"
    schema = TranscriptionistFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(TranscriptionistFolder, PROJECTNAME)

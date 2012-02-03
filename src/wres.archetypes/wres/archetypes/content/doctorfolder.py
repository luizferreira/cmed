"""Definition of the DoctorFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IDoctorFolder
from wres.archetypes.config import PROJECTNAME

DoctorFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

# DoctorFolderSchema['title'].storage = atapi.AnnotationStorage()
# DoctorFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    DoctorFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class DoctorFolder(folder.ATFolder):
    """Doctors' folder"""
    implements(IDoctorFolder)

    meta_type = "DoctorFolder"
    schema = DoctorFolderSchema

#    title = atapi.ATFieldProperty('title')
#    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(DoctorFolder, PROJECTNAME)

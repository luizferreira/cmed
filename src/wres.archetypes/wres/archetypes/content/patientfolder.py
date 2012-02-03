"""Definition of the PatientFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IPatientFolder
from wres.archetypes.config import PROJECTNAME

PatientFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(
    PatientFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class PatientFolder(folder.ATFolder):
    """Patients' folder"""
    implements(IPatientFolder)

    meta_type = "PatientFolder"
    schema = PatientFolderSchema

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(PatientFolder, PROJECTNAME)

"""Definition of the ExamFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IExamFolder
from wres.archetypes.config import PROJECTNAME

ExamFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(
    ExamFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class ExamFolder(folder.ATFolder):
    """Folder of exams"""
    implements(IExamFolder)

    meta_type = "ExamFolder"
    schema = ExamFolderSchema

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(ExamFolder, PROJECTNAME)

"""Definition of the InsuranceFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IInsuranceFolder
from wres.archetypes.config import PROJECTNAME

InsuranceFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

InsuranceFolderSchema['title'].storage = atapi.AnnotationStorage()
InsuranceFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    InsuranceFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class InsuranceFolder(folder.ATFolder):
    """InsuranceFolder"""
    implements(IInsuranceFolder)

    meta_type = "InsuranceFolder"
    schema = InsuranceFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(InsuranceFolder, PROJECTNAME)

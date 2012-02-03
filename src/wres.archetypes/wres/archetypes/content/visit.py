"""Definition of the Visit content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IVisit
from wres.archetypes.config import PROJECTNAME

VisitSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

VisitSchema['title'].storage = atapi.AnnotationStorage()
VisitSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    VisitSchema,
    folderish=True,
    moveDiscussion=False
)


class Visit(folder.ATFolder):
    """Visit type for wres website"""
    implements(IVisit)

    meta_type = "Visit"
    schema = VisitSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Visit, PROJECTNAME)

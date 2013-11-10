##coding=utf-8

"""Definition of the CmedConfiguration content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import ICmedConfiguration
from wres.archetypes.config import PROJECTNAME

CmedConfigurationSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(
    CmedConfigurationSchema,
    folderish=True,
    moveDiscussion=False
)


class CmedConfiguration(folder.ATFolder):
    """Description of the Example Type"""
    implements(ICmedConfiguration)

    meta_type = "CmedConfiguration"
    schema = CmedConfigurationSchema

atapi.registerType(CmedConfiguration, PROJECTNAME)

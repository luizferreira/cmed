"""Definition of the Insurance content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from wres.archetypes.interfaces import IInsurance
from wres.archetypes.config import PROJECTNAME

from wres.archetypes.content.schemas.insurance import InsuranceSchema

schemata.finalizeATCTSchema(InsuranceSchema, moveDiscussion=False)


class Insurance(base.ATCTContent):
    """Insurance"""
    implements(IInsurance)

    meta_type = "Insurance"
    schema = InsuranceSchema

    def at_post_create_script(self):
            self.setTitle(self.getName())
    
#    def at_post_create_script(self):
#        self.setId(self.getName())


atapi.registerType(Insurance, PROJECTNAME)

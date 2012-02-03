"""Definition of the Clinic content type
"""

from Products.DataGridField import DGFMessageFactory as _

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from wres.archetypes.content.schemas.clinic import ClinicSchema

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IClinic
from wres.archetypes.config import PROJECTNAME

class Clinic(base.ATCTContent):
    """Clinic type for WRES Website"""
    implements(IClinic)

    meta_type = "Clinic"
    schema = ClinicSchema

    def getSampleVocabulary(self):
        """Get a sample vocabulary
        """
        return atapi.DisplayList(

            (("sample", _(u"Sample value 1"),),
            ("sample2", _(u"Sample value 2"),),))

atapi.registerType(Clinic, PROJECTNAME)

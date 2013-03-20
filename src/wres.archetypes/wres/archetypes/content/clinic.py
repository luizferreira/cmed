## coding=utf-8

"""Definition of the Clinic content type
"""

# from Products.DataGridField import DGFMessageFactory as _

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

    def fillClinicInformation(self, info):
        self.setName(info['clinic_name'])
        self.setStreet(info['clinic_street'])
        self.setNumber(info['clinic_number'])
        self.setComplemento(info['clinic_complemento'])
        self.setCity(info['clinic_city'])
        self.setState(info['clinic_state'].lower())
        # self.setPhone(info['clinic_phone'])
        # self.setEmail(info['E-mail'])

atapi.registerType(Clinic, PROJECTNAME)

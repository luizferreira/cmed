# coding=utf-8

"""Definition of the DocBoletim content type
"""

from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.Archetypes.public import DisplayList
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

from wres.archetypes.interfaces import IDocBoletim
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.medicaldocument import MedicalDocument
from wres.archetypes.content.schemas.docboletim import DocBoletimSchema

class DocBoletim(MedicalDocument):
    """A type of medical document"""
    implements(IDocBoletim)

    title = "Boletim Operatório"

    meta_type = "DocBoletim"
    schema = DocBoletimSchema
    
    security = ClassSecurityInfo()
    
    security.declarePublic('Title')
    def getTitle(self):
        """ """
        return 'Boletim Operatório'
    
    def at_post_create_script(self):
        self.title = self.getTitle()

    def getProtese(self):
            return DisplayList((
                        ('tipo', "TIPO",),
                        ('forma', "FORMA",),
                        ('perfil', "PERFIL",),
                        ('volume', "VOLUME",),
                   ))
            
    def getRegiaoLipoaspirada(self):
            return DisplayList((
                        ('abdome',"ABDOME"),
                        ('flancos', "FLANCOS"),
                        ('dorso', "DORSO"),
                        ('culotes', "CULOTES"),
                        ('face_int_coxa', "FACE INTERNA DA COXA"),
                        ('axilas', "AXILAS"),
                        ('cauda_mamaria', "CAUDA MAMARIA"),
                        ('joelhos', "JOELHOS"),
                        ('outros', "OUTROS"),
                        ('volume_total_aspirado', "VOLUME TOTAL ASPIRADO"),
                        ('volume_enxertado', "VOLUME ENXERTADO"),
                   ))
   

atapi.registerType(DocBoletim, PROJECTNAME)

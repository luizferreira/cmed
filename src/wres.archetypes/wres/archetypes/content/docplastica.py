# coding=utf-8

from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.Archetypes.public import DisplayList
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

from wres.archetypes.interfaces import IDocPlastica
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.medicaldocument import MedicalDocument
from wres.archetypes.content.schemas.docplastica import DocPlasticaSchema

class DocPlastica(MedicalDocument):
    """Documento médico reponsável pela Primeira Consulta Cirurgia Plástica"""
    implements(IDocPlastica)

    meta_type = "DocPlastica"
    schema = DocPlasticaSchema
    
    security = ClassSecurityInfo()

    security.declarePublic('Title')
    def getTitle(self):
        """ """
        return 'Cirurgia Plástica'
    
    def at_post_create_script(self):
        self.title = self.getTitle()

    security.declarePublic('getReactionValues')    
    def getReactionValues(self):
        return DisplayList(( 
                        ('Non Specified', 'Não especificada'),
                        ('Rash', 'Irritação'), ('collapse', 'Colapso'),
                        ('Unable to breath', 'Dificuldade em respirar'),
                        ))
   
    security.declarePublic('getAllergyValues')
    def getAllergyValues(self):
        return DisplayList((
                        ('Dipirona','Dipirona'),
                        ('Antibióticos','Antibióticos'),
                        ('Iodo','Iodo'),
                        ('Éter','Éter'),
                        ('Esparadrapo','Esparadrapo'),
                        ('Desconhece','Desconhece'),
                        ))

atapi.registerType(DocPlastica, PROJECTNAME)

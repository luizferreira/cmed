#coding=utf-8

"""Definition of the MedicalDocument content type
"""

from zope.interface import implements

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from archetypes.referencebrowserwidget import ReferenceBrowserWidget


from wres.archetypes.interfaces import IMedicalDocument
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.fields.defaultreferencefield import DefaultReferenceField
from wres.policy.utils.utils import getWresSite
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema

from zope.i18nmessageid import MessageFactory, Message
from DateTime import DateTime

_ = MessageFactory("cmfuemr")

MAIN = Schema((
    DateTimeField('date',
        default_method=DateTime,
        widget=CalendarWidget(
            label='Date',
            visible={'edit':'invisible'}
        ),
    ),

    # o DefaultReferenceField e' um ReferenceField com suporte a default_method
    DefaultReferenceField('doctor',
        required=1,
        relationship='doctor',
        allowed_types=('Doctor',),
        vocabulary_custom_label='b.Title',
        default_method = 'getDefaultDoctor',
        widget=ReferenceBrowserWidget(
            label=_('Provider'),
            startup_directory = 'Doctors',   
            restrict_browsing_to_startup_directory = True,         
        ),
    ),

    DateTimeField('dateOfVisit',
        default_method=DateTime,
        index="DateIndex:schema",
        widget=CalendarWidget(
            label=_('Date of Encounter'),
            show_hm=False,
            format='%d.%m.%Y',
        ),
    ),

    StringField('medicalNote',
        widget=TextAreaWidget(
            label='Nota',
            description='Coloque aqui comentários a respeito do documento.',
            visible={'view':'invisible', 'edit':'visible'},
        ),
    ),    
    
))

set_schemata_properties(MAIN, schemata='Principal')

baseSchema = finalizeSchema(folder.ATFolderSchema.copy())

MedicalDocumentSchema = baseSchema + MAIN

class MedicalDocument(folder.ATFolder):
    """Father of all CommuniMed medical documents"""
    implements(IMedicalDocument)

    meta_type = "MedicalDocument"
    schema = MedicalDocumentSchema

    def at_post_create_script(self):
        self.setTitle('Documento Médico')

    def getDefaultDoctor(self):
        portal = getWresSite()
        mt = getToolByName(portal, 'portal_membership')
        if mt.isAnonymousUser():
            return None
        else:
            member = mt.getAuthenticatedMember()
            roles = member.getRoles()
            if member.has_role('Doctor'):
                username = member.getUserName()
                pc = portal.portal_catalog
                brains = pc.search({'meta_type': 'Doctor', 'getId': username}) 
                doctor = brains[0].getObject()
                uid = doctor.UID()
                return uid
            else:
                return None

registerType(MedicalDocument, PROJECTNAME)

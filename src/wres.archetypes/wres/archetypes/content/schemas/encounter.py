# coding=utf-8

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.Archetypes.interfaces.vocabulary import IVocabulary
from Products.Archetypes.Registry import setSecurity

from wres.archetypes.config import PROJECTNAME
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema

from zope.i18nmessageid import MessageFactory, Message

_ = MessageFactory("cmfuemr")

MAIN = Schema((
    DateTimeField('date_of_visit',
        index="DateIndex:schema",
        required=1,
        widget=CalendarWidget(label="Date Of Visit",
                            label_msgid="cmfuemr_label_date_of_visit",
                            i18n_domain='cmfuemr',
                            visible={'view': 'invisible',
                                     'edit': 'visible',
                                     },
                            ),
    ),
    ReferenceField('visit',
        multiValued=1,
        relationship='encounter_visit',
#        vocabulary='patient_visits',
        ReferenceWidget=ReferenceWidget(label="Visit",
                                       label_msgid="cmfuemr_label_visit",
                                       i18n_domain='cmfuemr',
                                       visible={'view': 'visible',
                                                'edit': 'visible',
                                                },
                                       ),
    ),
    ReferenceField('related_documents',
        multiValued=1,
        relationship='encounter_document',
        widget=ReferenceWidget(label='Related Documents',
                              label_msgid="cmfuemr_label_related_documents",
                              i18n_domain='cmfuemr',
                              visible={'view': 'visible',
                                       'edit': 'visible',
                                       },),
    ),
    StringField('prescription',
        subfields=('medication',),
        widget=StringWidget(label='Prescription',
                          label_msgid='cmfuemr_label_precription',
                          i18n_domain='cmfuemr',
                          visible={'view': 'visible',
                                   'edit': 'visible',
                                   },
                          ),
    ),
))
        
baseSchema = finalizeSchema(folder.ATFolderSchema.copy())

EncounterSchema = baseSchema + MAIN

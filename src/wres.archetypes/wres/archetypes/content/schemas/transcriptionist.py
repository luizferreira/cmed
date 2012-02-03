# coding=utf-8

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import schemata


# -*- Message Factory Imported Here -*-

from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema

from wres.brfields.content.BrFieldsAndWidgets import CPFField, CPFWidget
from wres.brfields.validators import *


from zope.i18nmessageid import MessageFactory, Message

_ = MessageFactory("cmfuemr")

MAIN = Schema((
        StringField('firstName',
                    required=1,
                    widget=StringWidget(label=_('First Name'),
                    ),
        ),

        StringField('lastName',
                    required=1,
                    widget=StringWidget(label=_('Last Name'),
                    ),
        ),
        
        StringField('middleInitial',
                    widget=StringWidget(label=_('Middle Initial'),
                                        label_msgid='cmfuerm_label_middle_initial',
                                        i18n_domain='cmfuemr',
                                        visible={'edit': 'invisible', 'view': 'invisible',}
                    ),
        ),
            
        CPFField('ssn',
                required=0,
                searchable=1,
                widget=CPFWidget(label=_('SSN'),
                ),
        ),

        StringField('email',
                   required=1, 
                   #validators='isEmail',
                   widget=StringWidget(label=_('Email'),
                   ),
        ),
))

set_schemata_properties(MAIN, schemata='Principal')

baseSchema = finalizeSchema(wresuser.WRESUserSchema.copy())

TranscriptionistSchema = baseSchema + MAIN
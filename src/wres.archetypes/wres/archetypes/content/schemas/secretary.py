# coding=utf-8

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import schemata

from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema
from wres.policy.utils.permissions import EDIT_SECRETARY, VIEW_SECRETARY


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
            index="ZCTextIndex",
            widget=StringWidget(label=_('Last Name'),
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
            widget=StringWidget(label=_('Email'),
            ),
        ),                                                                        
                                                                        
))
set_schemata_properties(MAIN, schemata='Principal')
        
baseSchema = finalizeSchema(wresuser.WRESUserSchema.copy())

SecretarySchema = baseSchema + MAIN

set_schemata_properties(SecretarySchema, read_permission=VIEW_SECRETARY, write_permission=EDIT_SECRETARY) 

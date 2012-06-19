# coding=utf-8

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import schemata

from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema
from wres.policy.utils.permissions import EDIT_SECRETARY, VIEW_SECRETARY, SET_CHART_ACCESS


from wres.brfields.content.BrFieldsAndWidgets import*
from wres.brfields.validators import *

from zope.i18nmessageid import MessageFactory, Message

_ = MessageFactory("cmfuemr")

MAIN = Schema((

        BooleanField('isTranscriptionist', 
            read_permission=SET_CHART_ACCESS,
            write_permission=SET_CHART_ACCESS,
            widget = BooleanWidget(label=_(u'Transcritora?'),
                                   description=_('Check if secretary will be able to transcript documents.'),
            ),
        ),
                                                                        
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

        StringField('address1',
            widget=StringWidget(
                label=_('Address 1'),
            ),
        ),

        StringField('city',
            widget=StringWidget(
                label=_('City'),
            ),
        ),

        StringField('state',
            widget=StringWidget(
                label=_('State'),
            ),
        ),   

        BrPhoneField('phone',
            widget=BrPhoneWidget(label=_('Phone'),
                                 description='You must enter only numbers',
                                 description_msgid='cmfuemr_help_you_must_enter_only_numbers',
                                 i18n_domain='cmfuemr',
                             ),
            searchable=1,
            ),      

        BrPhoneField('cel',
            widget=BrPhoneWidget(label=_('Cel'),
                                     description='You must enter only numbers',
                                     description_msgid='cmfuemr_help_you_must_enter_only_numbers',
                                     i18n_domain='cmfuemr',
            ),
        ),                                                     
                                                                        
))
set_schemata_properties(MAIN, schemata='Principal')
        
baseSchema = finalizeSchema(wresuser.WRESUserSchema.copy())

SecretarySchema = baseSchema + MAIN

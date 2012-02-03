# coding=utf-8

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import schemata

from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema
from wres.brfields.content.BrFieldsAndWidgets import *

from zope.i18nmessageid import MessageFactory, Message

_ = MessageFactory("cmfuemr")

#===============================================================================
# Definição dos schemas do tipo Admin
#===============================================================================

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
                                                visible={'edit': 'invisible', 'view': 'invisible',},
            ),      
        ),
        

        CPFField('ssn',
            index="FieldIndex:schema",
            searchable=1,
            widget=CPFWidget(
                label=_('SSN'),
            ),
         ),

        StringField('email',
           required=1, 
           validators='isEmail',
           widget=StringWidget(label=_('Email'),
           ),
        ),
))

set_schemata_properties(MAIN, schemata='Principal')

baseSchema = finalizeSchema(wresuser.WRESUserSchema.copy())

AdminSchema = baseSchema + MAIN
 

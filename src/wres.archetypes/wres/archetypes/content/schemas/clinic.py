# coding=utf-8

# Zope imports

# Plone imports
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import schemata

# Other products imports
from wres.brfields.content.BrFieldsAndWidgets import *
from wres.brfields.validators import *

# Local imports
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema

INFO = Schema((

    StringField('name',
        widget=StringWidget(
            label='Nome',
        ),
    ),                  

    StringField('endereco',
        widget=StringWidget(
            label='Endereço',
        ),
    ),
    
    BrPhoneField('phone',
#       required=1,   bax migrando
#       validators='isBrTelefone',
        widget=BrPhoneWidget(
            label='Telefone',
            description='You must enter only numbers',
            description_msgid='cmfuemr_help_home_phone',
            i18n_domain='cmfuemr'
        ),
    ),  
    
    BrPhoneField('fax',
#       required=1,   bax migrando
#       validators='isBrTelefone',
        widget=BrPhoneWidget(
            label='Fax',
            description='You must enter only numbers',
            description_msgid='cmfuemr_help_home_phone',
            i18n_domain='cmfuemr'
        ),
    ),         
    
    StringField('email',
#      validators='isEmail',
       widget=StringWidget(
           label='Email',
       ),
    ),    

))

set_schemata_properties(INFO, schemata='Informacoes da Clinica')

baseSchema = finalizeSchema(schemata.ATContentTypeSchema.copy())

ClinicSchema =  baseSchema + INFO

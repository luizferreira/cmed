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
from wres.policy.utils.permissions import VIEW_DOCTOR

STATES = DisplayList((
    ('ac', 'Acre'),
    ('al', 'Alagoas'),
    ('ap', 'Amapá'),
    ('am', 'Amazonas'),
    ('ba', 'Bahia'),
    ('ce', 'Ceará'),
    ('df', 'Distrito Federal'),
    ('es', 'Espírito Santo'),
    ('go', 'Goiás'),
    ('ma', 'Maranhão'),
    ('mt', 'Mato Grosso'),
    ('ms', 'Mato Grosso do Sul'),
    ('mg', 'Minas Gerais'),
    ('pa', 'Pará'),
    ('pb', 'Paraíba'),
    ('pb', 'Paraná'),
    ('pe', 'Pernambuco'),
    ('pi', 'Piauí'),
    ('rj', 'Rio de Janeiro'),
    ('rn', 'Rio Grande do Norte'),
    ('rs', 'Rio Grande do Sul'),
    ('ro', 'Rondônia'),
    ('rr', 'Roraima'),
    ('sc', 'Santa Catarina'),
    ('sp', 'São Paulo'),
    ('se', 'Sergipe'),
    ('to', 'Tocantins'),
    ))

INFO = Schema((

    StringField('name',
        widget=StringWidget(
            label='Nome',
        ),
    ),

    StringField('street',
        widget=StringWidget(
            label='Rua/Avenida',
        ),
    ),

    IntegerField('number',
        validators = ('isInt',),
        widget=IntegerWidget(
            label='Número',
        ),
    ),

    StringField('complemento',
        widget=StringWidget(
            label='Complemento',
        ),
    ),

    StringField('bairro',
        widget=StringWidget(
            label='Bairro',
        ),
    ),

    StringField('city',
        widget=StringWidget(
            label='Cidade',
        ),
    ),

    StringField('state',
        vocabulary=STATES,
        widget=SelectionWidget(
            label='Estado',
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
       validators='isEmail',
       widget=StringWidget(
           label='Email',
       ),
    ),

   ImageField('logo',
       max_size=(160,160),
       widget=ImageWidget(
           label='Logo da Clínica',
           description='Imagem usada em documentos impressos.'
        ),
   ),

))

set_schemata_properties(INFO, schemata='Informacoes da Clinica')

baseSchema = finalizeSchema(schemata.ATContentTypeSchema.copy())

ClinicSchema =  baseSchema + INFO

set_schemata_properties(ClinicSchema, read_permission=VIEW_DOCTOR)
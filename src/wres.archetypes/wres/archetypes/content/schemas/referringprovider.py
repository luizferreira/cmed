# coding=utf-8

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import schemata

from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema

from zope.i18nmessageid import MessageFactory, Message

_ = MessageFactory("cmfuemr")

MEDICAL_SPECIALTIES = DisplayList((
    ('allergy', _('Allergy & Immunology')), # Alergia e Imunologia
    ('anesthesiology', _('Anesthesiology')), # Anestesiologia
    ('emergency', _('Emergency Medicine')), # Atendimento de emergência
    ('cardiology', _('Cardiology')), # Cardiologia
    ('surgery', _('Surgery')), # Cirurgia
    ('neurological', _('Neurological Surgery')), # Cirurgia Neurológica
    ('plastic', _('Plastic Surgery')), # Cirurgia Plástica
    ('general', _('General Practice')), # Clínica geral
    ('dermatology', _('Dermatology')), # Dermatologia
    ('infectious', _('Infectious Disease')), # Doença infecciosa
    ('endocrinology', _('Endocrinology, Diabetes & Metabolism')), # Endocrinologia, Diabetes e Metabolismo
    ('gastroenterology', _('Gastroenterology')), # Gastroenterologia
    ('geriatrics', _('Geriatrics')), # Geriatria
    ('family', _('Family Medicine')), # Medicina familiar
    ('physical', _('Physical Medicine & Rehabilitation')), # Medicina Física e Reabilitação    
    ('medical', _('Medical Genetics')), # Medicina Genética
    ('internal', _('Internal Medicine')), # Medicina Interna
    ('preventive', _('Preventive Medicine')), # Medicina Preventiva
    ('nephrology', _('Nephrology')), # Nefrologia
    ('neurology', _('Neurology')), # Neurologia
    ('obstetrics', _('Obstetrics & Gynecology')), # Obstetrícia e Ginecologia
    ('ophthalmology', _('Ophthalmology')), # OftalmologiaOftalmologia
    ('oncology', _('Oncology (Cancer)')), # Oncologia (Câncer)
    ('orthopedics', _('Orthopedics')), #Ortopedia
    ('otolaryngology', _('Otolaryngology')), # Otorrinolaringologia
    ('other', _('Other')), # Outro
    ('pathology', _('Pathology')), # Patologia
    ('pediatrics', _('Pediatrics')), # Pediatria
    ('psychiatry', _('Psychiatry')), # Psiquiatria
    ('radiology', _('Radiology')), # Radiologia
    ('urology', _('Urology')), # Urologia
))

SSN_FEDTAXID = DisplayList((
    ('federalTax', _('Federal Tax ID Indicator')),
    ('SSN', _('SSN')),
))


MAIN = Schema((
        StringField('firstName',
            required=1,
            widget=StringWidget(label=_('First Name'),
            ),
        ),

#        StringField('middleInitial',
#            widget=StringWidget(label='Middle Initial',
#                                label_msgid='cmfuemr_label_middle_initial',
#                                i18n_domain='cmfuemr',
#            ),
#        ),

        StringField('lastName',
            index='ZCTextIndex',
            required=1,
            widget=StringWidget(label=_('Last Name'),
            ),
        ),
        StringField('credentials',
            widget=StringWidget(label=_('Credentials'),
            ),
        ),

#        StringField('medicareParticipating',
#            widget=BooleanWidget(label='Medicare Participating',
#                                 label_msgid='cmfuemr_label_medicare_participating',
#                                 i18n_domain='cmfuemr',
#            ),
#        ),

        StringField('licenseNumber',
            widget=StringWidget(label=_('License Number'),
            ),
        ),

        StringField('specialty',
            vocabulary=MEDICAL_SPECIALTIES,
            widget=StringWidget(label=_('Specialty'),
            ),
        ),
        StringField('professional',
            default='Provider',
            index="FieldIndex",
            widget=StringWidget(visible={'edit': 'invisible',
                                         'view': 'invisible'},
                                label=_('professional'),
            ),
        ),
        StringField('email',
           required=1, 
           validators='isEmail',
           widget=StringWidget(label='Email',
            ),
        ),
))
set_schemata_properties(MAIN, schemata='Principal')

ADDRESS = Schema((
        StringField('street',
            widget=StringWidget(label=_('Street'),
            ),
        ),

        StringField('city',
            widget=StringWidget(label=_('City'),
            ),
        ),

        StringField('state',
            widget=StringWidget(label=_('State'),
            ),
        ),

        StringField('zipCode',
            widget=StringWidget(label=_('ZipCode'),
            ),
        ),

        StringField('phone',
            widget=StringWidget(label=_('Phone'),
            ),
        ),

        StringField('fax',
            widget=StringWidget(label=_('Fax'),
            ),
        ),
))
set_schemata_properties(ADDRESS, schemata='Endereco')

PINS = Schema((
        StringField('SSN_FedTaxID',
            widget=StringWidget(label='SSN/Federal Tax ID',
#                                label_msgid='cmfuerm_label_ssn_federal_tax_id',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('SSN_FedTaxID_Option',
            vocabulary=SSN_FEDTAXID,
            widget=SelectionWidget(label='',
#                                   label_msgid='cmfuerm_label_''',
#                                   i18n_domain='cmfuemr',
            ),
        ),
        StringField('medicare',
            widget=StringWidget(label='Medicare',
#                                label_msgid='cmfuerm_label_medicare',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('medicaid',
            widget=StringWidget(label='Medicaid',
#                                label_msgid='cmfuerm_label_medicaid',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('tricare',
            widget=StringWidget(label='Tricare',
#                                label_msgid='cmfuerm_label_tricare',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('blueCross_shield',
            widget=StringWidget(label='Blue Cross/Shield',
#                                label_msgid='cmfuerm_label_blue_cross_shield',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('commercial',
            widget=StringWidget(label='Commercial',
#                                label_msgid='cmfuerm_label_commercial',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('ppo',
            widget=StringWidget(label='PPO',
#                                label_msgid='cmfuerm_label_ppo',
#                                i18n_domain='comfuemr',
            ),
        ),
        StringField('hmo',
            widget=StringWidget(label='HMO',
#                                label_msgid='cmfuerm_label_hmo',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('upin',
            widget=StringWidget(label='UPIN',
#                                label_msgid='cmfuerm_label_upin',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('extra1',
            widget=StringWidget(label='Extra 1',
#                                label_msgid='cmfuerm_label_extra_1',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('extra2',
            widget=StringWidget(label='Extra 2',
#                                label_msgid='cmfuerm_label_extra_2',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('emcId',
            widget=StringWidget(label='EMC ID',
#                                label_msgid='cmfuerm_label_emc_id',
#                                i18n_domain='cmfuemr',
            ),
        ),
        StringField('nationalIdentifier',
            widget=StringWidget(label='National Identifier',
#                                label_msgid='cmfuerm_label_national_identifier',
#                                i18n_domain='cmfuemr',
            ),
        ),
))
set_schemata_properties(PINS, schemata='Default PINs')
        
baseSchema = finalizeSchema(wresuser.WRESUserSchema.copy())

ReferringProviderSchema = baseSchema + MAIN + ADDRESS #+ PINS Campos na usados no Brasil
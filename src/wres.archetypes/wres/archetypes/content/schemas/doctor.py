# coding=utf-8

from Products.Archetypes.atapi import *

# datagrid field
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.DataGridField import FixedRow

from wres.archetypes.content import wresuser
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema
from wres.policy.utils.permissions import EDIT_DOCTOR, VIEW_DOCTOR

from wres.brfields.content.BrFieldsAndWidgets import *
from wres.brfields.validators import *

from zope.i18nmessageid import MessageFactory

_ = MessageFactory("cmfuemr")

#===============================================================================
# DisplayList de Especialidades
#===============================================================================
MEDICAL_SPECIALTIES = DisplayList((
    ('', _('Not selected')), # Nao selecionado
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
    ('neurosurgery', _('Neurosurgery')), # Neurocirurgia
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

#===============================================================================
# Schema de campos do tipo Doctor
#===============================================================================
MAIN = Schema((
        
       ImageField('photo',
           max_size=(150,150),
           widget=ImageWidget(
               label='Foto',
            ),
       ),

        StringField('professional',
            vocabulary=[_('Provider'), _('Technician'), _('Nurse')],
            default='Provider',
            index="FieldIndex",
            widget=SelectionWidget(label=_('Type of Professional'),
            ),
        ),    
        StringField('ssn',
            index="FieldIndex",
            # validators = ('isDecimal',),
            widget=StringWidget(label=_('CRM'),
            # helper_js=('doctorcrm.js',),
            ),
        ),
        StringField('firstName',
            required=1,
            widget=StringWidget(
                label=_('First Name'),
            ),
        ),
        StringField('lastName',
            required=1,
            index="ZCTextIndex",
            widget=StringWidget(
                label=_('Last Name'),
            ),
        ),
            
        #CPFField('ssn',
            #widget=CPFWidget(label=_('SSN'),
                             #),
            #searchable=1,
            #),
                    
        StringField('street1',
            widget=StringWidget(label=_('Address 1'),
            ),
        ),

        StringField('street2',
            widget=StringWidget(label=_('Address 2'),
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
            
        CEPField('zipcode',
            widget=CEPWidget(label=_('ZipCode'),
                             ),
            searchable=1,
            ),
        
         StringField('website',
            validator='isURL',
            widget=StringWidget(label=_('Website'),
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
        BrPhoneField('fax',
            widget=BrPhoneWidget(label=_('Fax'),
                                     description='You must enter only numbers',
                                     description_msgid='cmfuemr_help_you_must_enter_only_numbers',
                                     i18n_domain='cmfuemr',
            ),
        ),
        StringField('email',
            required=1,    
            validators = ('isEmail',),
            widget=StringWidget(
                label=_('Email'),
                description='Eventualmente poderemos entrar em contato através dele.'
            ),
        ),      

        StringField('specialty1',
            required=True,
            vocabulary=MEDICAL_SPECIALTIES,
            widget=SelectionWidget(label='Especialidade 1',
            ),
        ),       

        StringField('specialty2',
            vocabulary=MEDICAL_SPECIALTIES,
            widget=SelectionWidget(
                label='Especialidade 2',
                description="Deixe 'Não selecionado', caso não queira destacar outra especialidade.",
            ),
        ),        

        DataGridField('curriculum',
            description='Estas informações serão apresentadas em seu cartão de visita virtual.',
            columns=('tipo', 'course', 'inst'),
            allow_empty_rows = False,
            allow_oddeven=True,
            allow_reorder = False,
            fixed_rows = [
                FixedRow(keyColumn="course", initialData = { "tipo" : "", "course" : "Medicina", "inst" : "" }),
            ],                
            widget=DataGridWidget(
                label='Curriculum',
                columns={
                    'tipo' : SelectColumn('Tipo', vocabulary='getCourseTypes'),
                    'course' : Column('Área'),
                    'inst' : Column('Instituição'),
                },
            ),
        ),

))
set_schemata_properties(MAIN, schemata='Principal')

OTHER = Schema((   
         StringField('initial',
            widget=StringWidget(label=_('Initial'),
            ),
        ),
        StringField('signature',
            index=':schema',
            widget=StringWidget(label=_('Signature'),
                                description='Enter with the doctor signature label.',
                                description_msgid='cmfuemr_help_signature',
                                i18n_domain='cmfuemr',
            ),
        ),
        # StringField('dea',
        #             widget=StringWidget(label=_('DEA #'),
        #             ),
        # ),
        # TODO: retirar (May2012)
        StringField('credentials',
            widget=StringWidget(label=_('Credentials'),
            ),
        ),
                                                             
))
set_schemata_properties(OTHER, schemata='Outro')

SIGN_PASSWORD = Schema((
    StringField('signPassword',
        encryption='SSHA',
        widget=PasswordWidget(label=_('Sign Password'),
                                    visible={'edit': 'invisible',
                                             'view': 'invisible',
                                             }
                                    ),
        ),
))
set_schemata_properties(SIGN_PASSWORD, schemata='Assinatura Eletronica')
        
baseSchema = finalizeSchema(wresuser.WRESUserSchema.copy())

DoctorSchema = baseSchema + MAIN + OTHER + SIGN_PASSWORD

set_schemata_properties(DoctorSchema, read_permission=VIEW_DOCTOR, write_permission=EDIT_DOCTOR) 

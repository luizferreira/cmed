#coding=utf-8

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import schemata
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema

from wres.brfields.content.BrFieldsAndWidgets import *
from wres.brfields.validators import *

from zope.i18nmessageid import MessageFactory, Message

import datetime
now = datetime.datetime.now()

_ = MessageFactory("cmfuemr")

#===============================================================================
# Definição de algumas display lists utilizadas no schema
#===============================================================================

SEX = DisplayList((
    ('Male', _('Male')),
    ('Female', _('Female')),
    ))
    
ORGAOEMISSOR = DisplayList((
    ('', ''),
    ('ssp', 'Secretaria de Segurança Pública'),
    ('aeronautica', 'Ministério da Aeronáutica'),
    ('exercito', 'Ministério do Exército'),
    ('marinha', 'Ministério da Marinha'),
    ('pf', 'Polícia Federal'),
    ('classista', 'Carteira de Identidade Classista'),
    ('admin', 'Conselho Regional de Administração'),
    ('sociais', 'Conselho Regional de Assistentes Sociais'),
    ('biblio', 'Conselho Regional de Biblioteconomia'),
    ('cont', 'Conselho Regional de Contabilidade'),
    ('corretores', 'Conselho Regional de Corretores de Imóveis'),
    ('enfermagem', 'Conselho Regional de Enfermagem'),
    ('engenharia', 'Conselho Regional de Engenharia'),
    ('estatatistica', 'Conselho Regional de Estatística'),
    ('farm', 'Conselho Regional de Farmácia;'),
    ('fisio', 'Conselho Regional de Fisioterapia'),
    ('med', 'Conselho Regional de Medicina'),
    ('medvet', 'Conselho Regional de Medicina Veterinária'),
    ('odont', 'Conselho Regional de Odontologia'),
    ('ralacoes', 'Conselho Regional de Relações Públicas'),
    ('psico', 'Conselho Regional de Psicologia'),
    ('quim', 'Conselho Regional de Química'),
    ('comerciais', 'Conselho Representantes Comerciais'),
    ('advogados', 'Ordem dos Advogados do Brasil'),
    ('musicos', 'Ordem dos Músicos do Brasil'),
    ))
RACE = DisplayList((
    ('', ''),
    ('branca', 'Branca'),
    ('preta', 'Preta'),
    ('amarela', 'Amarela'),
    ('parda', 'Parda'),
    ('indigena', 'Indigena'),
    ))
MARITAL_STATUS = DisplayList((
    ('', ''),
    ('single', _('Single')),
    ('married', _('Married')),
    ('divorced', _('Divorced')),
    ('widowed', _('Widowed')),
    ))
EDUCATION_COMPLETED = DisplayList((
    ('', ''),
    ('analfabeto', 'Analfabeto'),
    ('alfabetizado', 'Alfabetizado'),
    ('fundamental_i', 'Nível Fundamental Incompleto'),
    ('fundamental_c', 'Nível Fundamental Completo'),
    ('medio_i', 'Nível Médio Incompleto'),
    ('medio_c', 'Nível Médio Completo'),
    ('sup_i', 'Nível Superior Incompleto'),
    ('sup_c', 'Nível Superior Completo'),
    ('mestrado', 'Mestrado'),
    ('doutorado', 'Doutorado'),
    ))
STATUS = DisplayList((
    ('', ''),
    ('notemployed', _('Not employed')),
    ('fulltime', _('Full time')),
    ('parttime', _('Part time')),
    ('parttimestudent', _('Part Time Student')),
    ('fulltimestudent', _('Full Time Student')),
    ('retired', _('Retired')),
    ('unknown', _('Unknown')),
    ))
PATIENT_TYPE = DisplayList((
    ('estabilished', _('Established')),
    ('new', _('New'))
    ))

#===============================================================================
# Definição dos schemas de do tipo Patient
#===============================================================================

MAIN = Schema((

    StringField('type_of_patient',
        required=0,
        vocabulary=PATIENT_TYPE,
        default='new',
        widget=SelectionWidget(
	        label=_('Type of patient'),
        ),
    ),

    StringField('firstName',
        required=1,
#       validators='isName',
        widget=StringWidget(
	        label=_('First Name'),
        ),
    ),

    StringField('lastName',
        required=1,
#       validators='isName',
        index="ZCTextIndex",
        widget=StringWidget(
	        label=_('Last Name'),
        ),
    ),
    
    # conforme decidido, a data de nascimento deixa de ser obrigaoria
	DateTimeField('birthDate',
		widget=CalendarWidget(
	       label=_('Birth Date'),
           format='%d/%m/%Y',
           starting_year=1901,
           future_years=0,
           show_hm=0,
       )
   ),    
    
    StringField('email',
#      validators='isEmail',
       widget=StringWidget(
	       label=_('Email'),
       ),
    ),    

#        StringField('socialSecurity',#O Nome não foi mudado para não dar conflitos em search, mas creio que isso deve ser resolvido rapidamente
##            validators=('isCPF',),#Validadores são definidos  em Products.CMFUEMR.validators
#            index="FieldIndex:schema",
#            widget=StringWidget(label='Social Security',#Não foi alterado o nome porque a internacionalização ja resolve o problema
#                             label_msgid='cmfuemr_label_social_security',
#                             i18n_domain='cmfuemr',),
#        ),

    BrPhoneField('homePhone',
#       required=1,   bax migrando
#       validators='isBrTelefone',
        widget=BrPhoneWidget(
            label=_('Home Phone'),
            description='You must enter only numbers',
            description_msgid='cmfuemr_help_home_phone',
            i18n_domain='cmfuemr'
        ),
    ),

    BrPhoneField('mobile',
#      validators='isBrTelefone',
       widget=BrPhoneWidget(
           label=_('Mobile'),
           description='You must enter only numbers',
           description_msgid='cmfuemr_help_mobile',
           i18n_domain='cmfuemr',
       ),
    ),
    
    BrPhoneField('contactPhone',
#       validators='isBrTelefone',
        required=1, 
        index=':schema',
        widget=BrPhoneWidget(
            label=_('Contact Phone'),
            description='Telefone pelo qual o paciente prefere ser contactado',
#            description_msgid='cmfuemr_help_contact_phone',
            i18n_domain='cmfuemr',
            macro_edit='patient_cphone_edit_macro',
            helper_js=('patient_cphone_edit.js', ),
#           helper_js=PhoneNumberWidget._properties['helper_js'] \
#           + ('uemr_widgets/js/contactphone_patient.js',),
        ),
    ),
    
    CPFField('socialSecurity',
        index="FieldIndex:schema",
        searchable=1,
        widget=CPFWidget(
	        label=_('SSN'),
        ),
     ),
    
    StringField('identidade',
        widget=StringWidget(
	        label='Identidade',
        ),
    ),
    
    StringField('orgaoEmissor',
        vocabulary=ORGAOEMISSOR,
        widget=SelectionWidget(
	        label='Órgão Emissor',
        ),
    ),


#===============================================================================
# Luiz
# Falta migrar o campo birthDate - Update: foi colocado um birthdate temporário, 
# precisa ser melhorado posteriormente. 
#===============================================================================

#        DateTimeField('birthDate',
#            index="DateIndex",
#            with_time=0, # set to False if you want date only objects
#            with_date=1, # set to False if you want time only objects            
#            widget=DateTimeWidget(label='Birth Date',
#                                   label_msgid='cmfuemr_label_birth_date',
#                                   i18n_domain='cmfuemr',),
#        ),
    

    StringField('sex',
        vocabulary=SEX,
        widget=SelectionWidget(
	        label=_('Sex'),
        ),
    ),

#===============================================================================
# Falta migrar os dois campos a seguir: primaryDoctor e referredBy
#===============================================================================

#        ExtendedReferenceField('primaryDoctor',
#            required=1,
#            relationship='primaryDoctor',
#            allowed_types=('Doctor',),
#            filter_indexes={'getProfessional': 'Provider'},
#            vocabulary_custom_label="'%s' % b.Title",
#            widget=ReferenceWidget(label='Primary Provider at our Office',
#                                   label_msgid='cmfuemr_label_primary_provider_at_our_office',
#                                   i18n_domain='cmfuemr',),
#        ),

#        ExtendedReferenceField('referredBy',
#            relationship='referredBy',
#            filter_indexes={'getProfessional': 'Provider'},
#            allowed_types=('ReferringProvider', 'Doctor'),
#            widget=BuildingBlocksWidget(label='Referred By',
#                                        label_msgid='cmfuemr_label_referred_by',
#                                        description=""" """,
#                                        description_msgid='cmfuemr_help_referred_by',
#                                        i18n_domain='cmfuemr',
#                                        blocks=({'id': 'popup_search',
#                                                 'value': 'Search',
#                                                 'filter_indexes': {'getProfessional': 'Provider'}},
#                                                {'id': 'popup_quick_register',
#                                                 'value': 'Register',
#                                                 'location': '/referringprovider_folder'
#                                                 },),),
#        ),
    
#===============================================================================
# Falta migrar o campo seguinte: insurance
#===============================================================================

    StringField('address1',
        widget=StringWidget(
	        label=_('Address 1'),
        ),
    ),

    StringField('address2',
        widget=StringWidget(
	        label=_('Address 2'),
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
    
    CEPField('zipcode',
        searchable=1,
        widget=CEPWidget(
            label=_('ZipCode'),
        ),
    ),

#    IntegerField('ext',
#        widget=IntegerWidget(
#           label=_('Ext.'),
#        ),
#    ),

    
    IntegerField('chart',
        default=0,
        index="FieldIndex:schema",
        widget=IntegerWidget(
            label=_('Chart Number'),                                
		    description='Must contain only numbers',
		    description_msgid='cmfuemr_help_chart_number',
		    i18n_domain='cmfuemr'
        ),
    ),

    BooleanField('confirmedChartNumber',
        default=False,
        widget=BooleanWidget(
	        label=_('Chart Number Confirmed'),
        ),
    ),    

))
set_schemata_properties(MAIN, schemata='Principal')

COMPLEMENTAR = Schema((

    StringField('pis_pasep',
        widget = StringWidget(
	        label='PIS/PASEP',
        ),
    ),

    StringField('CTPS',
        widget = StringWidget(
	        label='Carteira de Trabalho e Previdência Social',
        ),
    ),

    StringField('tituloEleitor',
        widget = StringWidget(
	        label='Título de eleitor',
        ),
    ),
))
set_schemata_properties(COMPLEMENTAR, schemata='Complementar')

GUARANTOR = Schema((
    BooleanField('isGuarantor',
         index='FieldIndex',
         default=1,
         widget=BooleanWidget(
	        label=_('Guarantor'),
            description='Check the box if the\
            patient is a guarantor',
            description_msgid='cmfuemr_help_guarantor',
            i18n_domain='cmfuemr',
         ),
    ),

    StringField('guarantor_name',
        widget = StringWidget(
	        label=_('Name'),
        ),
    ),

    StringField('guarantor_relationship',
        widget = StringWidget(
	        label=_('Relationship'),
        ),
    ),
                
   StringField('guarantor_identidade',
        widget=StringWidget(
	        label='Identidade',
        ),
    ),
    
    StringField('guarantor_orgaoEmissor',
        vocabulary=ORGAOEMISSOR,
        widget=SelectionWidget(
	        label='Orgão Emissor',
        ),
    ),
    
#===============================================================================
# O campo guarantor_contact_phone precisa de validador         
#===============================================================================
    
   StringField('guarantor_contact_phone',
#      validators='isBrTelefone',
       widget=StringWidget(
	       label=_('Contact Phone'),
           description='You must enter only numbers',
           description_msgid='cmfuemr_help_contact_phone',
           i18n_domain='cmfuemr',
       ),
   ),

    StringField('guarantor_extension',
        widget=StringWidget(
            label=_('Extension'),
        ),
    ),

    StringField('guarantor_address1',
        widget=StringWidget(
	        label='Endereço',
        ),
    ),

    StringField('guarantor_address2',
        widget=StringWidget(
	        label='Bairro',
        ),
    ),

    StringField('guarantor_city',
        widget=StringWidget(
	        label=_('City'),
        ),
    ),

    StringField('guarantor_state',
        widget=StringWidget(
	        label=_('State'),
        ),
    ),
    
#===============================================================================
# O campo guarantor_zipcode precisa de validador        
#===============================================================================
    
    StringField('guarantor_zipcode',
#       validators='isCEP',
        widget=StringWidget(
	        label=_('ZipCode'),
        ),
    ),
))
set_schemata_properties(GUARANTOR, schemata='Titular')

CONVENIOS = Schema((

	ReferenceField('insurance',
		relationship='insurance_patient',
		allowed_types=('Insurance',),			
		widget=ReferenceBrowserWidget(
			label='Plano de Saúde',
			description='Selecione a operadora do plano de saúde',
			startup_directory = 'Insurances',                                   
			label_msgid='cmfuemr_label_insurance',
			i18n_domain='cmfuemr'
		)
	),
	
	StringField('tipo',
		schemata='main',
		widget=StringWidget(label=_('Tipo'),
		)
	),	

    StringField('convenio',
        widget = StringWidget(
	        label='Convênio',
        ),
    ),
    #TODO - Retirar este campo
    #StringField('plano',
        #widget = StringWidget(
	        #label='Plano',
        #),
    #),

    StringField('matricula',
        widget = StringWidget(
	        label='Matrícula',
        ),
    ),
    
	DateTimeField('dataDeValidade',
		widget=CalendarWidget(
	       label=_('Data de Validade do Plano'),
           format='%d/%m/%Y',
           future_years=30,
           starting_year=now.year,
           show_hm=0,
       )
    #StringField('dataDeValidade',
        #widget = StringWidget(
	        #label='Data de validade',
        #),
    ),
                
    StringField('titular',
        widget = StringWidget(
	        label='Titular',
        ),
    ),
    
    StringField('cartaoNacionalDeSaude',
        widget=StringWidget(
	        label='Cartão Nacional de Saúde',
        ),
    ),    
    
))
set_schemata_properties(CONVENIOS, schemata='Planos de Saude')

DEMOGRAPHIC = Schema((

    StringField('nomeDoPai',
        widget=StringWidget(
	        label='Nome do Pai',
        ),
    ),
    
    StringField('nomeDaMae',
        widget=StringWidget(
	        label='Nome da Mãe',
        ),
    ),
    
    StringField('nacionalidade',
        widget=StringWidget(
	        label='Nacionalidade',
        ),
    ),    

    StringField('race',
        vocabulary=RACE,
        widget=SelectionWidget(
	        label=_('Race'),
        ),
    ),

    StringField('maritalStatus',
        vocabulary=MARITAL_STATUS,
        widget=SelectionWidget(
	        label='Estado Civil',
        ),
    ),

    StringField('educationCompleted',
        vocabulary=EDUCATION_COMPLETED,
        widget=SelectionWidget(
	        label=_('Education Completed'),
        ),
    ),
    
   ImageField('photo',
       max_size=(150,150),
       widget=ImageWidget(
	       label='Foto',
        ),
   ),
))
set_schemata_properties(DEMOGRAPHIC, schemata='Demografico')

EMPLOYMENT = Schema((
   StringField('employerName',
#      validators='isName',
       widget=StringWidget(
	       label=_('Employer Name'),
       ),
   ),

   StringField('industry',
       widget=StringWidget(
	       label=_('Industry'),
       ),
   ),

   StringField('occupationTitle',
       widget=StringWidget(
	       label=_('Occupation Title'),
       ),
   ),

   StringField('status',
       vocabulary=STATUS,
       widget=SelectionWidget(
	       label=_('Occupational Status'),
       ),
   ),

#===============================================================================
# O campo workPhone precisa de validador
#===============================================================================

   StringField('workPhone',
#      validators='isBrTelefone',
       widget=StringWidget(
	       label=_('Work Phone'),
           description='You must enter only numbers',
           description_msgid='cmfuemr_help_work_phone',
           i18n_domain='cmfuemr',
       ),
   ),

   StringField('extension',
       widget=StringWidget(
	       label=_('Extension'),
       ),
   ),

#===============================================================================
# O campo fax precisa de validador
#===============================================================================

   StringField('fax',
#      validators='isBrTelefone',
       widget=StringWidget(
	       label=_('Fax'),
           description='You must enter only numbers',
           description_msgid='cmfuemr_help_fax',
           i18n_domain='cmfuemr',
       ),
   ),

   DateTimeField('retirementdate',
       widget=CalendarWidget(
	       label=_('Retirement Date'),
           format='%d/%m/%Y',
           show_hm = False,
           visible={'edit':'visible'}
       ),
   ),
))

#===============================================================================
# Diminuindo o número de schematas
#===============================================================================
#set_schemata_properties(EMPLOYMENT, schemata='Employment Information')
set_schemata_properties(EMPLOYMENT, schemata='Complementar')

EMERGENCY = Schema((
    StringField('emergency_contact_name',
        widget = StringWidget(
	        label=_('Name'),
        ),
     ),

    StringField('emergency_relationship',
        widget = StringWidget(
	        label=_('Relationship'),
        ),
     ),
                
#===============================================================================
# Os campos emergency_work_phone, emergency_home_phone e emergency_other_phone
# precisam de validadores                
#===============================================================================
                
   StringField('emergency_work_phone',
#      validators='isBrTelefone',
       widget=StringWidget(
	       label=_('Work Phone'),
	       description='You must enter only numbers',
	       description_msgid='cmfuemr_help_work_phone',
	       i18n_domain='cmfuemr',
       ),
   ),

   StringField('emergency_home_phone',
#      validators='isBrTelefone',
       widget=StringWidget(
	       label=_('Home Phone'),
           description='You must enter only numbers',
           description_msgid='cmfuemr_help_home_phone',
           i18n_domain='cmfuemr',
       ),
   ),

   StringField('emergency_other_phone',
#      validators='isBrTelefone',
       widget=StringWidget(
	       label=_('Other Phone'),
           description='pager, cellular, etc. if applicable',
           description_msgid='cmfuemr_help_other_phone',
           i18n_domain='cmfuemr',
       ),
   ),

    StringField('emergency_address1',
        widget=StringWidget(
	        label='Endereço',
        ),
    ),

    StringField('emergency_address2',
        widget=StringWidget(
	        label='Bairro',
        ),
    ),

    StringField('emergency_city',
        widget=StringWidget(
	        label=_('City'),
        ),
    ),

    StringField('emergency_state',
        widget=StringWidget(
	        label=_('State'),
        ),
    ),
    
#===============================================================================
# O campo emergency_zipcode precisa de validador        
#===============================================================================
    
    StringField('emergency_zipcode',
        widget=StringWidget(
	        label=_('ZipCode'),
        ),
    ),
))
set_schemata_properties(EMERGENCY, schemata='Contato de Emergencia')

baseSchema = finalizeSchema(wresuser.WRESUserSchema.copy())

PatientSchema = baseSchema + MAIN + COMPLEMENTAR + GUARANTOR + CONVENIOS + DEMOGRAPHIC + EMPLOYMENT + EMERGENCY

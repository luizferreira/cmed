# coding=utf-8

from Products.Archetypes.atapi import *
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content import event

from wres.policy.utils.utils import set_schemata_properties, finalizeSchema

from zope.i18nmessageid import MessageFactory, Message

from wres.brfields.content.BrFieldsAndWidgets import *
from wres.brfields.validators import *

from wres.archetypes.validators import *
from wres.archetypes.widgets.BuildingBlocksWidget import BuildingBlocksWidget

_ = MessageFactory("cmfuemr")

#SEX = DisplayList((
    #('sdfdsafsdafe', 'pteste'),
    #('dasfesaefwf', 'pteste2'),
#))

#VISIT_REASON = DisplayList((
        #('office_visit',_('Office Visit')),
        #('follow_up', _('Follow Up')),
        #('work_up', _('Work Up')),
        #('pre_op', _('Pre Op')),
        #('six_months', _('6 months')),
        #('new_patient', _('New Patient')),
        #('np_cons', _('NP/Cons.')),
        #('consultation', _('Consultation')),
        #('stress_test', _('Stress Test')),
        #('plain', _('Plain')),
        #('thallium', _('Thallium')),
        #('adeno', _('Adeno')),
        #('walking-adeno', _('Walking-Adeno')),
        #('echo', _('Echo')),
        #('cdx', _('CDX')),
        #('pvs_left_leg', _('PVS Left Leg')),
        #('pvs_right_leg', _('PVS Right Leg')),
        #('pvs_both_legs', _('PVS Both Legs')),
        #('ultrasound_abdominal', _('Ultrasound Abdominal')),
        #('ultrasound_thyroid', _('Ultrasound Thyroid')),
        #('ultrasound_gb', _('Ultrasound GB')),
        #('ultrasound_kidney', _('Ultrasound Kidney')),
        #('holter', _('Holter')),
        #('event_monitor', _('Event Monitor')),
        #('bp_monitor', _('BP Monitor')),
        #('stress_echo', _('Stress Echo')),
        #('us_of_liver', _("US of Liver")),
        #('others', _('Other')),
    #))

MAIN = Schema((

        ReferenceField('patient',
            required = 1,
            relationship='patient',
            allowed_types=('Patient',),
            validators = ('isValidReference',),
#            default_method='default_patient',
#            vocabulary='default_patient_vocabulary',
            widget=BuildingBlocksWidget(label='Paciente',
#                                        label_msgid='cmfuemr_label_patient',
#                                        i18n_domain='cmfuemr',
                                        blocks=({'id':'popup_search', 'value':_('Search'), 'search_template': 'popup_choose_patient'},
                                                {'id':'popup_quick_register', 'value':_('Quick Register'), 'extra_fields':('birthDate', 'homePhone', 'mobile'), 'location':'/Patients'}),
                                        helper_js=('buildingblockwidget.js',),
                                        ),
        ),        
        
#        ReferenceField('doctor',
#            required=1,
#            relationship='doctor',
#            allowed_types=('Doctor',),
#            vocabulary_custom_label="b.Title",
#            widget=ReferenceBrowserWidget(label=_('Provider'),
#                                   startup_directory = 'Doctors',
#                                   ),
#        ),
        
        IntegerField('duration',
            required=1,
            widget=IntegerWidget(
                label=_('Duration'),
                description=_('Duration in minutes'),
            ),
        ),



        #StringField('visitReason',
            #required=1,
            #vocabulary=VISIT_REASON,
            #widget=SelectionWidget(label=_('Visit Reason'),
            #),
        #),
               
        BrPhoneField('contactPhone',
            index=':schema',
            widget=BrPhoneWidget(label=_('Contact Phone'),
                                     description='You must enter only numbers',
                                     description_msgid='cmfuemr_help_contact_phone',
                                     i18n_domain='cmfuemr',
            ),
        ),        

        # StringField('visit_type',
        #     required=True,
        #     vocabulary = "getTypesOfVisit",
        #     widget = SelectionWidget(
        #             label = 'Tipo de Consulta',
        #             macro_edit='generic_selection_edit_macro',
        #             helper_js=('generic_selection_edit.js', ),             
        #     ),
        # ),

        StringField('visit_type',
            required=True,
            default="1a Consulta",
            vocabulary = "getTypesOfVisit",
            widget = SelectionWidget(
                    label = 'Tipo de Consulta',
            ),
        ),

        StringField('visit_reason',
            required=False,
            vocabulary = "getVisitReason",
            widget = SelectionWidget(
                    label = 'Razão da Consulta',
                    macro_edit='generic_selection_edit_macro',
                    helper_js=('generic_selection_edit.js', ),             
            ),
        ),        
      
        StringField('insurance',
		required=False,
        vocabulary = "getInsurancesNames",
        widget = SelectionWidget(
                label = 'Plano de Saúde',
                macro_edit='insurance_selection_edit_macro',
                helper_js=('insurance_selection_edit.js', ),             
                ),
        ),
        StringField('note',
            widget=TextAreaWidget(label=_('Note'),
            ),
        ),                
        
))

set_schemata_properties(MAIN, schemata='default')

baseSchema = finalizeSchema(event.ATEventSchema.copy(), type='Visit')
#baseSchema = event.ATEventSchema.copy()

VisitSchema = baseSchema + MAIN                       

# move os campos patient e doctor para a 1a e 2a posicao, respectivamente.
VisitSchema._moveFieldToPosition('patient', 1)
# VisitSchema._moveFieldToPosition('doctor', 2)
VisitSchema._moveFieldToPosition('startDate', 2)
VisitSchema._moveFieldToPosition('duration', 3)

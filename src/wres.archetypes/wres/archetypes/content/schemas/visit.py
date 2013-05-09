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

_ = MessageFactory("cmfuemr")

MAIN = Schema((

        # Workaround
        # Os campos firstName e lastName estão aqui para não dar conflito no kssValidadeField
        # ao registrar uma novo paciente. Este problema ocorre pois são usados campos do Patient
        # no template visit_edit.pt, o kss tenta validar um campo do patient mas o contexto é a visita
        # e assim ocorre um erro.
        
        StringField('firstName',
        widget=StringWidget(
            label=_('First Name'),
            visible={'edit':'invisible','view':'invisible'},
        ),
    ),

        StringField('lastName',
            index="ZCTextIndex",
            widget=StringWidget(
                label=_('Last Name'),
                visible={'edit':'invisible','view':'invisible'},
            ),
        ),

        # Fim do workaround

        ReferenceField('patient',
            required = 1,
            relationship='patient',
            allowed_types=('Patient',),
            widget=ReferenceWidget(label='Paciente',
                                        macro_edit='visit_patient_selection_edit_macro',
                                        ),
        ),

        IntegerField('duration',
            required=1,
            widget=IntegerWidget(
                label=_('Duration'),
                description=_('Can be used to filter visits in calendar'),
            ),
        ),

        BrPhoneField('contactPhoneVisit',
            index=':schema',
            widget=BrPhoneWidget(label=_('Visit Contact Phone'),
                                     description='You must enter only numbers',
                                     description_msgid='cmfuemr_help_contact_phone',
                                     i18n_domain='cmfuemr',
            ),
        ),

        StringField('visit_type',
            required=True,
            default="1a Consulta",
            vocabulary = "getTypesOfVisit",
            widget = SelectionWidget(
                    label = 'Tipo de Visita',
                    description=_('Can be used to filter visits in calendar'),
            ),
        ),

        StringField('visit_reason',
            required=False,
            vocabulary = "getVisitReason",
            widget = SelectionWidget(
                    label = 'Razão da Visita',
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

))

set_schemata_properties(MAIN, schemata='default')

baseSchema = finalizeSchema(event.ATEventSchema.copy(), type='Visit')

VisitSchema = baseSchema + MAIN

# move os campos patient e doctor para a 1a e 2a posicao, respectivamente.
VisitSchema._moveFieldToPosition('patient', 1)
# VisitSchema._moveFieldToPosition('doctor', 2)
VisitSchema._moveFieldToPosition('startDate', 2)
VisitSchema._moveFieldToPosition('duration', 3)

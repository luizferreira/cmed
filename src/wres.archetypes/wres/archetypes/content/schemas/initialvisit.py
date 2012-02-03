#coding=utf-8

from DateTime import DateTime
from zope.i18nmessageid import MessageFactory, Message

from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from Products.Archetypes.atapi import *
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.DataGridField import FixedRow

from wres.archetypes.content.fields.defaultreferencefield import DefaultReferenceField
from wres.archetypes.content.medicaldocument import MedicalDocumentSchema
from wres.brfields.content.BrFieldsAndWidgets import *
from wres.brfields.validators import *
from wres.policy.utils.utils import set_schemata_properties

_ = MessageFactory("cmfuemr")

#===============================================================================
# Definição de algumas display lists utilizadas no schema
#===============================================================================

HISTORIES_VOCABULARY = DisplayList((
   ('medical_history','Denies Hypertension, Asthma, Epilepsy, Kidney disease.'),
   ('surgical_history','Negative'),
   ('family_history','No history of Hypertension, Diabetes, Coronary Artery disease, Kidney disease.'),
   ('social_history','Denies smoking, does not abuse alcohol, practices safe sex, excercises regularly.'),
   ('ob_gyn_history','Non Gravida, normal menstrual period, no hormonal replacement.'),
   ))

#===============================================================================
# Definição dos schemas de do tipo Initial Visits
#===============================================================================

SUBJECTIVE = Schema((

    StringField('chief_complaint',
        widget=TextAreaWidget(
            macro='autocomplete_string',
            label=_('Chief Complaint'),
            rows='1',
        ),
    ),

    StringField('present_illness',
        widget=TextAreaWidget(
            macro='autocomplete_string',
            label=_('History of Present Illness'),
            rows='2',
        ),
    ),

    StringField('past_history',
        subfields=('medical_history', 'surgical_history',
                   'ob_gyn_history', 'social_history','family_history',
        ),
        vocabulary=HISTORIES_VOCABULARY,
        is_subset = True,
        widget=TextAreaWidget(
            macro='autocomplete_string',
            label=_('Past History'),
            rows='2',
        ), 
    ),

    ReferenceField('ros',
        allowed_types=('ReviewOfSystems',),
        relationship='Owns',
        widget=ReferenceWidget(
            label=_('Review of Systems'),
            macro='ros_reference',
        ),
    ),

    DataGridField('allergies',
        columns=('allergy', 'reaction'),
        allow_empty_rows = False,
        allow_oddeven=True,
        widget=DataGridWidget(
        label=_('Allergies'),
            columns={
                'allergy' : Column('Alergia'),
                'reaction' : SelectColumn('Reação', vocabulary='getReactionValues'),
      	    },
        ),
    ), 
    
    #DataGridField('medication_taken',
        #columns=('medication', 'mg', 'use', 'start'),
        #allow_empty_rows = False,
        #allow_oddeven=True,
        #widget=DataGridWidget(
            #label=_('Medicamentos em uso'),
            #columns={
                #'medication' : Column('Medicamento'),
                #'mg' : Column('Concentração'),
                #'use' : Column('Uso'),
                #'start' : Column('Data', default=DateTime().strftime('%d/%m/%Y')),
            #},
        #),
    #),
))
set_schemata_properties(SUBJECTIVE, schemata='Subjetivo')

OBJECTIVE = Schema((

    DataGridField('vital_signs',
        columns=('blood_pressure', 'respiratory_rate', 'temperature', 'height', 'weight', 'IMC'),
        allow_empty_rows = False,
        allow_oddeven=True,
        widget=DataGridWidget(
        label=_('Sinais Vitais e Medidas'),
            columns={
                'blood_pressure' : Column('Pressão Arterial'),
                'respiratory_rate' : Column('Freqüência Respiratória'),
                'temperature' : Column('Temperatura'),
                'height' : Column('Altura'),
                'weight' : Column('Peso'),
      	    },
        ),
    ),
    
    DataGridField('laboratory',
        columns=('exam', 'value', 'date'),
        allow_empty_rows = False,
        allow_oddeven=True,
        widget=DataGridWidget(
            auto_insert = True,
            label=_('Laboratory'),
            columns={
                'exam' : Column('Exame'),
                'value' : Column('Valor'),
                'date' : Column('Data', default=DateTime().strftime('%d/%m/%Y')),
            },
        ),
    ),
    
    StringField('physical',
        widget=TextAreaWidget(
            macro='autocomplete_string',
            label=_('Physical'),
            rows='1',
        ),
    ),
    
    StringField('outros',
        widget=TextAreaWidget(
            macro='autocomplete_string',
            label=_('Outros'),
            rows='1',
        ),
    ),
))
set_schemata_properties(OBJECTIVE, schemata='Objetivo')

ASSESSMENT = Schema((

    DataGridField('diagnosis',
            columns=('desc', 'code', 'date', 'status'),
            allow_empty_rows = False,
            allow_oddeven=True,
            widget = DataGridWidget(
                label='Diagnóstico',
                columns={
                    'desc' : Column('Descrição'),
                    'code' : Column('CID'),
                    'date' : Column('Data', default=DateTime().strftime('%d/%m/%Y')),
                    'status' : SelectColumn('Estado', vocabulary='getStatusValues'),
      	        },
            ),
        ),

))
set_schemata_properties(ASSESSMENT, schemata='Avaliacao')

PLANS = Schema((   

    DataGridField('prescription',
        columns=('medication', 'concentration', 'quantity', 'use', 'start'),
        allow_empty_rows = False,
        allow_oddeven=True,
        widget=DataGridWidget(
            label=_('Prescription'),
            columns={
                'medication' : Column('Medicamento'),
                'concentration' : Column('Concentração'),
                'quantity' : Column('Quantidade'),
                'use' : Column('Uso'),
                'start' : Column('Data', default=DateTime().strftime('%d/%m/%Y')),
      	    },
        ),
    ),

    StringField('non_prescription',
        widget=TextAreaWidget(
            macro='autocomplete_string',
            label=_('Recommendations'),
            rows='2',
        ),
    ),
    
    StringField('obs',
        widget=TextAreaWidget(
            macro='autocomplete_string',
            label='Observações',
            rows='2',
        ),
    ),

))
set_schemata_properties(PLANS, schemata='Planos')

InitialVisitSchema = MedicalDocumentSchema + SUBJECTIVE + OBJECTIVE + ASSESSMENT + PLANS 

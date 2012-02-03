# coding=utf-8

from DateTime import DateTime
from zope.i18nmessageid import MessageFactory, Message

from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from Products.Archetypes.atapi import *
from Products.Archetypes.interfaces.vocabulary import IVocabulary
from Products.Archetypes.Registry import setSecurity
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from wres.archetypes.content.fields.defaultreferencefield import DefaultReferenceField
from wres.archetypes.content.medicaldocument import MedicalDocumentSchema
from wres.brfields.content.BrFieldsAndWidgets import *
from wres.brfields.validators import *
from wres.policy.utils.utils import set_schemata_properties

_ = MessageFactory("cmfuemr")

class MyDisplayList:

    __implements__ = (IVocabulary,)

    def __init__(self, tuples):
        self.tuples = tuples

    def __getitem__(self, item):
        return self.tuples[item]

    def getDisplayList(self, instance):
        retval = [item for item in self.tuples]
        return DisplayList(retval)

    def getThirdElement(self, id):
        retval = [elem[2] for elem in self.tuples if elem[0] == id]
        if len(retval) == 0:
            return None
        return retval[0]

    def __contains__(self, id):
        retval = [elem[2] for elem in self.tuples if elem[0] == id or elem[2] == id]
        return (len(retval) != 0)

    def getTuples(self):
        return self.tuples

    def keys(self):
        return []

setSecurity(MyDisplayList, defaultAccess='allow')

HISTORICO_PREGRESSO = MyDisplayList((
    ('1º Contato',_('first contact'),'checkbox'),
    ('Consultas Prévias',_('previous consultation'), 'checkbox'),
    ('Cirurgias Anteriores',_('previous surgeries'),'checkbox'),
    ))
    
HISTORIES_VOCABULARY = DisplayList((
                                    ("medical_history","Denies Hypertension, Asthma, Epilepsy, Kidney disease."),
                                    ("surgical_history","Negative"),
                                    ("ob_gyn_history","Non Gravida, normal menstrual period, no hormonal replacement."),
                                  ))

PARTO = MyDisplayList((
    ('Parto normal',_('natural childbirth'),'checkbox'),
    ('Cesariana',_('Cesarean'), 'checkbox'),
    ))
    
GESTACAO = MyDisplayList((
    ('Sim','yes','checkbox'),
    ('Não','no', 'checkbox'),
    ))
    
MEDICAMENTOS = MyDisplayList((
    ('AAS','AAS','checkbox'),
    ('IMAO','IMAO','checkbox'),
    ('ACO','ACO','checkbox'),
    ('Corticóides','Corticóides','checkbox'),
    ('Antidepressivos','Antidepressivos','checkbox'),
    ('Ansiolítico','Ansiolítico','checkbox'),
    ('Antihipertensivos','Antihipertensivos','checkbox'),
    ('Insulina','Insulina','checkbox'),
    ))
    
HABITOS = MyDisplayList((
    ('Tabagismo','Tabagismo','checkbox'),
    ('Etilismo','Etilismo','checkbox'),
    ('Toxicomania','Toxicomania','checkbox'),
    ('Sedentarismo','Sedentarismo','checkbox'),
    ))
        
CHECAGEM = MyDisplayList((
    ('Orientação sobre a cirurgia','Orientação sobre a cirurgia','checkbox'),   
    ('Entregue texto explicativo geral','Entregue texto explicativo geral','checkbox'),
    ('Entregue texto explicativo especifico','Entregue texto explicativo especifico','checkbox'),
    ('Entregue manual de cuidados pré e pós','Entregue manual de cuidados pré e pós','checkbox'),
    ('Capturada a imagem','Capturada a imagem','checkbox'),
    ('Feito orçamento','Feito orçamento','checkbox'),
    ('Marcada a cirurgia','Marcada a cirurgia','checkbox'),
    ('Pedido de exames pré-operatórios','Pedido de exames pré-operatórios','checkbox'),
    ))
    
FRENTE = Schema((
 
    #Inicial
    StringField('chief_complaint',
        widget=TextAreaWidget(
            label='Queixa principal',
            label_msgid='cmfuemr_chief_complaint',
            i18n_domain='cmfuemr',
            size=85,
        ),
    ),            
        
    StringField('hma',
        widget=TextAreaWidget(
            label='HMA',
            text_type='textarea',
            rows='3',
            size='85',
            num_inputs=1,
        ),
    ),
    
    StringField('conhecimento',
        widget=TextAreaWidget(
            label='Conhecimento sobre o tratamento',
            text_type='textarea',
            rows='2',
            size='85',
        ),
    ),
    StringField('pretensao',
        widget=TextAreaWidget(
            label='Pretensão estética / Espectativas',
            text_type='textarea',
            rows='2',
            size='85',
        ),
    ),
    
    #Historico Pregresso em Cirurgia Plástica        
    
   
    StringField('historico_cirurgia',
        multiValued=1,
        vocabulary=HISTORICO_PREGRESSO,
        widget=MultiSelectionWidget(
            label='Histórico Pregresso em Cirurgia Plástica', 
            format='checkbox',
            #num_checkboxes=3,
            cols=3,
            other=1,
        ),
    ),
    

#-------------------------------------------------------------------------
#    O widget historico_patologia abaixo foi modificado para atingirmos a versão 1.0 do sistema.
#    
#    Em vez de ter um campo com vários subcampos, colocaremos vários campos
#    em formato string básico.
#
#    A seguir o campo original:
#------------------------------------------------------------------------------ 

        #História Patológica Pregressa


#        RecordField('historico_patologia',
#        StringField('historico_patologia',
##                     widget=HistoriaPatologicaWidget(label='História Patológica Pregressa',
#                      widget=TextAreaWidget(label='História Patológica Pregressa',
#                                            rows='3',
#                                            text_type='textarea',),
#                     subfields=('pat_cli_tratadas', 'pat_cli_sem_controle', 'pat_cli_com_controle',
#                                'pat_cirurgica', 'anestesias', 'problemas_anteriores',
#                                ),
#                     vocabulary=HISTORIES_VOCABULARY,
#                     is_subset = True,
#        ),
    
    StringField('pat_cli_tratadas',
        widget=TextAreaWidget(
            label='Patologias Clínicas já tratadas',
            visible={'edit': 'visible',
                     'view': 'visible'},
            size=85,
        ),
    ),
    
    StringField('pat_cli_sem_controle',
        widget=TextAreaWidget(
            label='Patologias Clínicas sem controle',
            visible={'edit': 'visible',
                     'view': 'visible'},
            size=85,
        ),
    ),
    
    StringField('pat_cli_com controle',
        widget=TextAreaWidget(
            label='Patologias Clínicas com controle',
            visible={'edit': 'visible',
                     'view': 'visible'},
            size=85,
        ),
    ),
    
    StringField('pat_cirurgia',
        widget=TextAreaWidget(
              label='Patologias Cirúrgicas',
              visible={'edit': 'visible',
                       'view': 'visible'},
              size=85,
        ),
    ),
    
    StringField('anestesias',
        widget=TextAreaWidget(
            label='Anestesias',
            visible={'edit': 'visible',
                     'view': 'visible'},
            size=85,
        ),
    ),
    
    StringField('problemas_anteriores',
        widget=TextAreaWidget(
            label='Problemas anteriores',
            visible={'edit': 'visible',
                     'view': 'visible'},
            size=85,
        ),
    ),
    
    
    #História Gineco-Obstétrica
    
    StringField('GPA',
        widget=TextAreaWidget(
            label='G.P.A.',
            visible={'edit': 'visible',
                     'view': 'hidden'},
            size=85,
        ),
    ),
    
    StringField('parto',
        multiValued=0,
        vocabulary=PARTO,
        widget=MultiSelectionWidget(
            label='',
            format='checkbox',
            num_checkboxes=2,
            cols=2,
            other=0,
        ),
    ),
    
    
    StringField('idade_filhos',
        widget=TextAreaWidget(
            label='Idade dos filhos',
            visible={'edit': 'visible',
                     'view': 'hidden'},
            rows=1,
        ),
    ),
    
    StringField('ciclos_menstruais',
        widget=TextAreaWidget(
            label='Ciclos menstruais',
            visible={'edit': 'visible',
                     'view': 'hidden'},
        ),
    ),
    
    
    StringField('planeja_gestacoes',
        multiValued='0',
        vocabulary=GESTACAO,
        widget=TextAreaWidget(
            label='Planeja gestações? Quando?',
            num_checkboxes='2',
            rows='1',
            cols='2',
            other='1',
        ),
    ),
    
    StringField('metodo_anticoncepcional',
        widget=TextAreaWidget(
            label='Método Anticoncepcional',
            visible={'edit': 'visible',
                     'view': 'hidden'},
            rows='1',
        ),
    ),
    
    StringField('exames_anteriores',
        widget=TextAreaWidget(
            label='Exames Ginecológicos Anteriores',
            visible={'edit': 'visible',
                     'view': 'hidden'},
        ),
    ),
    
    StringField('ginecologista',
        widget=TextAreaWidget(
            label='Ginecologista',
            visible={'edit': 'visible',
                     'view': 'hidden'},
        ),
    ),
    
    StringField('Peso',
        widget=StringWidget(
            label='Peso (Kg)',
            visible={'edit': 'visible',
                     'view': 'hidden'},
            size='5',
        ),
    ),

    StringField('Altura',
        widget=StringWidget(
            label='Altura (m)',
            visible={'edit': 'visible',
                     'view': 'hidden'},
            size='5',
        ),
    ),

    StringField('Soutien',
        widget=StringWidget(
            label='Soutien',
            visible={'edit': 'visible',
                     'view': 'hidden'},
            size='5',
        ),
    ),

    

))
set_schemata_properties(FRENTE, schemata='Frente')

VERSO = Schema((
                
    DataGridField('allergies',
        columns=('allergy', 'reaction'),
        allow_oddeven=True,
        widget=DataGridWidget(
              label='Allergies',
              columns={
                  'allergy' : SelectColumn("Alergia", vocabulary="getAllergyValues"),
                  'reaction' : SelectColumn("Reação", vocabulary="getReactionValues"),
              },
              label_msgid='cmfuemr_label_allergies',
              i18n_domain='cmfuemr',
        ),
    ),

    StringField('medicamentos',
        multiValued=1,
        #schemata='Frente',Review of Systems
        vocabulary=MEDICAMENTOS,
#            widget=MultipleCheckboxWidget(label=' ',
        widget=MultiSelectionWidget(
            label='', 
            format='checkbox',
            num_checkboxes='8',
            cols='2',
            other='1',
        ),
    ),
    
    #Hábitos             
    StringField('habitos',
        multiValued='1',
        vocabulary=HABITOS,
        widget=MultiSelectionWidget(
            label='', 
            format='checkbox',
            num_checkboxes=4,
            cols=2,
            other=1,
        ),
    ),
    
    #Diagnósticos
    
    StringField('diagnostico',
        widget=TextAreaWidget(
            label='',
            rows='3',
            size='85',
            num_inputs=1,
        ),
    ),

    #Tratamento proposto
    
    StringField('tratamento',
        widget=TextAreaWidget(
            label='',
            rows='3',
            size='85',
            num_inputs=1,
        ),
    ),

    #Checagem
    
    StringField('checagem',
        multiValued=1,
        vocabulary=CHECAGEM,
#            widget=MultipleCheckboxWidget(label=' ', ',
        widget=MultiSelectionWidget(
            label='', 
            format='checkbox',
            num_checkboxes=8,
            cols=2,
            other=0,
        ),
    ),
    
    #Comentários, observações e Condutas Iniciais
    StringField('comentarios',
        widget=TextAreaWidget(
            label='',
            text_type='textarea',
            rows='3',
            size='85',
            num_inputs=1,
        ),
    ),


    
))
set_schemata_properties(VERSO, schemata='Verso')
        
DocPlasticaSchema = MedicalDocumentSchema + FRENTE + VERSO 

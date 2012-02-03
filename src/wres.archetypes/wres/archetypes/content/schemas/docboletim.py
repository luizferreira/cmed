# coding=utf-8

from DateTime import DateTime
from zope.i18nmessageid import MessageFactory, Message

from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from Products.Archetypes.atapi import *
from Products.Archetypes.interfaces.vocabulary import IVocabulary
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

LEAVE_TYPES = DisplayList((
    ('local','LOCAL'),
    ('local_sedacao','LOCAL SEDAÇÃO'),
    ('geral_venosa','GERAL VENOSA'),
    ('geral_inalatoria','GERAL INALATÓRIA'),
    ('geral_balanceada','GERAL BALANCEADA'),
    ('raqui','RAQUI'),
    ('peridural','PERIDURAL'),
    ('pridural_toracica','PERIDURAL TORÁCICA'),
    ('outra','OUTRA'),
))

NATUREZA_PROCEDIMENTO = DisplayList((
    ('estetica', 'ESTÉTICA'),
    ('reconstrutiva', 'RECONSTRUTIVA'),
    ('estetica_reconstrutiva', 'ESTÉTICA E RECONSTRUTIVA'),
))

POSICIONAMENTO = DisplayList((
    ('decubito_dorsal', 'DECÚBITO DORSAL'),
    ('decubito_ventral', 'DECÚBITO VENTRAL'),
    ('decubito_lateral', 'DECÚBITO LATERAL'),
    ('mudanca_decubital', 'MUDANÇA DECUBITAL'),
    ('membros_abduzidos', 'MEMBROS ABDUZIDOS'),
    ('membros_aduzidos', 'MEMBROS ADUZIDOS'),
))

ANTISSEPSIA = DisplayList((
    ('pvpi_degermante', 'PVPI DEGERMANTE'),
    ('pvpi_topico', 'PVPI TÓPICO'),
    ('clorohexidina', 'CLOROHEXIDINA'),
    ('triclosan', 'TRICLOSAN'),
    ('alcooliodado', 'ALCOOLIODADO'),
    ('decubito_lateral', 'DECÚBITO LATERAL'),
))

MEDICACAO_EXTRA = DisplayList((
    ('zofran', 'ZOFRAN'),
    ('keflin', 'KEFLIN'),
    ('bufedil', 'BUFEDIL'),
))

ANATOMO_PATOLOGICO = DisplayList((
    ('sim', 'SIM'),
    ('nao', 'NÃO'),
))

FRENTE = Schema((
    
    #Campo "Local".
    StringField('local',
        widget=TextAreaWidget(
            label='Local da cirurgia',
            visible={'edit':'visible',
                   'view': 'visible'},
            rows='1',
            size='132'
        ),
    ),
    
    #Campos "Início".
    #StringField('inicio',
    #    widget=TextAreaWidget(label='Início',
    #                        size= 6),
    #),
    #
    #Campos "Término".
    #StringField('termino',
    #    widget=TextAreaWidget(label='Término',
    #                        size= 6),
    #),
    
    #Campos "Duração".
    #StringField('duracao',
    #    widget=TextAreaWidget(label='Duração',
    #                        size= 6),
    #), 
    
    #Campo "Natureza do Procedimento".
    #StringField('natureza_procedimento',
    #    vocabulary=NATUREZA_PROCEDIMENTO,
    #    widget=SelectionWidget(
    #        label='Natureza do Procedimento',
    #        format='radio',
    #    ),
    #),
    
    #Campo "Procedimentos Realizados".
    StringField('procedimentos',
        multiValued=1,
        widget=TextAreaWidget(
            label='Procedimentos Realizados',
            text_type='textarea',
            rows='3',
            size='83',
            num_inputs=1,
        ),
    ),
    
    #Campo "Anestesia Empregada".
    StringField('anestesia_empregada',
        vocabulary=LEAVE_TYPES,
        widget=TextAreaWidget(
            label='Anestesia Empregada',
            visible={'edit':'visible',
                   'view': 'visible'},
            rows='1',
            size='150'
        ),
    ),
        

    #Campo "Cirurgiões".
    StringField('cirurgiao',
        widget=TextAreaWidget(
            label='Cirurgião',
            visible={'edit':'visible',
                   'view': 'visible'},
            rows='1',
            size='150',
        ),
    ),
    
    #Campo "Cirurgião Auxiliar".
    StringField('auxiliar',
        widget=TextAreaWidget(
            label='Auxiliar',
            visible={'edit':'visible',
                     'view': 'visible'},
            rows='1',
            size='150',
        ),
    ),
    
    #Campo "Anestesologista".
    StringField('anestesiologista',
        widget=TextAreaWidget(
            label='Anestesiologista',
            visible={'edit':'visible',
                   'view': 'visible'},
            rows='1',
            size='150',
        ),
    ),                    

    #Campo "Instrumentadores".
    StringField('instrumentadores',
        widget=TextAreaWidget(
            label='Instrumentadores',
            visible={'edit':'visible',
                   'view': 'visible'},
            rows='1',
            size='150',
        ),
    ),        
    
    #Campo "Acadêmicos".
    #StringField('academicos',
    #    widget=TextAreaWidget(label='Acadêmicos',
    #                        visible={'edit':'visible',
    #                                 'view': 'visible'},
    #                        size='150',),
    #),        
    
    #Campo "Circulante".
    StringField('circulante',
        widget=TextAreaWidget(
            label='Circulante',
            visible={'edit':'visible',
                   'view': 'visible'},
            rows='1',
            size='150',
        ),
    ),    
    
    #Campo "Fechamento"
    #RecordsField('fechamento',
    #    subfields = ('regiao', 'cirurgiao'),
    #    subfield_labels ={'regiao':'Descricao', 'cirurgiao':'Cirurgiao'},
    #    widget=FechamentoWidget(
    #        label='Fechamento',
    #    ),
    #),

    # - DESCRIÇÃO DO ATO CIRÚRGICO -
    
    #Campo - "Posicionamento".
    LinesField('posicionamento',
        vocabulary=POSICIONAMENTO,
        widget=MultiSelectionWidget(
            label='Posicionamento', 
            format='checkbox',),                                                                  
    ),   
    
    #Campo - "Antissepsia do Campo Operatório".
    LinesField('antissepsia',
        vocabulary=ANTISSEPSIA,
        widget=MultiSelectionWidget(
            label='Antissepsia do Campo Operatório',
            format='checkbox',),
    ),
    
    
    DataGridField('anestesia_local',
            columns=('regiao', 'adrenalina', 'volume_infiltrado', 'porcentagem'),
            widget=DataGridWidget(
                label='Anestesia Local',
                columns={
                    'regiao' : Column("Região"), 
                    'adrenalina' : Column("Adrenalina (1:________)"),
                    'volume_infiltrado' : Column("Volume infiltrado (ml)"),
                    'porcentagem' : Column("Porcentagem (%)"),
                },
            ),
    ),
    
    #Campo - "Medicação Extra".
    #LinesField('medicacao_extra',
    #    vocabulary=MEDICACAO_EXTRA,
    #    widget=MultiSelectionWidget(
    #        label='Medicação Extra',
    #        format='checkbox',),
    #),
    
))

set_schemata_properties(FRENTE, schemata='Frente')

VERSO = Schema((

    #StringField('incisoes_cirurgicas',
    #    widget=TextAreaWidget(
    #        label='Incisões Cirúrgicas',
    #        rows='2',
    #        size='10',
    #        visible={'edit':'visible',
    #                 'view':'visible'},
    #    ),
    #),
    
    #StringField('tecnica_cirurgica',
    #    widget=TextAreaWidget(
    #        label='Técnica Cirúrgica Empregada',
    #        size='150',
    #        rows='3',
    #        visible={'edit':'visible',
    #                 'view': 'visible'},
    #         
    #     ),
    #),

    StringField('descricao',
        widget=TextAreaWidget(
            label='Descrição',
            cols='10',
            visible={'edit':'visible',
                     'view':'visible'},
        ),
    ),

    StringField('dificuldades_tecnicas',
        widget=TextAreaWidget(
            label='Dificuldades Técnicas',
            size='150',
            visible={'edit':'visible',
                     'view': 'visible'},
        ),
    ),    
    
    StringField('intercorrencias',
        widget=TextAreaWidget(
            label='Intecorrências Cirúrgicas e/ou Anestésicas',
            size='150',
            visible={'edit':'visible',
                     'view': 'visible'},
        ),
    ),        
    
    StringField('impressao_final',
        widget=TextAreaWidget(
            label='Impressão Final',
            size='150',
            visible={'edit':'visible',
                     'view': 'visible'},
         ),
    ),

    #RecordsField('suturas',
    #    subfields = ('local', 'tipo_de_fio'),
    #    subfield_labels ={'local':'Local/Tipo de Sutura', 'tipo_de_fio':'Tipo de Fio'},
    #        widget=SuturasWidget(
    #            label='Suturas e Fios',
    #        ),
    #),
    
    #RecordsField('curativo',
    #    subfields = ('local', 'micropore', 'gazes', 'pomada', 'crepom', 'modelador'),      
    #    widget=CurativosWidget(
    #        label='Curativos',
    #    ),              
    #),

                     
    DataGridField('proteses',
        columns=('proteses','dir', 'esq'),
        allow_oddeven=True,
        fixed_rows = [
            FixedRow(keyColumn="proteses", initialData = { "proteses" : "tipo"}),
            FixedRow(keyColumn="proteses", initialData = { "proteses" : "forma"}),
            FixedRow(keyColumn="proteses", initialData = { "proteses" : "perfil"}),
            FixedRow(keyColumn="proteses", initialData = { "proteses" : "volume"}),
        ],
        widget=DataGridWidget(
            label='Próteses',
            columns={
                'proteses' : SelectColumn("Prótese", vocabulary="getProtese"), 
                'dir' : Column("Direita"),
                'esq' : Column("Esquerda"),
            },
        ),
    ),
   
    
    StringField('anatomo_patologico',
        vocabulary=ANATOMO_PATOLOGICO,
#        widget=SelectionWidget(
        widget=TextAreaWidget(
            label='Anátomo-Patológico',
            format='radio',
        ),
    ),                
                        
    DataGridField('regiao_lipoaspirada',
        columns=('regiao','dir', 'esq'),
        allow_oddeven=True,
        fixed_rows = [
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "abdome"}),
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "flancos"}),
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "dorso"}),
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "culotes"}),
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "face_int_coxa"}),
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "axilas"}),
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "cauda_mamaria"}),
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "joelhos"}),
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "outros"}),
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "volume_total_aspirado"}),
            FixedRow(keyColumn="regiao", initialData = { "regiao" : "volume_enxertado"}),
        ],
        widget=DataGridWidget(
            label='Regiao Lipoaspirada',
            columns={
                'regiao' : SelectColumn("Região", vocabulary="getRegiaoLipoaspirada"), 
                'dir' : Column("Direita"),
                'esq' : Column("Esquerda"),
            },
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
        
DocBoletimSchema = MedicalDocumentSchema + FRENTE + VERSO 

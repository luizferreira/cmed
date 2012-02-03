# coding=utf-8

from Products.Archetypes.atapi import *
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.content import schemata
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema

from zope.i18nmessageid import MessageFactory, Message

_ = MessageFactory("cmfuemr")

MAIN = Schema((
        
        ReferenceField('doctor',
            required=1,
            relationship='doctor',
            allowed_types=('Doctor',),
            vocabulary_custom_label='b.Title',
            widget=ReferenceBrowserWidget(
                label=_('Provider'),
                startup_directory = 'Doctors',
            ),
        ),

        StringField('general',
            widget=TextAreaWidget(
                label='Tem febre, fraqueza, tonturas, suor frio, desmaio, tremor, dor de cabeça?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),

        StringField('eyes',
            widget=TextAreaWidget(
                label='Tem problemas de vista? Qual? Usa óculos? Data do último exame de vista?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('nose',
            widget=TextAreaWidget(
                label='Tem sintomas no nariz? Coriza, espirros, obstrução, sinusite?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('ears',
            widget=TextAreaWidget(
                label='Tem boa audição? Sente algo nos ouvidos?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('mouth',
            widget=TextAreaWidget(
                label='Tem sintomas na boca, gengivas, língua ou garganta?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('teeth',
            widget=TextAreaWidget(
                label='Tem dentes naturais? Estão com problema? Data da última visita ao dentista?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('respiratory',
            widget=TextAreaWidget(
                label='Tem ou teve doença respiratória? Asma, pneumonia, tuberculose? Tosse? Cheira? Escarro?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('cardiovascular',
            widget=TextAreaWidget(
                label='Tem ou teve pressão alta ou doença do coração? Inchaço nas pernas? Falta de ar?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('stomach',
            widget=TextAreaWidget(
                label='Tem sintomas estomacais? Dificuldade para engolir? Úlcera, gastrite, refluxo?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('pancres',
            widget=TextAreaWidget(
                label='Tem ou teve doença do pâncreas, fígado, vesícula biliar ou hemorróidas?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('intestine',
            widget=TextAreaWidget(
                label='Intestino preso? Diarréia? Muco nas fezes? Gazes? Sangramento retal? Dor no abdômen?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('urinary',
            widget=TextAreaWidget(
                label='A urina está normal? Com sangue? Sintomas urinários?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('ortopedics',
            widget=TextAreaWidget(
                label='Tem ou teve doença ortopédica? Coluna, juntas, ossos, tendinite, gota?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('legs',
            widget=TextAreaWidget(
                label='Tem doenças nas pernas e pés? Varizes, flebite, trombose, ferida crônica?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('glands',
            widget=TextAreaWidget(
                label='Tem diabetes, doença da tireóide ou de outra glândula?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('tegumentar',
            widget=TextAreaWidget(
                label='Tem doença de pele, cabelo, unhas ou venérea?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('neurological',
            widget=TextAreaWidget(
                label='Tem ou teve doenças neurológicas? Epilepsia, derrame, isquemia cerebral transitória? Doença de Parkinson?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('apetite',
            widget=TextAreaWidget(
                label='Como está o apetite? Aumentado? Diminuído? Faz dieta especial?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('weight',
            widget=TextAreaWidget(
                label='Como está o seu peso? Emagreceu? Engordou? Quantos quilos em quanto tempo?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('sleep',
            widget=TextAreaWidget(
                label='Como está o seu sono?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('drink_smoke',
            widget=TextAreaWidget(
                label='Fuma ou bebe? O quê? Quanto e por quanto tempo?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('exercises',
            widget=TextAreaWidget(
                label='Pratica exercícios físicos? Quais? Quantas vezes por semana?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('sex',
            widget=TextAreaWidget(
                label='Vida sexual ativa? Inativa? Sem interesse? Problemas?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('surgery',
            widget=TextAreaWidget(
                label='Fez cirurgias? Quais? Em que ano?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('internation',
            widget=TextAreaWidget(
                label='Ficou internado nos últimos dois anos? Por qual motivo? Quando?',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('family_diseases',
            default='Tuberculose( ), Câncer( ), Pressão alta( ), Infarto( ), Derrame( ), Diabetes( ),' \
                    'Pedra na vesícula( ), Doença da Tireóide( ), Depressão( ), Ansiedade( ), Outras - Especifique( )',
            widget=TextAreaWidget(
                label='Quantos parentes seus (qualquer grau) tiveram estas doenças?',
                description ='Digite o número dentro dos parênteses',
                rows=2,
            ),
        ),
        
        StringField('sons',
            widget=TextAreaWidget(
                label='Teve filhos? Quantos partos? Quantas cesáreas? Quantos abortos? Teve gêmeos?',
                description='Somente para mulheres',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('utero',
            widget=TextAreaWidget(
                label='Teve ou teve alguma doença de mama, ovários, trompas ou útero?',
                description='Somente para mulheres',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('gineco_mamo',
            default='Exame ginecológico:        Mamografia:',
            widget=TextAreaWidget(
                label='Data do último exame ginecológico? Data da última mamografia?',
                description='Somente para mulheres',
                rows=2,
            ),
        ),
        
        StringField('menstruacao',
            widget=TextAreaWidget(
                label='Seu ciclo e regular? Cólicas? Tem TPM? Qual seu método contraceptivo?',
                description='Somente para quem menstrua',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('menopausa',
            widget=TextAreaWidget(
                label='Teve menopausa com quantos anos? Sente onda de calor? Usa hormônios? Quais?',
                description='Somente para quem teve manopausa',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('man_genital',
            widget=TextAreaWidget(
                label='Tem ou teve algum problema genital? Pênis, próstata, testículos?',
                description='Somente para homens',
                macro='autocomplete_string',
                rows=2,
            ),
        ),
        
        StringField('ex_prevencao',
            widget=TextAreaWidget(
                label='Data do último exame de prevenção: Toque retal, dosagem de PSA no sangue?',
                description='Somente para homens',
                macro='autocomplete_string',
                rows=2,
            ),
        ),

))

set_schemata_properties(MAIN, schemata='Principal')

baseSchema = finalizeSchema(schemata.ATContentTypeSchema.copy())

ReviewOfSystemsSchema = baseSchema + MAIN

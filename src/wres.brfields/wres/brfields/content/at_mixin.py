# -*- coding: utf-8 -*-
__author__ = """Simples Consultoria <contato@simplesconsultoria.com.br>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *

from wres.brfields.content.BrFieldsAndWidgets import *
from Products.CMFPlone.utils import getToolByName

from wres.brfields import MessageFactory as _

schema = Schema((
    StringField(
        name='logradouro',
        widget=StringWidget(
            size="30",
            description="Exemplo: Rua Mourato Coelho",
            visible={'view':'invisible', 'edit':'visible'},
            label='Logradouro',
            label_msgid='BrFieldsAndWidgets_label_logradouro',
            description_msgid='BrFieldsAndWidgets_help_logradouro',
            i18n_domain='Products.BrFieldsAndWidgets',
        ),
        required=1,
        schemata="Address"
    ),
    
    StringField(
        name='numero',
        widget=StringWidget(
            size="7",
            description="12",
            visible={'view':'invisible', 'edit':'visible'},
            label='Número',
            label_msgid='BrFieldsAndWidgets_label_numero',
            description_msgid='BrFieldsAndWidgets_help_numero',
            i18n_domain='Products.BrFieldsAndWidgets',
        ),
        required=1,
        schemata="Address"
    ),
    
    StringField(
        name='complemento',
        widget=StringWidget(
            visible={'view':'invisible', 'edit':'visible'},
            label='Complemento',
            label_msgid='BrFieldsAndWidgets_label_complemento',
            i18n_domain='Products.BrFieldsAndWidgets',
        ),
        schemata="Address"
    ),
    
    StringField(
        name='bairro',
        widget=StringWidget
        (
            description="Exemplo: Pinheiros.",
            visible={'view':'invisible', 'edit':'visible'},
            size="30",
            label='Bairro',
            label_msgid='BrFieldsAndWidgets_label_bairro',
            description_msgid='BrFieldsAndWidgets_help_bairro',
            i18n_domain='Products.BrFieldsAndWidgets',
        ),
        required=0,
        schemata="Address",
    ),
    
    CEPField(
        name='cep',
        required=1,
        widget=CEPWidget(   
                        description="Informe o CEP.",
                        visible={'view':'invisible', 'edit':'visible'},
                        label='CEP',
                        label_msgid='BrFieldsAndWidgets_label_cep',
                        description_msgid='BrFieldsAndWidgets_help_cep',
                        ),
        schemata="Address"
    ),
    
    StringField(
        name='cidade',
        widget=StringWidget(
            description="Informe sua cidade.",
            visible={'view':'invisible', 'edit':'visible'},
            label='Cidade',
            label_msgid='BrFieldsAndWidgets_label_cidade',
            description_msgid='BrFieldsAndWidgets_help_cidade',
            i18n_domain='Products.BrFieldsAndWidgets',
        ),
        required=1,
        schemata="Address"
    ),
    
    StringField(
        name='uf',
        widget=SelectionWidget
        (
            description="Informe seu estado.",
            visible={'view':'invisible', 'edit':'visible'},
            size="1",
            label='Uf',
            label_msgid='BrFieldsAndWidgets_label_uf',
            description_msgid='BrFieldsAndWidgets_help_uf',
            i18n_domain='Products.BrFieldsAndWidgets',
        ),
        required=1,
        schemata="Address",
        vocabulary='vocLstUF',
        enforceVocabulary=1
    ),
    
    ComputedField(
        name='Endereco',
        expression='context.fmt_endereco()',
        widget=ComputedWidget(
            visible={'view':'visible', 'edit':'invisible'},
            label='Endereco',
            label_msgid='BrFieldsAndWidgets_label_Endereco',
            i18n_domain='Products.BrFieldsAndWidgets',
        ),
        default_output_type='text/x-html-safe',
        schemata="Address",
        searchable=1
    ),
    
    TextField(
        name='referencia',
        allowable_content_types=('text/html',),
        widget=RichWidget
        (
            description="Informe pontos de referência.",
            visible={'view':'invisible', 'edit':'invisible'},
            label='Referencia',
            label_msgid='BrFieldsAndWidgets_label_referencia',
            description_msgid='BrFieldsAndWidgets_help_referencia',
            i18n_domain='Products.BrFieldsAndWidgets',
        ),
        required=0,
        schemata="Address",
        searchable=1,
        default_output_type='text/x-html-safe'
    ),

),
)

br_endereco_schema = BaseSchema.copy() + \
    schema.copy()


class br_endereco:
    """Classe basica de endereco
    """
    security = ClassSecurityInfo()

    # This name appears in the 'add' box
    archetype_name = 'br_endereco'

    meta_type = 'br_endereco'
    portal_type = 'br_endereco'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'br_endereco.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "br_endereco"
    typeDescMsgId = 'description_edit_br_endereco'

    _at_rename_after_creation = True

    schema = br_endereco_schema

    security.declarePrivate('fmt_endereco')
    def fmt_endereco(self):
        """Retorna um endereco formatado para o atributo Endereco
        """
        template = "%s,%s %s<br/>%s<br/>%s<br/>%s - %s"
        logradouro = self.getLogradouro()
        numero = self.getNumero()
        complemento = self.getComplemento()
        bairro = self.getBairro()
        cep = self.getCep()
        if cep:
            cep = "%s-%s" % (cep[:5], cep[-3:])
        cidade = self.getCidade()
        uf= self.getUf()

        return template % (logradouro, numero, complemento, bairro, cep, cidade, uf)


    security.declarePrivate('vocLstUF')
    def vocLstUF(self):
        """Retorna lista de unidades da federacao
        """
        uf = [
            ('','Selecione'),
            ('AC',u'Acre'),
            ('AL',u'Alagoas'),
            ('AM',u'Amazonas'),
            ('AP',u'Amapá'),
            ('BA',u'Bahia'),
            ('CE',u'Ceará'),
            ('DF',u'Distrito Federal'),
            ('ES',u'Espírito Santo'),
            ('GO',u'Goiás'),
            ('MA',u'Maranhão'),
            ('MG',u'Minas Gerais'),
            ('MS',u'Mato Grosso do Sul'),
            ('MT',u'Mato Grosso'),
            ('PA',u'Pará'),
            ('PB',u'Paraíba'),
            ('PE',u'Pernambuco'),
            ('PI',u'Piauí'),
            ('PR',u'Paraná'),
            ('RJ',u'Rio de Janeiro'),
            ('RN',u'Rio Grande do Norte'),
            ('RO',u'Rondônia'),
            ('RR',u'Roraima'),
            ('RS',u'Rio Grande do Sul'),
            ('SC',u'Santa Catarina'),
            ('SE',u'Sergipe'),
            ('SP',u'São Paulo'),
            ('TO',u'Tocantins')]

        return uf

# coding=utf-8

from Products.Archetypes import atapi
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import schemata, base

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema

from wres.brfields.content.BrFieldsAndWidgets import *
from wres.brfields.validators import *

from zope.i18nmessageid import MessageFactory, Message

_ = MessageFactory("cmfuemr")

#===============================================================================
# Definicao de DisplayLists
#===============================================================================
TYPE = DisplayList((
    ('medicare',_('Medicare')),
    ('blueCS',_('Blue Cross/Blue Shield')),
    ('tricare',_('Tricare')),
    ('group',_('Group')),
    ('medicaid',_('Medicaid')),
    ('FECA',_('FECA')),
    ('champVA',_('ChampVA')),
    ('other',_('Other')),
    ))

MAIN = Schema((
        StringField('name',
            schemata='main',
            required=1,
            widget=StringWidget(label=_('Name'),
            )
        ),
        BrPhoneField('phoneNumber',
            schemata='main',
            required=1,
            #validators='isBrTelefone',
            widget=BrPhoneWidget(label=_('Phone'),
                                     description='You must enter only numbers',
                                     description_msgid='help_you_must_enter_only_numbers',
                                     i18n_domain='cmfuemr',
            ),
        ),

        BrPhoneField('faxNumber',
            schemata='main',
            #validators='isBrTelefone',
            widget=BrPhoneWidget(label=_('Fax'),
                                     description='You must enter only numbers',
                                     description_msgid='help_you_must_enter_only_numbers',
                                     i18n_domain='cmfuemr',
            ),
        ),

        StringField('email',
            schemata='main',
            validators='isEmail',
            widget=StringWidget(label=_('Email'),
            ),
        ),

        StringField('webPage',
            schemata='main',
            validators='isURL',
            widget=StringWidget(label=_('Web Site'),
            ),
        ),
        ))
set_schemata_properties(MAIN, schemata='Principal')

NOTES = Schema((
        TextField('notas',
            schemata='notas',
            widget=TextAreaWidget(label=_('Notes'),
            ),
        ),
))
set_schemata_properties(NOTES, schemata='Notas')

baseSchema = finalizeSchema(schemata.ATContentTypeSchema.copy())

InsuranceSchema = baseSchema + MAIN + NOTES

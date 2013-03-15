#coding=utf-8

"""Definition of the Template content type
"""

from zope.interface import implements

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import ITemplate
from wres.archetypes.config import PROJECTNAME
from wres.policy.utils.roles import DOCTOR_ROLE, MANAGER_ROLE
from wres.policy.utils.utils import set_schemata_properties, finalizeSchema

MAIN = Schema((

#    StringField('text',
#        widget=TextAreaWidget(
#            label='Corpo',
#            rows='10',
#        ),
#    ),

    TextField('template_body',
		required=False,
		searchable=False,
		primary=True,
		storage = AnnotationStorage(migrate=True),
		validators = ('isTidyHtmlWithCleanup',),
		#validators = ('isTidyHtml',),
		default_output_type = 'text/x-html-safe',
		widget = RichWidget(
		        description = '',
		        label = 'Corpo do Modelo',
		        rows = 30,
		        allow_file_upload = False,
		),
    ),    

))
set_schemata_properties(MAIN, schemata='default')

baseSchema = schemata.finalizeATCTSchema(schemata.ATContentTypeSchema.copy(), moveDiscussion=False)
baseSchema = finalizeSchema(baseSchema, non_exclude_schematas=['default',])
TemplateSchema = baseSchema + MAIN


class Template(base.ATCTContent):
    """A medical template."""
    implements(ITemplate)

    meta_type = "Template"
    schema = TemplateSchema

    def manage_afterAdd(self, item=None, container=None):
		self.manage_permission('View management screens', [DOCTOR_ROLE, MANAGER_ROLE], acquire=False)

registerType(Template, PROJECTNAME)

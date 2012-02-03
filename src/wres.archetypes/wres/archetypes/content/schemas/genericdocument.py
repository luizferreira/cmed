# coding=utf-8

from zope.i18nmessageid import MessageFactory, Message

from Products.Archetypes.atapi import *

from wres.archetypes.content.medicaldocument import MedicalDocumentSchema
from wres.policy.utils.utils import set_schemata_properties

_ = MessageFactory("cmfuemr")

DOC_BODY = Schema((
    TextField('gdocument_body',
		required=False,
		searchable=False,
		primary=True,
		storage = AnnotationStorage(migrate=True),
		validators = ('isTidyHtmlWithCleanup',),
		#validators = ('isTidyHtml',),
		default_output_type = 'text/x-html-safe',
		widget = RichWidget(
		        description = '',
		        label = _(u'label_generic_document_body_text', default=u'Document Body'),
		        rows = 30,
		        allow_file_upload = False,
	            macro_edit='generic_richtext_edit_macro',
	            helper_js=('generic_richtext_edit.js', ),		        
	            helper_css=('generic_richtext_edit.css', 'cmed.css'),
		),
    ),
))

set_schemata_properties(DOC_BODY, schemata='Corpo do Documento')

GenericDocumentSchema = MedicalDocumentSchema + DOC_BODY
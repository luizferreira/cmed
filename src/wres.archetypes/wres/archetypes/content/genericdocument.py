# coding=utf-8

"""Definition of the GenericDocument content type
"""

from zope.interface import implements

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

from wres.archetypes.interfaces import IGenericDocument
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.medicaldocument import MedicalDocument
from wres.archetypes.content.schemas.genericdocument import GenericDocumentSchema
from wres.policy.utils.utils import set_schemata_properties

MAIN = Schema((
    StringField('document_type',
		required=True,
		# default = 'Documento sem tipo',
        vocabulary = "getTypesOfDocument",
        widget = SelectionWidget(
                label = 'Tipo do Documento',
                macro_edit='generic_selection_edit_macro',
                helper_js=('generic_selection_edit.js', ),             
                # helper_css=('generic_richtext_edit.css', 'cmed.css'),
        ),
    ),
))

set_schemata_properties(MAIN, schemata='Principal')

class GenericDocument(MedicalDocument):
    """Generic medical document."""
    implements(IGenericDocument)

    meta_type = "GenericDocument"
    schema = MAIN + GenericDocumentSchema

    def at_post_create_script(self):
        document_type = self.getDocument_type()
        self.setTitle(document_type)
        dl = self.getTypesOfDocument()
        if document_type not in dl:
            portal = getSite()
            vt = getToolByName(portal, 'vocabulary_tool')        
            vt.add2vocabulary('document_types', document_type, 1)
        # self.setTitle(dl.getValue(self.getDocument_type()))
        
    def generic_document_edit_title(self):
        # return self.getDate().strftime('%d/%m/%y %H:%M') + ' - ' + self.Title()
        return self.getDate().strftime('%d/%m/%y') + ' - ' + self.Title()

    def getTypesOfDocument(self):
        dl = DisplayList()
        dl.add('', 'Selecione')
        portal = getSite()
        vt = getToolByName(portal, 'vocabulary_tool')
        vocab_list = vt.get_vocabulary('document_types', 2)
        for vocab in vocab_list:
            # dl_entry = (vocab, vocab)
            dl.add(vocab, vocab)
        dl.add('outro', 'Outro')
        return dl

registerType(GenericDocument, PROJECTNAME)

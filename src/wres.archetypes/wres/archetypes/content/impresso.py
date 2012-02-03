#coding=utf-8

"""Definition of the Impresso content type
"""

from zope.interface import implements

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from wres.archetypes.interfaces import IImpresso
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.medicaldocument import MedicalDocument
from wres.archetypes.content.schemas.genericdocument import GenericDocumentSchema
from wres.policy.utils.utils import set_schemata_properties

TYPE_OF_DOCUMENT = DisplayList((
    ('', 'Selecione'),
    ('atestado', 'Atestado'),
    ('laudo', 'Laudo'),
    ('licenca', 'Licença'),
))

MAIN = Schema((
    StringField('document_type',
        required=True,
        # default = 'Documento sem tipo',
        vocabulary = TYPE_OF_DOCUMENT,
        widget = SelectionWidget(
                label = 'Tipo do Documento'
                # macro_edit='generic_richtext_edit_macro',
                # helper_js=('generic_richtext_edit.js', ),             
                # helper_css=('generic_richtext_edit.css', 'cmed.css'),
        ),
    ),
))

set_schemata_properties(MAIN, schemata='Principal')

ImpressoSchema = MAIN + GenericDocumentSchema

class Impresso(MedicalDocument):
    """Tipo de documento para ser usado como atestado, laudo ou licenca."""
    implements(IImpresso)

    meta_type = "Impresso"
    schema = ImpressoSchema

    def at_post_create_script(self):
        self.setTitle(TYPE_OF_DOCUMENT.getValue(self.getDocument_type()))
        
    def generic_document_edit_title(self):
        # return self.Title() + ' - ' + self.getDate().strftime('%d/%m/%y %H:%M')
        return self.getDate().strftime('%d/%m/%y') + ' - ' + self.Title()

registerType(Impresso, PROJECTNAME)

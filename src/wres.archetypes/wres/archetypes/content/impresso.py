#coding=utf-8

"""Definition of the Impresso content type
"""

from zope.interface import implements

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

from wres.archetypes.interfaces import IImpresso
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.medicaldocument import MedicalDocument
from wres.archetypes.content.schemas.genericdocument import GenericDocumentSchema
from wres.policy.utils.utils import set_schemata_properties

MAIN = Schema((
    StringField('document_type',
        required=True,
        vocabulary = "getTypesOfImpresso",
        widget = SelectionWidget(
                label = 'Tipo do Documento',
                macro_edit='generic_selection_edit_macro',
                helper_js=('generic_selection_edit.js', ),            
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
        '''
        Configura o titulo do impresso e verifica se o usuario entrou com 
        um valor no campo de tipo de impresso que ainda nao esta presente
        no vocabulario 'impresso_types'. Caso nao esteja presente, adiciona.
        '''
        document_type = self.getDocument_type()
        self.setTitle(document_type)
        dl = self.getTypesOfImpresso()
        if document_type not in dl:
            portal = getSite()
            vt = getToolByName(portal, 'vocabulary_tool')        
            vt.add2vocabulary('impresso_types', document_type, 1)
        
    def generic_document_edit_title(self):
        return self.getDate().strftime('%d/%m/%y') + ' - ' + self.Title()

    def getTypesOfImpresso(self):
        ''' 
        Monta a displaylist do selectionWidget a partir do vocabulario
        impresso_types dentro da ferramenta vocabulary_tool 
        '''
        dl = DisplayList()
        dl.add('', 'Selecione')
        portal = getSite()
        vt = getToolByName(portal, 'vocabulary_tool')
        vocab_list = vt.get_vocabulary('impresso_types', 2)
        for vocab in vocab_list:
            dl.add(vocab, vocab)
        dl.add('outro', 'Outro')
        return dl

registerType(Impresso, PROJECTNAME)

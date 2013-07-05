# coding=utf-8

"""Definition of the DocumentFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IDocumentFolder
from wres.archetypes.config import PROJECTNAME

DocumentFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

schemata.finalizeATCTSchema(
    DocumentFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class DocumentFolder(folder.ATFolder):
    """Folder of Medical Documents"""
    implements(IDocumentFolder)

    meta_type = "DocumentFolder"
    schema = DocumentFolderSchema

    def listDocuments(self):
        """
        Retorna os documentos. Usado para alimentar o documents_folder_view, tanto
        da pasta de Impressos e Consultas.
        """

        # se for a pasta de impressos o meta_type será Impresso, se for a pasta
        # de Consultas, será GenericDocument
        allowed_types = self.allowedContentTypes()
        if len(allowed_types) > 1:
            raise Exception("This folder must have only one allowed type!")
        meta_type = allowed_types[0].getId()

        # restringe a apenas documentos deste paciente.
        path = '/'.join(self.getPhysicalPath())

        # pesquisa no catalog
        pc = getToolByName(self, 'portal_catalog')
        brains = pc.searchResults({'portal_type': meta_type, 'path': path, 'sort_on': 'created', 'sort_order': 'ascending'})

        return [br.getObject() for br in brains]


atapi.registerType(DocumentFolder, PROJECTNAME)

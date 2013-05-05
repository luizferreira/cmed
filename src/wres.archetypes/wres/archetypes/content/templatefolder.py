#coding=utf-8

"""Definition of the TemplateFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import ITemplateFolder
from wres.archetypes.config import PROJECTNAME

TemplateFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

schemata.finalizeATCTSchema(
    TemplateFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class TemplateFolder(folder.ATFolder):
    """A folder for medical templates."""
    implements(ITemplateFolder)

    meta_type = "TemplateFolder"
    schema = TemplateFolderSchema

    def getDocumentTemplates(self):
        """
        Search catalog for Templates. Used by the TemplateFolder view
        (template_folder_view.pt)
        """
        catalog = getToolByName(self,"portal_catalog")
        path = '/'.join(self.getPhysicalPath())
        query = {'portal_type': 'Template', 'path': path, 'sort_on': 'sortable_title'}
        results = catalog.searchResults(query)
        docs = []
        for brain in results:
            # the getObject here is only acceptable since the view that uses
            # this code is not linked in the system (only by URL).
            docs.append(brain.getObject())
        return docs

atapi.registerType(TemplateFolder, PROJECTNAME)

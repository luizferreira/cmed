"""Definition of the UploadChartFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IUploadChartFolder
from wres.archetypes.config import PROJECTNAME
from wres.policy.utils.roles import DOCTOR_ROLE, MANAGER_ROLE

UploadChartFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(
    UploadChartFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class UploadChartFolder(folder.ATFolder):
    """Folder to upload files in chart."""
    implements(IUploadChartFolder)

    meta_type = "UploadChartFolder"
    schema = UploadChartFolderSchema

    def getUploadData(self):
        """
        Provide data for uploaded_view.pt
        """

        pc = getToolByName(self, 'portal_catalog')
        imagens = []
        other_files = []

        def getPatientId(self):
            if self.meta_type == 'Patient':
                return self.getId()
            else:
                return getPatientId(self.aq_inner.aq_parent)

        def getFilesAndImages(self):
            #Get Imagens
            portal = self.getPortal()
            patientPath = '/' + portal.getId() + '/Patients/' + getPatientId(self) + '/'
            brains = pc.search({'portal_type': 'Image', 'path': patientPath})
            index = 0
            for brain in brains:
                parts = brain.getPath().split("/")
                parts.pop(0)
                parts.pop(0)
                path = '/'.join(parts)
                date = brain.created.strftime("%y/%m/%d")
                name = parts[-1].split('.')[0]
                imagens.append((path, date, name, index))
                index = index + 1

            #Get Other Files
            brains += pc.search({'portal_type': 'File', 'path': patientPath})
            for brain in brains:
                filePath = brain.getURL()
                name = brain.Title
                icon = brain.getIcon
                file = (filePath, name, icon, brain.UID)
                other_files.append(file)
            return [imagens, other_files]

        return getFilesAndImages(self)

    def deleteExternalFile(self):
        """
        Deleta um arquivo externo
        """

        pc = getToolByName(self, "portal_catalog")

        for uid in self.REQUEST.form.iterkeys():
            brain_list = pc.searchResults({'UID': uid})
            brain = brain_list[0]
            self.manage_delObjects(brain.id)

        return self.REQUEST.response.redirect("/".join(self.getPhysicalPath()))

    def manage_afterAdd(self, item=None, container=None):
        self.manage_permission('Delete objects', [DOCTOR_ROLE, MANAGER_ROLE], acquire=False)

atapi.registerType(UploadChartFolder, PROJECTNAME)

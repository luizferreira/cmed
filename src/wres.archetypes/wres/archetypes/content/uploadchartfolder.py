## coding=utf-8

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
        cp = self.getPhysicalPath()
        patient_path = '/'.join(cp[:cp.index('Patients')+2])

        # build list of images to be previewed
        images = []
        brains = pc.search({'portal_type': 'Image', 'path': patient_path})
        for br in brains:
            parts = br.getPath().split("/")[2:] # preciso do path começando no 'Patients'
            images.append( 
                {
                    'path': '/'.join(parts),
                }
            )

        # build list of all files (including images)
        files = []
        # increment list of brains using '+='
        brains += pc.search({'portal_type': 'File', 'path': patient_path})
        for br in brains:
            icon = br.getIcon
            if not icon:
                icon = 'f.png'
            files.append(
                {
                    'path': br.getURL(),
                    'name': br.Title,
                    'icon': icon,
                    'uid': br.UID,
                    'date': br.created.strftime("%d/%m/%Y"),
                }
            )

        return {
            'all_files': files,
            'preview_images': images,
        }

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

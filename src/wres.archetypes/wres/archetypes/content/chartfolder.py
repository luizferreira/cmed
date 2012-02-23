"""Definition of the ChartFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFPlone.utils import _createObjectByType

from ComputedAttribute import ComputedAttribute

from wres.policy.utils.roles import MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, TRANSCRIPTIONIST_ROLE
# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IChartFolder
from wres.archetypes.config import PROJECTNAME
#from wres.archetypes.content.documentfolder import DocumentFolder

ChartFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(
    ChartFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class ChartFolder(folder.ATFolder):
    """Chart Folder of Patients"""
    implements(IChartFolder)

    meta_type = "ChartFolder"
    schema = ChartFolderSchema
    
#    def create_hidden_object(self, obj_id, title, type='UemrFolder',
#                             layout='documents_view', allowed_types=['Doc']):
#        obj = getattr(self, obj_id, None)
#        if obj is None:
#            _createObjectByType(type, self, obj_id, title=title)
#            obj = getattr(self, obj_id)
#        if layout != obj.getLayout():
#            obj.setLayout(layout)
#        if tuple(allowed_types) != tuple(obj.getLocallyAllowedTypes()):
#            from Products.CMFUEMR.compatibility import set_field_value
#            set_field_value(obj, 'enableConstrainMixin', True)
#            obj.setLocallyAllowedTypes(allowed_types)
#        if obj.title != title:
#            obj.title = title
#        return obj
    
    def create_hidden_object(self, obj_id, title, type):
        obj = getattr(self, obj_id, None)
        if obj is None:
            _createObjectByType(type, self, obj_id, title=title)
            obj = getattr(self, obj_id)
        return obj 
    
#    def at_post_create_script(self):
#        self.create_hidden_object('upload', 'Upload', 'Folder')
        
    def manage_afterAdd(self, item=None, container=None):
        """ Essa funcao e' chamada logo apos a adicao (addChartFolder) de um archetype """ 
        self.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
        self.create_hidden_object('documents', 'Consultas', 'DocumentFolder')
        self.documents.title = 'Consultas'
        self.documents.setLocallyAllowedTypes('GenericDocument')
        self.documents.setImmediatelyAddableTypes('GenericDocument')
        self.documents.setConstrainTypesMode(1)
        self.documents.reindexObject()

        self.create_hidden_object('impressos', 'Impressos', 'DocumentFolder')
        self.impressos.title = 'Impressos'
        self.impressos.setLocallyAllowedTypes('Impresso')
        self.impressos.setImmediatelyAddableTypes('Impresso')
        self.impressos.setConstrainTypesMode(1)
        self.impressos.reindexObject()        
            
        self.create_hidden_object('exams', 'Exames', 'UploadChartFolder')
        self.exams.title = 'Exames'               
                   
        self.create_hidden_object('upload', 'Documentos Externos', 'UploadChartFolder')
        self.upload.title = 'Documentos Externos'


atapi.registerType(ChartFolder, PROJECTNAME)

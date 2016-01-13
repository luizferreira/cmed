"""Definition of the PatientFolder content type
"""

from zope.interface import implements

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IPatientFolder
from wres.archetypes.config import PROJECTNAME

PatientFolderSchema = folder.ATFolderSchema.copy() + Schema((

    # -*- Your Archetypes field definitions here ... -*-
     IntegerField('lastChartSystemID',
        index="FieldIndex:schema",
        validators = ('isInt',),
        widget=IntegerWidget(
            visible={'edit':'invisible'},
            description='Last System Chart Number',
            i18n_domain='cmfuemr',
        ),
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(
    PatientFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class PatientFolder(folder.ATFolder):
    """Patients' folder"""
    implements(IPatientFolder)

    meta_type = "PatientFolder"
    schema = PatientFolderSchema

    def at_post_create_script(self):
        #Start LastChartSystemID couter
        self.setLastChartSystemID(0)

    def patient_folder_view_data(self):
        """
        Alimenta patient_folder_view.pt
        """

        data = []

        member = self.portal_membership.getAuthenticatedMember()

        brains = self.portal_catalog.search({'portal_type': 'Patient'}, sort_index='sortable_title')

        # usamos base_url para o sistema nao adicionar o id do site na URL quando em producao
        base_url = '/'.join(self.getPhysicalPath()) + '/'

        for br in brains:

            if br.review_state == 'inactive':
                continue

            patient = {
                'id': '',
                'name': '',
                'phone': '',
                'birth': '',
                'url': '',
                'chartUrl': '',
            }

            patient['id'] = br.getId
            patient['name'] = br.Title
            patient['url'] = base_url + br.getId
            if br.genericColumn1:
                patient['birth'] = br.genericColumn1.strftime('%d/%m/%Y')
            if br.genericColumn2:
                patient['phone'] = '(' + br.genericColumn2[:2] + ')' +  br.genericColumn2[2:6]+ '-' +br.genericColumn2[6:]
            if 'Secretary' in member.getRoles():
                patient['chartUrl'] = br.getPath()
            else:
                patient['chartUrl'] = br.getPath() + '/initChart'
            data.append(patient)

        return data


registerType(PatientFolder, PROJECTNAME)

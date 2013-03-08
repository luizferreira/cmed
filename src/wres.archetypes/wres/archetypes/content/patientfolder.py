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

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

registerType(PatientFolder, PROJECTNAME)

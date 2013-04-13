"""Definition of the VisitFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from Products.CMFCore.utils import getToolByName
  
  
from wres.archetypes.interfaces import IVisitFolder
from wres.archetypes.config import PROJECTNAME
from zope.app.component.hooks import getSite
from wres.archetypes.content.wresuser import create_id

import json

VisitFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(
    VisitFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class VisitFolder(folder.ATFolder):
    """Folder of visits"""
    implements(IVisitFolder)

    meta_type = "VisitFolder"
    schema = VisitFolderSchema

    def createNewPatient(self):
		type_name = 'Patient'
		location = '/Patients'
		path = self.portal_url.getPortalPath()
		
		place_to_create = self.restrictedTraverse(path + location)

		id = self.generateUniqueId(type_name)

		if place_to_create.portal_factory.getFactoryTypes().has_key(type_name):
		    o = place_to_create.restrictedTraverse('portal_factory/' + type_name + '/' + id)
		else:
		    new_id = place_to_create.invokeFactory(id=id, type_name=type_name)
		    if new_id is None or new_id == '':
		       new_id = id
		    o = getattr(place_to_create, new_id, None)
		return o

    def saveNewDataPatient(self,firstName,lastName,contactPhone):
		# firstName = self.REQUEST.get("firstName")
		# lastName = self.REQUEST.get("lastName")
		# contactPhone = self.REQUEST.get("contactPhone")

		portal = getSite()
		patient = self.createNewPatient()

		patient.setFirstName(firstName)
		patient.setLastName(lastName)
		patient.setContactPhone(contactPhone)

		pr = getToolByName(portal,"portal_registration")
		new_id = create_id(pr,firstName,lastName)
		
		patient = patient.portal_factory.doCreate(patient, new_id)
		patient.processForm()
		return patient


		



    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(VisitFolder, PROJECTNAME)

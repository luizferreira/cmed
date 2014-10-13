## coding=utf-8

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
		"""
		Return patient saved by quick register way.
		"""
		#firstName = self.REQUEST.get("firstName")
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
		return json.dumps({"url": "/".join(patient.getPhysicalPath()),"name": patient.getFullName()})


    # def create_dummy_visits(self):
    #     """
    #     Cria visitas para realização de testes.
    #     """
    #     from random import randint
    #     from DateTime import DateTime

    #     visits_number = 10

    #     patients = self.portal_catalog(portal_type='Patient')

    #     for v in range(visits_number):

    #         oid = str(randint(1, 100000000)) + str(randint(1, 100000000))
    #         new_visit = self.invokeFactory(id=oid, type_name='Visit')
    #         new_visit = self.get(oid)

    #         start_hour = randint(8, 17)
    #         start_minute = randint(1, 59)

    #         today = DateTime()
    #         start_date = DateTime(today.year(), today.month(), today.day(), start_hour, start_minute)
    #         if start_minute < 45:
    #             end_date = DateTime(today.year(), today.month(), today.day(), start_hour, start_minute+15)
    #         else:
    #             end_date = DateTime(today.year(), today.month(), today.day(), start_hour+1, start_minute-45)

    #         new_visit.setStartDate(start_date)
    #         new_visit.setEndDate(end_date)
    #         new_visit.setDuration(15)

    #         patient = patients[randint(0, len(patients)-1)].getObject()
    #         new_visit.setPatient(patient)

    #         new_visit = new_visit.portal_factory.doCreate(new_visit, oid)
    #         new_visit.processForm()

    #         new_visit.reindexObject()

    #     import ipdb; ipdb.set_trace()



    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(VisitFolder, PROJECTNAME)

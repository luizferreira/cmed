#coding=utf-8
import unittest2 as unittest
from wres.archetypes.tests.IntegrationLayer import WRES_ARCHETYPES_INTEGRATION_TESTING
from wres.archetypes.tests.IntegrationLayer import WRES_ARCHETYPES_INTEGRATION_TESTING
from wres.archetypes.content.patient import Patient
from wres.archetypes.content.visit import Visit
from wres.archetypes.tests.utilsPatient import create_patients, getPatientOwnerFromPath
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
import json
from wres.policy.utils.roles import PATIENT_GROUP
from wres.policy.setuphandlers import getOrCreateType

class TestSetup(unittest.TestCase):
    layer = WRES_ARCHETYPES_INTEGRATION_TESTING
   
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.pc = getToolByName(self.portal,"portal_catalog")
        self.pr = getToolByName(self.portal, 'portal_registration')
        
        #Set me as Manager
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        
        #Cria um paciente para ser usado nos testes 
        create_patients(self.portal,self.pr,"joao","silva")        
        
        #Make patient easy to access
        query = self.pc.searchResults({'id':'jsilva'})
        self.patient = query[0].getObject()
        
    def test_SearchableText(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentPatient   Test:SearchableText"
        print "----------------------------------------------"
        #Get requirements
        patient = self.patient
        
        #Test Function
        #I know pdi = jsilva, cpf = 01234567890, fullname = Joao Silva
        result = ['jsilva','01234567890','Joao Silva']
        self.assertTrue(patient.SearchableText(), result)
        print "Done"

    
    def test_getInformation(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentPatient   Test:getInformation"
        print "----------------------------------------------"
        patient = self.patient
        uuid = patient.UID()
        phone = patient.getContactPhone()
        lastVisit = patient.getLastVisitDate()
        j_dump = json.dumps({'getLastDate': lastVisit, 'getContactPhone': phone, 'UID': uuid})
        self.assertTrue(patient.getInformation(), j_dump)
        print "Done"

    def test_getInformation(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentPatient   Test:getInformation"
        print "----------------------------------------------"
        patient = self.patient
        uuid = patient.UID()
        phone = patient.getContactPhone()
        lastVisit = patient.getLastVisitDate()
        j_dump = json.dumps({'getLastDate': lastVisit, 'getContactPhone': phone, 'UID': uuid})
        self.assertTrue(patient.getInformation(), j_dump)
        print "Done"

    def test_getGroup(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentPatient   Test:getGroup"
        print "----------------------------------------------"
        patient = self.patient
        self.assertTrue(PATIENT_GROUP, patient.getGroup())
        print "Done"

    def test_createHiddenKey(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentPatient   Test:createHiddenKey"
        print "----------------------------------------------"
        patient = self.patient
        key = "key"
        self.assertTrue("key_hidden",patient.createHiddenKey(key))
        print "Done"

    def test_existSubObject(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentPatient   Test:existSubObject"
        print "----------------------------------------------"
        patient = self.patient
        key = "atributo"
        hidden_key = "atributo_hidden"
        patient.atributo_hidden = "contentudoqualquer"
        self.assertTrue(patient.existSubObject(key))
        self.assertFalse(patient.existSubObject("schwarzenegger_hidden"))
        print "Done"
    
    def test_createChartFolder(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentPatient   Test:createChartFolder"
        print "----------------------------------------------"
        patient = self.patient
        patient.createChartFolder("ChartFolder_ID123")
        query = self.pc.searchResults({"type":"chartfolder"})
        all_chartfolders = []
        for i in range(len(query)):
                obj = query[i].getObject()
                all_chartfolders.append(obj.id)
        self.assertTrue("documents" in all_chartfolders)
        self.assertTrue("impressos" in all_chartfolders)
        self.assertTrue("exams" in all_chartfolders)
        self.assertTrue("upload" in all_chartfolders)
        print "Done"
        
    def test_createMissingObject(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:createMissingObject"
        print "-------------------------------------------------"
        patient = self.patient
        #Pass First if and fail
        patient.atributo_hidden = "contentudoqualquer"
        self.assertTrue("atributo_hidden" in patient.createMissingObject("atributo"))
        
        #Create new patient without chartfolder yet        
        create_patients(self.portal,self.pr,"carlos","jose")        
        query = self.pc.searchResults({'id':'cjose'})
        new_patient = query[0].getObject()
        
        #Check Cleanness (if chartFolder exists)
        query = self.pc.searchResults({"id":"upload"})
        for i in range(len(query)):
                brain = query[i]
                if "cjose" in brain.getPath():
                        raise NameError("Upload shouldn't exists")
        
        #Check chart
        new_patient.createMissingObject("chartFolder")
        query = self.pc.searchResults({"id":"upload"})
        cjose_upload = False
        for i in range(len(query)):
                brain = query[i]
                if "cjose" in brain.getPath():
                        cjose_upload = True
        self.assertTrue(cjose_upload)
        print "Done"
        
    def test__getSubObject(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:_getSubObject"
        print "-------------------------------------------------"
        patient = self.patient
        chart = patient._getSubObject("chartFolder")
        self.assertTrue("<ChartFolder at" in str(chart))
        
    def test_chartFolder(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:chartFolder"
        print "-------------------------------------------------"
        patient = self.patient
        chart = patient.chartFolder
        self.assertTrue("<ChartFolder at" in str(chart))
    
    def test_getLastVisitDate(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:getLastVisitDate"
        print "-------------------------------------------------"
        patient = self.patient
        
        #Fist test, without lastVisitDate
        self.assertEqual('No visits concluded',patient.getLastVisitDate())
        
        #Test with lastVisitDate
        import datetime
        DATE = datetime.datetime(2009,5,25)
        patient.lastVisitDate = DATE
        self.assertEqual('25/05/2009',patient.getLastVisitDate())
        print "Done"
    
    def test_setLastVisitDate(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:setLastVisitDate"
        print "-------------------------------------------------"
        patient = self.patient
        #Set invalid date type
        try:
            patient.setLastVisitDate("03/07/1961")
        except ValueError as error:
            self.assertEqual('Tipo de data invalida',str(error))
            
        #Set valid date
        import datetime
        DATE = datetime.datetime(2009,4,21)
        patient.setLastVisitDate(DATE)
        self.assertEqual('21/04/2009',patient.getLastVisitDate())
        print "Done"
    
    def test_Title(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:Title"
        print "-------------------------------------------------"
        patient = self.patient

        #Check patient Title when name exists
        self.assertEqual("Joao Silva",patient.Title())
        
        #Check patient Title when name doesn't exists
        patient.firstName = ""
        patient.lastName = ""
        self.assertEqual("Sem Nome",patient.Title())
        print "Done"
    
    def test_lower_title(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:lower_title"
        print "-------------------------------------------------"
        patient = self.patient
        #Check patient Title when name exists
        self.assertEqual("joao silva",patient.lower_title())
        print "Done"
    
    def test_at_post_create_script(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:at_post_create_script"
        print "-------------------------------------------------"
        #This function has been used at the creation time of the patient
        #Here we just look if his ID is registered.
        portal = self.portal
        pm = getToolByName(portal,'portal_membership')
        mb = pm.getMemberById('jsilva')
        self.assertFalse(mb is None)
        print "Done"
        


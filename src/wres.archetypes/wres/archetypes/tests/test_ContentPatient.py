#coding=utf-8
import unittest2 as unittest
from wres.archetypes.tests.IntegrationLayer import WRES_ARCHETYPES_INTEGRATION_TESTING
from wres.archetypes.content.chartdata import Event
from wres.archetypes.tests.utilsPatient import create_patient, create_empty_patient
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
import json
from wres.policy.utils.roles import PATIENT_GROUP

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
        create_patient(self.portal,self.pr,"joao","silva")        
        
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
        create_patient(self.portal,self.pr,"carlos","jose")        
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
        print "Done"
        
    def test_chartFolder(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:chartFolder"
        print "-------------------------------------------------"
        patient = self.patient
        chart = patient.chartFolder
        self.assertTrue("<ChartFolder at" in str(chart))
        print "Done"
    
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
    
    def test_at_post_edit_script(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:at_post_edit_script"
        print "-------------------------------------------------"
        patient = self.patient
        patient.setFirstName('carlos')
        patient.at_post_edit_script()
        self.assertEqual('Carlos',patient.getFirstName())
        print "Done"
    
    def test_at_post_edit_script(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:at_post_edit_script"
        print "-------------------------------------------------"
        patient = self.patient
        patient.setFirstName('carlos')
        patient.at_post_edit_script()
        self.assertEqual('Carlos',patient.getFirstName())
        print "Done"
    
    def test_getFullName(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:getFullName"
        print "-------------------------------------------------"
        patient = self.patient
        self.assertEqual('Joao Silva',patient.getFullName())
        print "Done"
        
    def test_get_home_url(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:get_home_url"
        print "-------------------------------------------------"
        patient = self.patient
        self.assertEqual('/plone/Patients/jsilva',patient.get_home_url())
        print "Done"
    
    def test___create_chart_data(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:__create_chart_data"
        print "-------------------------------------------------"
        #This function is executed when patient's event creation is executed
        #Here it will be just checked if it has been executed
        patient = self.patient
        self.assertTrue(hasattr(patient,"chart_data_hidden"))
        print "Done"
        
    def test_create_event(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:create_event"
        print "-------------------------------------------------"
        patient = self.patient
        #Here we just check if the creation patient event has been called
        chartdata = patient.chart_data
        event_list = dict(chartdata.events).values()
        event_list.sort(cmp=Event._event_cmp)
        event_txt = event_list[0].eprint()
        self.assertEqual('Paciente <a class="" target="_blank" href="/plone/Patients/jsilva"> Joao Silva </a> adicionado.',event_txt)
        print "Done"

    def test_get_events(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:get_events"
        print "-------------------------------------------------"
        patient = self.patient
        size1 = len(patient.get_events())
        
        #To test, I'll add one more event to events, and see if I'll get it
        from DateTime import DateTime 
        patient.create_event(Event.CREATION,DateTime(),patient)
        
        #Check if number of events changed
        size2 = len(patient.get_events())
        self.assertTrue(size1 + 1 == size2)
        
        #Check if the last event is correct
        events = patient.get_events()
        event_txt = events[-1:][0].eprint()
        self.assertEqual('Paciente <a class="" target="_blank" href="/plone/Patients/jsilva"> Joao Silva </a> adicionado.',event_txt)
        print "Done"

    def test_get_chart_data_map(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:get_chart_data_map"
        print "-------------------------------------------------"
        patient = self.patient
        self.assertTrue("{'review_of_systems': <type 'BTrees.OOBTree.OOBTree'>, 'not_signed_allergies': <type 'BTrees.OOBTree.OOBTree'>, 'medications': <type 'BTrees.OOBTree.OOBTree'>, 'prescriptions': <type 'BTrees.OOBTree.OOBTree'>, 'laboratory': <type 'BTrees.OOBTree.OOBTree'>, 'allergies': <type 'BTrees.OOBTree.OOBTree'>, 'problems': <type 'BTrees.OOBTree.OOBTree'>, 'events': <type 'BTrees.OOBTree.OOBTree'>}"
        == str(patient.get_chart_data_map()))
        print "Done"
    
    def test_chart_data_summary(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:chart_data_summary"
        print "-------------------------------------------------"
        patient = self.patient
        #Is difficult to test the correctness of this function.
        #Here will be just checked the returned value of an empty chart folder.
        #Created new clean patient       
        create_empty_patient(self.portal,self.pr,"carlos","jose")        
        query = self.pc.searchResults({'id':'cjose'})
        new_patient = query[0].getObject()
        self.assertTrue("{'review_of_systems': <type 'BTrees.OOBTree.OOBTree'>, 'not_signed_allergies': <type 'BTrees.OOBTree.OOBTree'>, 'medications': <type 'BTrees.OOBTree.OOBTree'>, 'prescriptions': <type 'BTrees.OOBTree.OOBTree'>, 'laboratory': <type 'BTrees.OOBTree.OOBTree'>, 'allergies': <type 'BTrees.OOBTree.OOBTree'>, 'problems': <type 'BTrees.OOBTree.OOBTree'>, 'events': <type 'BTrees.OOBTree.OOBTree'>}"
        == str(new_patient.get_chart_data_map()))
        print "Done"
    
    def test_import_chartdata(self):
        print "\n"
        print "-------------------------------------------------"
        print "Modulo: ContentPatient   Test:import_chartdata"
        print "-------------------------------------------------"
        patient = self.patient
        #The test will import the chart folder from patient to a clean patient
        create_empty_patient(self.portal,self.pr,"carlos","jose")        
        query = self.pc.searchResults({'id':'cjose'})
        new_patient = query[0].getObject()
        new_patient.import_chartdata(patient.chart_data_summary())
        self.assertEqual(new_patient.chart_data_summary(),patient.chart_data_summary())
        print "Done"
        

        

    

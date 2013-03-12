#coding=utf-8
import unittest2 as unittest
from wres.archetypes.tests.IntegrationLayer import WRES_ARCHETYPES_INTEGRATION_TESTING
from wres.policy.utils.utils import createVisitObject
from wres.archetypes.tests.utilsDoctor import create_doctor
from wres.archetypes.tests.utilsPatient import create_patient
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from DateTime import DateTime

class TestSetup(unittest.TestCase):
    layer = WRES_ARCHETYPES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.pc = getToolByName(self.portal,"portal_catalog")
        self.pr = getToolByName(self.portal, 'portal_registration')
        
        #Set me as Manager
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        
        #Cria um médico e paciente para serem usados nos testes 
        create_doctor(self.portal,self.pr,"Dr. Victor","Frankenstein")   
        create_patient(self.portal,self.pr,"Anderson","Silva")        
             
        #Make patient easy to access
        query = self.pc.searchResults({'id':'dfrankenstein'})
        self.doctor = query[0].getObject()

        #Make patient easy to access
        query = self.pc.searchResults({'id':'asilva'})
        self.patient = query[0].getObject()
        self.patient.setSocialSecurity('12131415')

        #Cria consulta
        visit = createVisitObject(self.portal.Appointments.dfrankenstein, 'id_visit_1')
        visit.setPatient(self.patient)
        visit.setDuration(30)
        visit.setContactPhone('31 9765 0616')
        visit.reindexObject()
        self.visit = visit
        
    def test_SimpleGets(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentVisit   Test:getDoctor"
        print "Modulo: ContentVisit   Test:getProviderId"
        print "Modulo: ContentVisit   Test:getTagDefault"
        print "Modulo: ContentVisit   Test:getTypesOfVisit"
        print "Modulo: ContentVisit   Test:getVisitReason"
        print "----------------------------------------------"
        #Get requirements
        visit = self.visit
        self.assertEqual(visit.getDoctor(), self.doctor)
        self.assertEqual(visit.getProviderId(), 'dfrankenstein')
        self.assertTrue('1a Consulta' in visit.getTypesOfVisit())
        self.assertTrue('Acompanhamento' in visit.getVisitReason())
        print "Done"

    # def test_at_post_create_script(self):
    #     print "\n"
    #     print "----------------------------------------------"
    #     print "Modulo: ContentVisit   Test:at_post_create_script"
    #     print "----------------------------------------------"
    #     #Get requirements
    #     visit = self.visit
    #     import pdb; pdb.set_trace()
    #     visit.at_post_create_script() #erro ao utilizar o doActionFor do Workflow
    #     self.assertEqual(visit.getDoctor, self.doctor)
    #     self.assertEqual(visit.getProviderId(), 'dfrankenstein')
    #     print "Done"

    def test_addInsurance(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentVisit  Test:addInsurance"
        print "Modulo: ContentVisit  Test:getInsuranceNames"
        print "----------------------------------------------"
        #Get requirements
        visit = self.visit
        visit.setInsurance('Golden Cross')
        visit.addInsurance()
        insurances = visit.getInsurancesNames()
        self.assertEqual(visit.getInsurance(), 'Golden Cross')
        self.assertTrue('Golden Cross' in insurances)
        print "Done"

    def test_FewGetsMore(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentVisit   Test:getStartDate"
        print "Modulo: ContentVisit   Test:getSocialSecurity"
        print "Modulo: ContentVisit   Test:popup_search_script"
        print "Modulo: ContentVisit   Test:getPatientInfo"
        print "----------------------------------------------"
        #Get requirements
        visit = self.visit
        visit.setStartDate(DateTime('10/10/2012'))
        self.assertEqual(visit.getStartDate(), DateTime('10/10/2012')) #StartDate
        self.assertEqual(visit.getSocialSecurity(), '12131415') #SocialSecurity
        self.assertEqual(visit.popup_search_script().getId(), 'popup_search_script') #popup_search_script
        patient = visit.getPatientInfo()
        self.assertEqual(patient['Title'], 'Joao Silva') #getPatientInfo
        self.assertEqual(patient['absolute_url'], 'http://nohost/plone/Patients/asilva') #getPatientInfo
        print "Done"
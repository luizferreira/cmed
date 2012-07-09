#coding=utf-8
import unittest2 as unittest
from wres.archetypes.tests.IntegrationLayer import WRES_ARCHETYPES_INTEGRATION_TESTING
from wres.archetypes.tests.IntegrationLayer import WRES_ARCHETYPES_INTEGRATION_TESTING
from wres.archetypes.content.patient import Patient
from wres.archetypes.tests.utilsPatient import create_patients
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

class TestSetup(unittest.TestCase):
    layer = WRES_ARCHETYPES_INTEGRATION_TESTING
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.pc = getToolByName(self.portal,"portal_catalog")
        
        #Set me as Manager
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        
        #Cria um paciente para ser usado nos testes 
        pr = getToolByName(self.portal, 'portal_registration')
        create_patients(self.portal,pr,"joao","silva")        
        
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
        self.failUnlessEqual(patient.SearchableText(), result)


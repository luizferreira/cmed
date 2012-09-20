#coding=utf-8
import unittest2 as unittest
from wres.archetypes.tests.IntegrationLayer import WRES_ARCHETYPES_INTEGRATION_TESTING
from wres.archetypes.tests.utilsSecretary import create_secretary
from wres.policy.utils.roles import SECRETARY_GROUP
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class TestSetup(unittest.TestCase):
    layer = WRES_ARCHETYPES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.pc = getToolByName(self.portal,"portal_catalog")
        self.pr = getToolByName(self.portal, 'portal_registration')
        
        #Set me as Manager
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        
        #Cria uma sec para ser usado nos testes 
        create_secretary(self.portal,self.pr,"Anna","Kournikova")        
        
        #Make patient easy to access
        query = self.pc.searchResults({'id':'akournikova'})
        self.sec = query[0].getObject()

    def test_getGroup(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentSecretary   Test:getGroup"
        print "----------------------------------------------"
        #Get requirements
        sec = self.sec
        self.assertEqual(sec.getGroup(), SECRETARY_GROUP)
        print "Done"

    def test_get_home_url(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentSecretary   Test:get_home_url"
        print "----------------------------------------------"
        #Get requirements
        sec = self.sec
        parts = sec.get_home_url().split('/')
        self.assertTrue('Appointments' in parts)
        self.assertTrue('sec_desk' in parts)
        print "Done"

    
    def test_Title(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentSecretary   Test:Title"
        print "----------------------------------------------"
        #Get requirements
        sec = self.sec
        self.assertEqual(sec.Title(), sec.getFirstName()+' '+sec.getLastName())
        print "Done"

    def test_at_post_create_script(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentSecretary   Test:at_post_create_script"
        print "----------------------------------------------"
        #Get requirements
        sec = self.sec
        sec.setFirstName('ANNA')
        sec.at_post_create_script()
        pm = getToolByName(self.portal, 'portal_membership')
        self.assertTrue(pm.getMemberById(sec.getId()))
        self.assertEqual(sec.Title(), 'Anna Kournikova')
        print "Done"

    def test_at_post_edit_script(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentSecretary   Test:at_post_edit_script"
        print "----------------------------------------------"
        #Get requirements
        sec = self.sec
        sec.setFirstName('ANNA')
        sec.at_post_create_script()
        pm = getToolByName(self.portal, 'portal_membership')
        self.assertTrue(pm.getMemberById(sec.getId()))
        self.assertEqual(sec.Title(), 'Anna Kournikova')
        print "Done"
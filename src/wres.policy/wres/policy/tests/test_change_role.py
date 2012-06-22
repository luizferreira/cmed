## coding=utf-8

import datetime
from DateTime.DateTime import *
import unittest2 as unittest
from plone.testing.z2 import Browser
from plone.testing import z2
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD, SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.app.testing import setRoles
from wres.policy.testing import WRES_POLICY_FUNCTIONAL_TESTING
from wres.policy.test_browser_utils import *

from Testing.ZopeTestCase.utils import  startZServer
from Products.CMFCore.utils import getToolByName
from wres.policy.test_browser_utils import *
import random


DOCTOR_TEST_USER_ID = 'doctor_test_user_id'
DOCTOR_TEST_USER_NAME = 'doctor_test_user_name'
SECRETARY_TEST_USER_ID = 'secretary_test_user_id'
SECRETARY_TEST_USER_NAME = 'secretary_test_user_name'
PATIENT_TEST_USER_ID = 'patient_test_user_id'
PATIENT_TEST_USER_NAME = 'patient_test_user_name'

MANAGER_ROLES = ['Manager']
DOCTOR_ROLES = ['Doctor', 'Member', 'Contributor', 'Reviewer']
SECRETARY_ROLES = ['Secretary', 'Member', 'Contributor']
PATIENT_ROLES = ['Patient', 'Member']

PW = "senha1"

class TestSetup(unittest.TestCase):
    
    layer = WRES_POLICY_FUNCTIONAL_TESTING
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.browser = Browser(self.app)
    
    def logout(self):
        browser = self.browser
        portal = self.portal
        
        browser.open(portal.absolute_url() + "/logout")
        
    def test_log_as_members(self):
        print "\nTeste logar com diversos membros"
        browser = self.browser
        portal = self.portal
        
        create_members_by_debug_init(self)
        
        login_as_admin(self)
        browser.open(portal.absolute_url() + "/check_actual_roles")
        self.failUnless("['admin'," in browser.contents)
        logout(self)
        
        login_as_secretary(self)
        browser.open(portal.absolute_url() + "/check_actual_roles")
        self.failUnless("[u'steste'," in browser.contents)
        logout(self)
        
        login_as_doctor(self)
        browser.open(portal.absolute_url() + "/check_actual_roles")
        self.failUnless("[u'dteste'," in browser.contents)
        logout(self)
        print "\nTeste logar com diversos usuários passou"
        

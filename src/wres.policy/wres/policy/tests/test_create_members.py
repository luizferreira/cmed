## coding=utf-8

import datetime
import unittest2 as unittest
from plone.testing.z2 import Browser
from plone.testing import z2
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD, SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.app.testing import setRoles
from wres.policy.testing import WRES_POLICY_FUNCTIONAL_TESTING

from Testing.ZopeTestCase.utils import  startZServer

from Products.CMFCore.utils import getToolByName

# import unittest2 as unittest
# from wres.policy.testing import WRES_POLICY_FUNCTIONAL_TESTING
# from Products.CMFCore.utils import getToolByName

# from Products.Five.testbrowser import Browser
# from Products.PloneTestCase import PloneTestCase as ptc

# from Products.PloneTestCase.setup import portal_owner, default_password

# from plone.app.testing import setRoles

# from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD

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

# TEST_USER_ID = 'admin'

#TODO: Lembrar de trocar os assertsEquals quando conseguir trocar o role do usuário. Por enquanto o setRoles não funciona. Matheus

def create_uemr_user(portal, user_id, group, email='', fullname=''):
    pr = getToolByName(portal, 'portal_registration')
    pm = getToolByName(portal, 'portal_membership')
    uf = getToolByName(portal, 'acl_users')
    if email == '':
        email = 'sem@email.com'
    pr.addMember(
        user_id, TEST_USER_PASSWORD,
        properties={
            'username': user_id,
            'email': email,
            'fullname': fullname,
        },
    )
    uf.userSetGroups(user_id, [group])
    pm.createMemberArea(member_id=user_id) 
    
    

class TestSetup(unittest.TestCase):
    
    layer = WRES_POLICY_FUNCTIONAL_TESTING
    
    # def afterSetUp(self):
    #     """
    #     Show errors in console by monkey patching site error_log service
    #     """
    #     ptc.FunctionalTestCase.afterSetUp(self)

    #     self.browser = Browser()
    #     self.browser.handleErrors = False # Don't get HTTP 500 pages


    #     self.portal.error_log._ignored_exceptions = ()

    #     def raising(self, info):
    #         import traceback
    #         traceback.print_tb(info[2])
    #         print info[1]

    #     from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
    #     SiteErrorLog.raising = raising


    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.browser = Browser(self.app)

        z2.logout()
        z2.login(self.app['acl_users'], SITE_OWNER_NAME)

        # self.addDoctor()

        # Log out again
        z2.logout()


    #     self.afterSetUp()

    # def afterSetUp(self):
    #     """
    #     Show errors in console by monkey patching site error_log service
    #     """
    #     self.browser.handleErrors = False
        
    #     self.portal.error_log._ignored_exceptions = ()        

    #     def raising(self, info):
    #         import traceback
    #         traceback.print_tb(info[2])
    #         print info[1]

    #     from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
    #     SiteErrorLog.raising = raising

    #     import ipdb; ipdb.set_trace()

    def login_as_admin(self):
        """ Perform through-the-web login.

        Simulate going to the login form and logging in.

        We use username and password provided by PloneTestCase.

        This sets session cookie for testbrowser.
        """

        # Go admin
        portal = self.portal
        browser = self.browser
        # setRoles(portal, TEST_USER_ID, ('Manager', 'Doctor'))
        # browser = self.browser
        browser.open(portal.absolute_url() + "/login_form")
        browser.getControl(name='__ac_name').value = "admin"
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()
        browser.open(portal.absolute_url() + '/view')
    
    def create_doctor(self):
        # vai pra pagina inicial e depois entra na pasta Patients
        portal = self.portal
        browser = self.browser
        browser.open(portal.absolute_url() + '/view')

        # entra na pasta Doctors e vai pra pagina de adicao de doutor
        browser.getLink("Médicos").click()
        browser.open(browser.url + "/createObject?type_name=Doctor")

        # preenche os dados do medico
        browser.getControl(name='firstName').value = "Doutor"
        browser.getControl(name='lastName').value = "Teste"        
        browser.getControl(name='email').value = "aa@aa.com"
        browser.getControl(name="form.button.save").click()
    
    def create_secretary(self):
        # vai pra pagina inicial e depois entra na pasta secretaria
        portal = self.portal
        browser = self.browser
        browser.open(portal.absolute_url() + '/view')

        # entra na pasta Secretary vai pra pagina de adicao de secretaria
        browser.getLink("Secretárias").click()
        browser.open(browser.url + "/createObject?type_name=Secretary")


        # preenche os dados do medico
        browser.getControl(name='firstName').value = "Secretary"
        browser.getControl(name='lastName').value = "Teste"        
        browser.getControl(name='email').value = "aa@aa.com"
        browser.getControl(name="form.button.save").click()

    def create_patient(self):
        # vai pra pagina inicial e depois entra na pasta patient
        portal = self.portal
        browser = self.browser
        browser.open(portal.absolute_url() + '/view')
        
        # entra na pasta Patients e vai pra pagina de adicao de paciente
        patients_link = browser.getLink("Pacientes")
        patients_link.click()
        browser.open(browser.url + "/createObject?type_name=Patient")
        
        # preenche os dados do paciente
        browser.getControl(name='firstName').value = "Paciente"
        browser.getControl(name='lastName').value = "Teste"
        browser.getControl(name="birthDate_year").value = ['1915']
        browser.getControl(name="birthDate_month").value = ['01']
        browser.getControl(name="birthDate_day").value = ['10']
        browser.getControl(name='email').value = "aa@aa.com"
        browser.getControl(name='contactPhone').value = "1133333333"
        browser.getControl(name="form.button.save").click()

    def edit_clinic(self):
        # vai pra pagina inicial e depois entra na pasta clinic na secao de edicao
        portal = self.portal
        browser = self.browser
        browser.open(portal.absolute_url() + '/Clinic/edit')
        # preenche os dados da clinica
        browser.getControl(name='name').value = "ClinicMed"
        browser.getControl(name='endereco').value = "Av Afonso Pena, 1500"
        browser.getControl(name='phone').value = "3199584756"
        browser.getControl(name='fax').value = "3199584757"
        browser.getControl(name='email').value = "aa@aa.com"
        browser.getControl(name="form.button.save").click()

    def test_edit_clinic(self):
        print "\n::::Teste editar clinica iniciou!" 
        # loga como admin
        self.login_as_admin()
        portal = self.portal
        browser = self.browser
        
        #As Manager----------------------------------
        setRoles(portal, TEST_USER_ID, MANAGER_ROLES)
        self.edit_clinic()
        # testa a mensagem de status e alguns dados
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        self.assertEqual(True, "ClinicMed" in browser.contents)
        self.assertEqual(True, "aa@aa.com" in browser.contents)
        
        #As Doctor----------------------------------
        setRoles(portal, TEST_USER_ID, DOCTOR_ROLES)
        self.edit_clinic()
        # testa a mensagem de status e alguns dados
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        self.assertEqual(True, "ClinicMed" in browser.contents)
        self.assertEqual(True, "aa@aa.com" in browser.contents)
        
        #As Secretary----------------------------------
        setRoles(portal, TEST_USER_ID, SECRETARY_ROLES)
        self.edit_clinic()
        # testa a mensagem de status e alguns dados
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        self.assertEqual(True, "ClinicMed" in browser.contents)
        self.assertEqual(True, "aa@aa.com" in browser.contents)
        
        #As Patient----------------------------------
        setRoles(portal, TEST_USER_ID, PATIENT_ROLES)
        self.edit_clinic()
        # testa a mensagem de status e alguns dados
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        self.assertEqual(True, "ClinicMed" in browser.contents)
        self.assertEqual(True, "aa@aa.com" in browser.contents)
        
        print "\n::::Teste editar clinica passou!" 
    
    def test_create_patient(self):
        
        print "\n::::Teste criar paciente iniciou!" 
        # loga como admin
        self.login_as_admin()
        portal = self.portal
        browser = self.browser

        #As Manager----------------------------------
        setRoles(portal, TEST_USER_ID, MANAGER_ROLES)
        self.create_patient()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Patients/pteste/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        
        #As Doctor----------------------------------
        setRoles(portal, TEST_USER_ID, DOCTOR_ROLES)
        self.create_patient()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Patients/pteste1/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        
        #As Secretary----------------------------------
        setRoles(portal, TEST_USER_ID, SECRETARY_ROLES)
        self.create_patient()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Patients/pteste2/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        
        #As Patient----------------------------------
        setRoles(portal, TEST_USER_ID, PATIENT_ROLES)
        self.create_patient()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Patients/pteste3/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        
        print "\n::::Teste criar paciente passou!" 
    
    def test_create_doctor(self):
        
        print "\n::::Teste criar doutor iniciou!" 
        
        app = self.app
        portal = self.portal
        browser = self.browser
        self.login_as_admin()
        
        #As Manger----------------------------------
        setRoles(portal, TEST_USER_ID, MANAGER_ROLES)
        self.create_doctor()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Doctors/dteste/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)  

        #As Doctor----------------------------------
        setRoles(portal, TEST_USER_ID, DOCTOR_ROLES)
        self.create_doctor()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Doctors/dteste1/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)          

        #As Secretary----------------------------------
        setRoles(portal, TEST_USER_ID, SECRETARY_ROLES)
        self.create_doctor()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Doctors/dteste2/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)          

        #As Patient----------------------------------
        setRoles(portal, TEST_USER_ID, PATIENT_ROLES)
        self.create_doctor()
        # testa a url e a mensagem de status
        # self.assertEqual(portal.absolute_url() + "/Doctors/dteste/", browser.url)
        #self.assertEqual(False, "As alterações foram salvas." in browser.contents)
        
        print "\n::::Teste criar doutor passou!" 
        
    def test_create_secretary(self):
        
        print "\n::::Teste criar secreataria iniciou!" 

        app = self.app
        portal = self.portal
        browser = self.browser
        self.login_as_admin()
        
        #As Manager----------------------------------
        setRoles(portal, TEST_USER_ID, MANAGER_ROLES)
        self.create_secretary()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Secretaries/steste/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)  

        #As Doctor----------------------------------
        setRoles(portal, TEST_USER_ID, DOCTOR_ROLES)
        self.create_secretary()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Secretaries/steste1/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)          

        #As Secretary----------------------------------
        setRoles(portal, TEST_USER_ID, SECRETARY_ROLES)
        self.create_secretary()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Secretaries/steste2/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)          

        #As Patient----------------------------------
        setRoles(portal, TEST_USER_ID, PATIENT_ROLES)
        self.create_secretary()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Secretaries/steste3/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        
        print "\n::::Teste criar secreataria passou!" 
    

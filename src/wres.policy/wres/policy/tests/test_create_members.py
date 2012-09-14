## coding=utf-8

import datetime
import unittest2 as unittest
from plone.testing.z2 import Browser
from plone.testing import z2
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD, SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.app.testing import setRoles

from wres.policy.testing import WRES_POLICY_FUNCTIONAL_TESTING
from wres.policy.test_browser_utils import *

from Testing.ZopeTestCase.utils import  startZServer
from Testing import ZopeTestCase
from Products.CMFCore.utils import getToolByName


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
    
    def setUp(self):
        self.app = self.layer['app']
        ZopeTestCase.utils.setupCoreSessions(self.app)
        self.app.REQUEST['SESSION'] = Session()
        
        self.portal = self.layer['portal']
        self.browser = Browser(self.app)

        z2.logout()
        z2.login(self.app['acl_users'], SITE_OWNER_NAME)
        create_members_by_debug_init(self)

    def create_doctor(self,fname="Joao",lname="Doutor",email="jd@email.com",specialty="endocrinology"):
        # vai pra pagina inicial e depois entra na pasta Patients
        portal = self.portal
        browser = self.browser
        browser.open(portal.absolute_url() + '/view')

        # entra na pasta Doctors e vai pra pagina de adicao de doutor
        browser.getLink("Médicos").click()
        browser.open(browser.url + "/createObject?type_name=Doctor")

        # preenche os dados do medico
        browser.getControl(name='firstName').value = fname
        browser.getControl(name='lastName').value = lname        
        browser.getControl(name='email').value = "aa@aa.com"
        browser.getControl(name='specialty1').value = [specialty]
        browser.getControl(name="form.button.save").click()
        
    
    def create_secretary(self,fname="Viviane",lname="Secretaria"):
        # vai pra pagina inicial e depois entra na pasta secretaria
        portal = self.portal
        browser = self.browser
        browser.open(portal.absolute_url() + '/view')

        # entra na pasta Secretary vai pra pagina de adicao de secretaria
        browser.getLink("Secretárias").click()
        browser.open(browser.url + "/createObject?type_name=Secretary")


        # preenche os dados do medico
        browser.getControl(name='firstName').value = fname
        browser.getControl(name='lastName').value = lname
        browser.getControl(name='email').value = "aa@aa.com"
        browser.getControl(name="form.button.save").click()

    def create_patient(self,fname="Marcos",lname="Paciente"):
        # vai pra pagina inicial e depois entra na pasta patient
        portal = self.portal
        browser = self.browser
        browser.open(portal.absolute_url() + '/view')
        
        # entra na pasta Patients e vai pra pagina de adicao de paciente
        patients_link = browser.getLink("Pacientes")
        patients_link.click()
        browser.open(browser.url + "/createObject?type_name=Patient")
        
        # preenche os dados do paciente
        browser.getControl(name='firstName').value = fname
        browser.getControl(name='lastName').value = lname
        browser.getControl(name="birthDate_year").value = ['1915']
        browser.getControl(name="birthDate_month").value = ['01']
        browser.getControl(name="birthDate_day").value = ['10']
        browser.getControl(name='email').value = "aa@aa.com"
        browser.getControl(name='contactPhone').value = "1133333333"
        browser.getControl(name="form.button.save").click()

    def edit_clinic(self,cname="Clinica Grande"):
        # vai pra pagina inicial e depois entra na pasta clinic na secao de edicao
        portal = self.portal
        browser = self.browser
        browser.open(portal.absolute_url() + '/Clinic/edit')
        # preenche os dados da clinica
        browser.getControl(name='name').value = "Clinica Grande"
        browser.getControl(name='street').value = "Av Afonso Pena"
        browser.getControl(name='number').value = "1500"
        browser.getControl(name='complemento').value = "Sala 404"
        browser.getControl(name='bairro').value = "Centro"
        browser.getControl(name='city').value = "Belo Horizonte"
        browser.getControl(name='phone').value = "3199584756"
        browser.getControl(name='fax').value = "3199584757"
        browser.getControl(name='email').value = "aa@aa.com"
        browser.getControl(name="form.button.save").click()

    def test_edit_clinic(self):
        print "\n::::Teste editar clinica iniciou!" 
        # loga como admin
        login_as_admin(self)
        portal = self.portal
        browser = self.browser
        
        
        #As Manager----------------------------------
        print "As Manager"
        setRoles(portal, TEST_USER_ID, MANAGER_ROLES)
        self.edit_clinic()
        # testa a mensagem de status e alguns dados
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        self.assertEqual(True, "Clinica Grande" in browser.contents)
        self.assertEqual(True, "aa@aa.com" in browser.contents)
        
        #As Doctor----------------------------------
        print "As Doctor"
        logout(self)
        login_as_doctor(self)
        self.edit_clinic()
        # testa a mensagem de status e alguns dados
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        self.assertEqual(True, "Clinica Grande" in browser.contents)
        self.assertEqual(True, "aa@aa.com" in browser.contents)
        
        #As Secretary----------------------------------
        print "As Secretary - False Case"
        logout(self)
        login_as_secretary(self)
        # testa a mensagem de status e alguns dados
        self.assertEqual(False, "As alterações foram salvas." in browser.contents)
        self.assertEqual(False, "ClinicMed" in browser.contents)
        self.assertEqual(False, "aa@aa.com" in browser.contents)
        
        print "\n::::Teste editar clinica passou!" 
        
    def test_create_patient(self):
        
        print "\n::::Teste criar paciente iniciou!" 
        # loga como admin
        login_as_admin(self)
        portal = self.portal
        browser = self.browser

        #As Manager----------------------------------
        print "As Manager"
        setRoles(portal, TEST_USER_ID, MANAGER_ROLES)
        self.create_patient()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Patients/mpaciente/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        
        #As Doctor----------------------------------
        print "As Doctor"
        logout(self)
        login_as_doctor(self)
        self.create_patient()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Patients/mpaciente1/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        
        #As Secretary----------------------------------
        print "As Secretary"
        logout(self)
        login_as_secretary(self)
        self.create_patient()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Patients/mpaciente2/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)
        
        print "\n::::Teste criar paciente passou!" 
    
    def test_create_doctor(self):
        
        print "\n::::Teste criar doutor iniciou!" 
        
        app = self.app
        portal = self.portal
        browser = self.browser
        login_as_admin(self)
        
        #As Manger----------------------------------
        print "As Manager"
        setRoles(portal, TEST_USER_ID, MANAGER_ROLES)
        self.create_doctor()
        # testa a url e a mensagem de status
        #import ipdb;ipdb.set_trace()
        self.assertEqual(portal.absolute_url() + "/Doctors/jdoutor/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)  

        #As Doctor----------------------------------
        print "As Doctor"
        logout(self)
        login_as_doctor(self)
        self.create_doctor()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Doctors/jdoutor1/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)          

        #As Secretary----------------------------------
        print "As Secretary - False Case"
        logout(self)
        login_as_secretary(self)
        self.create_doctor()
        # testa a url e a mensagem de status
        self.failUnless("Privilégios Insuficientes" in browser.contents)
        
        print "\n::::Teste criar doutor passou!" 
        
    def test_create_secretary(self):
        
        print "\n::::Teste criar secretaria iniciou!" 

        app = self.app
        portal = self.portal
        browser = self.browser
        login_as_admin(self)
        
        #As Manager----------------------------------
        print "As Manger"
        self.create_secretary()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Secretaries/vsecretaria/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)  

        #As Doctor----------------------------------
        print "As Doctor"
        logout(self)
        login_as_doctor(self)
        self.create_secretary()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Secretaries/vsecretaria1/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)          

        #As Secretary----------------------------------
        print "As Secretary - False Case"
        logout(self)
        login_as_secretary(self)
        self.create_secretary()
        # testa a url e a mensagem de status
        self.assertEqual(portal.absolute_url() + "/Secretaries/vsecretaria2/", browser.url)
        self.assertEqual(True, "As alterações foram salvas." in browser.contents)         
        
        print "\n::::Teste criar secretaria passou!" 
    
    #def create_members_by_debug_init(self,secs=1,pats=1,docs=1,admins=1,clins=1):
        #browser = self.browser
        #portal = self.portal
        #login_as_admin(self)
        
        #print "Criando " + str(secs) + " Secretárias, " + str(pats) + " Pacientes, " + str(docs) + " Doutores, " + str(admins) + " Administradores e " + str(clins) + " Clinicas."
        #browser.open(portal.absolute_url() + "/debug_init")
        #logout(self)
    

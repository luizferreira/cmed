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

class TestSetup(unittest.TestCase):
    
    layer = WRES_POLICY_FUNCTIONAL_TESTING
    
    def addDoctor(self):
        create_uemr_user(self.portal, DOCTOR_TEST_USER_ID, 'Doctor')
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.browser = Browser(self.app)
        
        #Cria P pacientes e D doutores para testes create_patients_doctors(P,D)
        self.create_patients_doctors(10,20)
    
    def create_patients_doctors(self,P,D):
        self.login_as_admin()
        for i in range(P):
            self.create_patient()
        for i in range(D):
            self.create_doctor()
        z2.logout()

    def login_as_admin(self):
        # Go admin
        portal = self.portal
        browser = self.browser
        # setRoles(portal, TEST_USER_ID, ('Manager', 'Doctor'))
        # browser = self.browser
        browser.open(portal.absolute_url() + "/login_form")
        browser.getControl(name='__ac_name').value = "admin"
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
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

    def verifyPatient(self,patient):
        portal = self.portal
        browser = self.browser
        
        #Verifica se paciente existe
        try:
            browser.open(portal.absolute_url() + "/Patients/" + patient )
        except:
            print "\nNão foi possivel acessar o prontuário do paciente: " + patient + "."
            return False
            
        return True
    
    def get_doctor_ref(self):
        #Pega referencia do doutor dteste
        portal = self.portal
        browser = self.browser
        ref = portal.Doctors.dteste.UID()
        return ref
        
        #Pega referencia de forma randômica 
        #pc = getToolByName(portal,"portal_catalog")
        #brains = pc.searchResults({'meta_type':'Doctor'})
        #n_doctors = len(brains)
        #import ipdb;ipdb.set_trace()
        #rand_index = random.randrange(0,n_doctors)
        #ref = brains[rand_index].getObject().UID()
    
    def create_document(self,PATIENT_ID,PATIENT_URL):
        #TODO: (matheus) Descobrir porque nao consigo acessar browser.open(PATIENT_URL + "/chartFolder"), talves
        #template chart_folder_view está acessando algo que o teste nao deixa passar e portanto da erro 500
        portal = self.portal
        browser = self.browser
        
        # Entra e verifica o prontuario de um paciente
        self.failUnless(self.verifyPatient(PATIENT_ID))
        
        # Entra em Consultas
        browser.open(PATIENT_URL + "/chartFolder/documents")
        
        
        #Entra em novo documento generico
        browser.open(PATIENT_URL + "/chartFolder_hidden/documents/createObject?type_name=GenericDocument")
        
        #Pega a refarência de um Doutor
        doctor_ref = self.get_doctor_ref()
        
        #Prenche campos obrigatorios, nao preenche corpo pois o msm é javascript
        browser.getControl(name='document_type').value = ["Retorno"]
        browser.getControl(name='doctor').value = doctor_ref
        browser.getControl(name="form.button.save").click()
    
    def test_create_document(self):
        print "\n::::Teste criar documento iniciou!" 
        portal = self.portal
        browser = self.browser
        self.login_as_admin()
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        self.create_document(PATIENT_ID, PATIENT_URL)
        #A mensagem de status e conteúdo
        self.failUnless("As alterações foram salvas." in browser.contents)
        self.failUnless("Criado por" in browser.contents)
        
        print "\n::::Teste criar documento passou!" 
        
        
        
        
        
        

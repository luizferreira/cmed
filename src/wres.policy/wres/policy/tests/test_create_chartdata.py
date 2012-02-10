## coding=utf-8

import datetime
from DateTime.DateTime import *
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
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.browser = Browser(self.app)
        
        #Cria P pacientes e D doutores para testes create_patients_doctors(P,D)
        self.create_patients_doctors(2,2)
        
        #Ignore erros
        #self.browser.handleErrors = False # Don't get HTTP 500 pages
        #self.portal.error_log._ignored_exceptions = ()

        #def raising(self, info):
            #import traceback
            #traceback.print_tb(info[2])
            #print info[1]

        #from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        #SiteErrorLog.raising = raising
    
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

    def verifyChartPatient(self,patient):
        portal = self.portal
        browser = self.browser
        
        #Verifica se paciente existe
        try:
            #Cria a pasta chartFolder se nao existir
            browser.open(portal.absolute_url() + "/Patients/" + patient +"/chartFolder/documents" )
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
        #TODO: (matheus) 
        #   1-Descobrir porque nao consigo acessar browser.open(PATIENT_URL + "/chartFolder"), talvez
        #   template chart_folder_view está acessando algo que o teste nao deixa passar e portanto da erro 500
        #
        #   2-O documento é criado sem "Corpo do Documento" (não consigo preencher os campos), o corpo é setado via python
        #   depois
        
        portal = self.portal
        browser = self.browser
        
        # Entra e verifica o prontuario de um paciente alem de criar o chartFolder
        self.failUnless(self.verifyChartPatient(PATIENT_ID))
        
        # Entra em Consultas
        browser.open(PATIENT_URL + "/chartFolder/documents")
        
        #Entra em novo documento generico
        browser.open(PATIENT_URL + "/chartFolder_hidden/documents/createObject?type_name=GenericDocument")
        
        #Pequeno parser para pegar o id do documento
        url = browser.url
        inicio = url.find("genericdocument.")
        fim = -len("/edit")
        doc_id = url[inicio:fim]
        
        #Pega a refarência de um Doutor
        doctor_ref = self.get_doctor_ref()
        
        #Prenche campos obrigatorios, nao preenche corpo pois o msm é javascript
        browser.getControl(name='document_type').value = ["Retorno"]
        browser.getControl(name='doctor').value = doctor_ref
        browser.getControl(name="form.button.save").click()
        return doc_id
        
    def create_impresso(self,PATIENT_ID,PATIENT_URL):
        #TODO: Igual ao create document
        portal = self.portal
        browser = self.browser
        
        # Entra e verifica o prontuario de um paciente
        self.failUnless(self.verifyChartPatient(PATIENT_ID))
        
        # Entra em Impressos
        browser.open(PATIENT_URL + "/chartFolder/impressos")
        
        #Entra em novo Impresso
        browser.open(PATIENT_URL + "/chartFolder_hidden/impressos/createObject?type_name=Impresso")
        
        #Pequeno parser para pegar o id do impresso
        url = browser.url
        inicio = url.find("impresso.")
        fim = -len("/edit")
        impresso_id = url[inicio:fim]
        
        #Pega a refarência de um Doutor
        doctor_ref = self.get_doctor_ref()
        
        #Prenche campos obrigatorios, nao preenche corpo pois o msm é javascript
        browser.getControl(name='document_type').value = ["atestado"]
        browser.getControl(name='doctor').value = doctor_ref
        browser.getControl(name="form.button.save").click()
        return impresso_id

    def edit_impresso(self,PATIENT_ID,PATIENT_URL,impresso_id):
        #Edicao do documento via python, não deveria ser assim (integration test), mas é feito para testar
        #possiveis problemas de permissão
        portal = self.portal
        browser = self.browser
        
        #Edicao
        patient = getattr(portal.Patients,PATIENT_ID)
        document = getattr(patient.chartFolder.impressos,impresso_id)
        document.setGdocument_body("Escrevendo no corpo do impresso.")
        self.failUnless("Escrevendo no corpo do impresso." in document.getGdocument_body() )        
        
    
    def edit_document(self,PATIENT_ID,PATIENT_URL,document_id):
        #Edicao do documento via python, não deveria ser assim (integration test), mas é feito para testar
        #possiveis problemas de permissão
        portal = self.portal
        browser = self.browser
        
        #Edicao
        patient = getattr(portal.Patients,PATIENT_ID)
        document = getattr(patient.chartFolder.documents,document_id)
        document.setGdocument_body("Escrevendo no corpo do documento.")
        self.failUnless("Escrevendo no corpo do documento." in document.getGdocument_body() )
    
    def create_medications(self,PATIENT_ID,PATIENT_URL,medication="Dorflex",concentration="40 mg",quantity="3",use="Oral",status="active"):
        portal = self.portal
        browser = self.browser
        
        # Entra e verifica o prontuario de um paciente alem de criar o chartFolder
        self.failUnless(self.verifyChartPatient(PATIENT_ID))
        
        browser.open(PATIENT_URL + "/chartFolder_hidden/show_medications")
        
        browser.getControl(name='medication').value = medication
        browser.getControl(name='concentration').value = concentration
        browser.getControl(name='quantity').value = quantity
        browser.getControl(name='use').value = use
        browser.getControl(name='status').value = [status]
        browser.getControl(name="form.button.save").click()
        
    def edit_medications(self,PATIENT_ID,PATIENT_URL):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_medications")
        
        #Pequeno parse para pegar o id de um medicamento, no caso o primeiro da lista
        try:
            self.assertEqual(True,"id=medication." in browser.contents)
        except:
            print "Nao existe medicamento para editar"
            return
            
        pag = browser.contents
        inicio = pag.find("id=medication.")
        inicio = inicio + len("id=medication.")
        fim = inicio + pag[inicio:].find("'")
        med_id = pag[inicio:fim]
        
        #Entrar na pagina de edicao
        browser.open(PATIENT_URL + "/chartFolder_hidden/edit_medication?id=medication." + med_id)
        browser.getControl(name='medication').value = "Medicamento Editado"
        browser.getControl(name='concentration').value = "Concentracao Editado"
        browser.getControl(name='quantity').value = "Quantidade Editado"
        browser.getControl(name='use').value = "Uso Editado"
        browser.getControl(name='status').value = ["active"]
        browser.getControl(name='form.button.save').click()
        
    def inactivate_medications(self,PATIENT_ID,PATIENT_URL):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_medications")
        
        try:
            self.assertEqual(True,"id=medication." in browser.contents)
        except:
            print "Nao existe medicamento para inativar"
            self.assertEqual(True,"id=medication." in browser.contents)
        
        #Pequeno parse para pegar o id de um medicamento, no caso o primeiro da lista
        pag = browser.contents
        inicio = pag.find("id=medication.")
        inicio = inicio + len("id=medication.")
        fim = inicio + pag[inicio:].find("'")
        med_id = pag[inicio:fim]
        
        #Entrar na pagina de Inativação
        browser.open(PATIENT_URL + "/chartFolder_hidden/inactivate_medication?id=medication." + med_id)
        browser.getControl(name='shown_end_date').value = "05/05/03"
        browser.getControl(name='note').value = "Nota do Medicamento inativado"
        browser.getControl(name='form.button.inactivate').click()
    
    def generate_prescription(self,PATIENT_ID,PATIENT_URL):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_medications")
        try:
            self.assertEqual(True,"id=medication." in browser.contents)
        except:
            print "Nao existe medicamento para gerar prescricao"
            self.assertEqual(True,"id=medication." in browser.contents)
        
        browser.getControl(name='form.button.generate').click()
        browser.getControl(name='form.button.confirm').click()
        
    def visualize_prescription(self,PATIENT_ID,PATIENT_URL):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL + "/chartFolder_hidden/prescriptions_history")
        try:
            self.assertEqual(True,"Visualizar" in browser.contents)
        except:
            print "Nao existe medicamento para gerar visualização"
            self.assertEqual(True,"Visualizar." in browser.contents)
        
        #Pequeno parse para pegar o id de uma prescricao, no caso o primeiro da lista
        pag = browser.contents
        inicio = pag.find("id=prescription.")
        inicio = inicio + len("id=prescription.")
        fim = inicio + pag[inicio:].find('"')
        pre_id = pag[inicio:fim]
        browser.open(PATIENT_URL + "/chartFolder_hidden/print_prescription?id=prescription."+ pre_id)
    
    def create_problems(self,PATIENT_ID,PATIENT_URL,problem="Diarréia",code="J00-J99",status="active"):
        portal = self.portal
        browser = self.browser
        
        # Entra e verifica o prontuario de um paciente alem de criar o chartFolder
        self.failUnless(self.verifyChartPatient(PATIENT_ID))
        
        browser.open(PATIENT_URL + "/chartFolder_hidden/show_problem_list")
        
        browser.getControl(name='problem').value = problem
        browser.getControl(name='code').value = code
        browser.getControl(name='started').value = DateTime().Date()
        browser.getControl(name='state').value = [status]
        browser.getControl(name="form.button.save").click()

    
    def edit_problems(self,PATIENT_ID,PATIENT_URL,problem="Diarréia",code="J00-J99",status="active"):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_problem_list")
        
        
        try:
            self.assertEqual(True,'value="problem.' in browser.contents)
        except:
            print "Nao existe problemas para editar"
            self.assertEqual(True,'value="problem.' in browser.contents)
            return
        
        #Pequeno parse para pegar o id de um problema, no caso o primeiro da lista
        pag = browser.contents
        inicio = pag.find('value="problem.')
        inicio = inicio + len('value="problem.')
        fim = inicio + pag[inicio:].find('"')
        pro_id = pag[inicio:fim]
        
        
        #Entrar na pagina de edicao
        browser.open(PATIENT_URL + "/chartFolder_hidden/show_problem_list?form.submitted=1&id=problem." + pro_id + "&form.button.edit=Editar")
        #import ipdb;ipdb.set_trace()
        browser.getControl(name='problem').value = problem
        browser.getControl(name='code').value = code
        browser.getControl(name='started').value = DateTime().Date()
        browser.getControl(name='state').value = [status]
        browser.getControl(name="form.button.save").click()
    
    def resolve_problems(self,PATIENT_ID,PATIENT_URL,date=DateTime().Date(),note="Nota do resolvimento"):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_problem_list")
        
        try:
            self.assertEqual(True,'value="problem.' in browser.contents)
        except:
            print "Nao existe problemas para resolver"
            self.assertEqual(True,'value="problem.' in browser.contents)
            return
        
        #Pequeno parse para pegar o id de um problema, no caso o primeiro da lista
        pag = browser.contents
        inicio = pag.find('value="problem.')
        inicio = inicio + len('value="problem.')
        fim = inicio + pag[inicio:].find('"')
        pro_id = pag[inicio:fim]
        
        #Entrar na pagina de solução
        browser.open(PATIENT_URL + "/chartFolder_hidden/show_problem_list?form.submitted=1&id=problem." + pro_id + "&form.button.resolve=Resolver")
        browser.getControl(name='end_date').value = date
        browser.getControl(name='note').value = note
        browser.getControl(name="form.button.resolve").click()
    
    def create_allergy(self,PATIENT_ID,PATIENT_URL,allergy="Alergia a cigarro",reaction="Taquicardia",date=DateTime().Date()):
        portal = self.portal
        browser = self.browser
        
        # Entra e verifica o prontuario de um paciente alem de criar o chartFolder
        self.failUnless(self.verifyChartPatient(PATIENT_ID))
        browser.open(PATIENT_URL+"/chartFolder/show_allergies")
        
        
        #import ipdb;ipdb.set_trace()
        browser.getControl(name='allergy').value = allergy
        browser.getControl(name='reaction').value = reaction
        browser.getControl(name='date').value = date
        browser.getControl(name="form.button.save").click()
    
    def create_exam(self,PATIENT_ID,PATIENT_URL,exam="Hemoglobina",value="500 mg/ml",date=DateTime().Date()):
        portal = self.portal
        browser = self.browser
        
        # Entra e verifica o prontuario de um paciente alem de criar o chartFolder
        self.failUnless(self.verifyChartPatient(PATIENT_ID))
        browser.open(PATIENT_URL+"/chartFolder/show_exams")
        
        browser.getControl(name='exam').value = exam
        browser.getControl(name='value').value = value
        browser.getControl(name='date').value = date
        browser.getControl(name="form.button.save").click()
    
    def test_create_exam(self):
        print "\n::::Teste criar exames iniciou!" 
        portal = self.portal
        browser = self.browser
        self.login_as_admin()
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        #Cria 3 exames
        self.create_exam(PATIENT_ID, PATIENT_URL)
        self.failUnless("Exame adicionado." in browser.contents)
        self.failUnless("Hemoglobina" in browser.contents[browser.contents.find("<legend>Exames"):])
        self.create_exam(PATIENT_ID, PATIENT_URL,"Globulos Brancos")
        self.failUnless("Exame adicionado." in browser.contents)
        self.failUnless("Globulos Brancos" in browser.contents[browser.contents.find("<legend>Exames"):])
        self.create_exam(PATIENT_ID, PATIENT_URL,"Fezes")
        self.failUnless("Exame adicionado." in browser.contents)
        self.failUnless("Fezes" in browser.contents[browser.contents.find("<legend>Exames"):])
        
        #As Doctor----------------------------------
        setRoles(portal, TEST_USER_ID, DOCTOR_ROLES)
        #Cria 3 alergias
        self.create_exam(PATIENT_ID, PATIENT_URL)
        self.failUnless("Exame adicionado." in browser.contents)
        self.failUnless("Hemoglobina" in browser.contents[browser.contents.find("<legend>Exames"):])
        self.create_exam(PATIENT_ID, PATIENT_URL,"Globulos Brancos")
        self.failUnless("Exame adicionado." in browser.contents)
        self.failUnless("Globulos Brancos" in browser.contents[browser.contents.find("<legend>Exames"):])
        self.create_exam(PATIENT_ID, PATIENT_URL,"Fezes")
        self.failUnless("Exame adicionado." in browser.contents)
        self.failUnless("Fezes" in browser.contents[browser.contents.find("<legend>Exames"):])
        
        
        print "\n::::Teste criar exames passou!" 
       
    
    def test_create_allergy(self):
        print "\n::::Teste criar alergias iniciou!" 
        portal = self.portal
        browser = self.browser
        self.login_as_admin()
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        #Cria 3 alergias
        self.create_allergy(PATIENT_ID, PATIENT_URL)
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a cigarro" in browser.contents[browser.contents.find("<legend>Alergias</legend>"):])
        self.create_allergy(PATIENT_ID, PATIENT_URL,"Alergia a poeira")
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a poeira" in browser.contents[browser.contents.find("<legend>Alergias</legend>"):])
        self.create_allergy(PATIENT_ID, PATIENT_URL,"Alergia a flores")
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a flores" in browser.contents[browser.contents.find("<legend>Alergias</legend>"):])
        
        #As Doctor----------------------------------
        setRoles(portal, TEST_USER_ID, DOCTOR_ROLES)
        #Cria 3 alergias
        self.create_allergy(PATIENT_ID, PATIENT_URL)
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a cigarro" in browser.contents[browser.contents.find("<legend>Alergias</legend>"):])
        self.create_allergy(PATIENT_ID, PATIENT_URL,"Alergia a poeira")
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a poeira" in browser.contents[browser.contents.find("<legend>Alergias</legend>"):])
        self.create_allergy(PATIENT_ID, PATIENT_URL,"Alergia a flores")
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a flores" in browser.contents[browser.contents.find("<legend>Alergias</legend>"):])
        
        print "\n::::Teste criar alergias passou!" 
        
        
    
    def test_create_edit_resolve_problems(self):
        print "\n::::Teste criar, editar, resolver problemas iniciou!" 
        portal = self.portal
        browser = self.browser
        self.login_as_admin()
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        #Cria 3 problemas(um já resolvido), depois edita um mudando o status para resolvido, depois resolve outro diretamente.
        #Create problems
        self.create_problems(PATIENT_ID, PATIENT_URL)
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        self.create_problems(PATIENT_ID, PATIENT_URL,"Dor de cabeça")
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        self.failUnless("Dor de cabeça" in browser.contents)
        
        #Testa se "Dor de braço" dentro do fildset "Resolvidos" por causa do status "inactive"
        self.create_problems(PATIENT_ID, PATIENT_URL,"Dor de braço","456 7897","inactive")
        inicio = browser.contents.find('id="historical"')
        self.failUnless("Dor de braço" in browser.contents[inicio:])
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        #Edit Problems
            #Edita a diarreia
        self.edit_problems(PATIENT_ID,PATIENT_URL,problem="Tendinite",status="inactive")
        self.failUnless("Tendinite" in browser.contents[browser.contents.find("Resolvidos"):])
        #Resolve problem
            #Resolve dor de cabeça
        self.resolve_problems(PATIENT_ID,PATIENT_URL)
        self.failUnless("Dor de cabeça" in browser.contents[browser.contents.find("Resolvidos"):])
        
        #As Doctor----------------------------------
        setRoles(portal, TEST_USER_ID, DOCTOR_ROLES)
        #Cria 3 problemas(um já resolvido), depois edita um mudando o status para resolvido, depois resolve outro diretamente.
        #Create problems
        self.create_problems(PATIENT_ID, PATIENT_URL)
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        self.create_problems(PATIENT_ID, PATIENT_URL,"Dor de cabeça")
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        self.failUnless("Dor de cabeça" in browser.contents)
        
        #Testa se "Dor de braço" dentro do fildset "Resolvidos" por causa do status "inactive"
        self.create_problems(PATIENT_ID, PATIENT_URL,"Dor de braço","456 7897","inactive")
        inicio = browser.contents.find('id="historical"')
        self.failUnless("Dor de braço" in browser.contents[inicio:])
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        #Edit Problems
            #Edita a diarreia
        self.edit_problems(PATIENT_ID,PATIENT_URL,problem="Tendinite",status="inactive")
        self.failUnless("Tendinite" in browser.contents[browser.contents.find("Resolvidos"):])
        #Resolve problem
            #Resolve dor de cabeça
        self.resolve_problems(PATIENT_ID,PATIENT_URL)
        self.failUnless("Dor de cabeça" in browser.contents[browser.contents.find("Resolvidos"):])
        
        print "\n::::Teste criar, editar, resolver problemas passou!" 
        
        
        
    def test_create_edit_inativate_medications_and_show_prescriptions(self):
        print "\n::::Teste criar, editar, inativar medicamentos e apresentar prescrições iniciou!" 
        portal = self.portal
        browser = self.browser
        self.login_as_admin()
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        #Create medications
        self.create_medications(PATIENT_ID, PATIENT_URL)
        self.failUnless("Medicamento adicionado" in browser.contents)
        self.create_medications(PATIENT_ID, PATIENT_URL,"Aspirina")
        self.failUnless("Aspirina" in browser.contents)
        self.create_medications(PATIENT_ID, PATIENT_URL,"Tilenol")
        self.failUnless("Tilenol" in browser.contents)
        self.create_medications(PATIENT_ID, PATIENT_URL,"Energil C")
        self.failUnless("Energil C" in browser.contents)
        #Generate Prescriptions
        self.generate_prescription(PATIENT_ID,PATIENT_URL)
        self.failUnless('id="prescriptions"' in browser.contents)
        self.failUnless("CRM:" in browser.contents)
        #Visualize Prescription
        self.visualize_prescription(PATIENT_ID,PATIENT_URL)
        self.failUnless("CRM:" in browser.contents)
        self.failUnless('id="prescriptions"' in browser.contents)
        #Edit Medications
        self.edit_medications(PATIENT_ID,PATIENT_URL)
        self.failUnless("Medicamento Editado" in browser.contents)
        self.failUnless("Concentracao Editado" in browser.contents)
        self.failUnless("Quantidade Editado" in browser.contents)
        self.failUnless("Uso Editado" in browser.contents)
        #Inactive Medications
        self.inactivate_medications(PATIENT_ID,PATIENT_URL)
        self.failUnless("Medicamento enviado para o histórico." in browser.contents)
        self.failUnless("Nota do Medicamento inativado" in browser.contents)
        
        PATIENT_ID = "pteste1"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Doctor----------------------------------
        setRoles(portal, TEST_USER_ID, DOCTOR_ROLES)
        #Create medications
        self.create_medications(PATIENT_ID, PATIENT_URL)
        self.failUnless("Medicamento adicionado" in browser.contents)
        self.create_medications(PATIENT_ID, PATIENT_URL,"Aspirina")
        self.failUnless("Aspirina" in browser.contents)
        self.create_medications(PATIENT_ID, PATIENT_URL,"Tilenol")
        self.failUnless("Tilenol" in browser.contents)
        self.create_medications(PATIENT_ID, PATIENT_URL,"Energil C")
        self.failUnless("Energil C" in browser.contents)
        #Generate Prescriptions
        self.generate_prescription(PATIENT_ID,PATIENT_URL)
        self.failUnless('id="prescriptions"' in browser.contents)
        self.failUnless("CRM:" in browser.contents)
        #Visualize Prescription
        self.visualize_prescription(PATIENT_ID,PATIENT_URL)
        self.failUnless("CRM:" in browser.contents)
        self.failUnless('id="prescriptions"' in browser.contents)
        #Edit Medications
        self.edit_medications(PATIENT_ID,PATIENT_URL)
        self.failUnless("Medicamento Editado" in browser.contents)
        self.failUnless("Concentracao Editado" in browser.contents)
        self.failUnless("Quantidade Editado" in browser.contents)
        self.failUnless("Uso Editado" in browser.contents)
        #Inactive Medications
        self.inactivate_medications(PATIENT_ID,PATIENT_URL)
        self.failUnless("Medicamento enviado para o histórico." in browser.contents)
        self.failUnless("Nota do Medicamento inativado" in browser.contents)

        print "\n::::Teste criar, editar, inativar medicamentos e apresentar prescrições passou!" 
        
        
        
        
    def test_create_edit_document(self):
        print "\n::::Teste criar e editar documento iniciou!" 
        portal = self.portal
        browser = self.browser
        self.login_as_admin()
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        #Create document
        document_id = self.create_document(PATIENT_ID, PATIENT_URL)
        self.failUnless("As alterações foram salvas." in browser.contents)
        self.failUnless("Criado por" in browser.contents)
        #Edit document
        self.edit_document(PATIENT_ID,PATIENT_URL,document_id)
        
        #As Doctor----------------------------------
        setRoles(portal, TEST_USER_ID, DOCTOR_ROLES)
        #Create document
        document_id = self.create_document(PATIENT_ID, PATIENT_URL)
        self.failUnless("As alterações foram salvas." in browser.contents)
        self.failUnless("Criado por" in browser.contents)
        #Edit document
        self.edit_document(PATIENT_ID,PATIENT_URL,document_id)
        
        print "\n::::Teste criar e editar documento passou!" 
        
        
    def test_create_edit_impresso(self):
        print "\n::::Teste criar e editar impresso iniciou!" 
        portal = self.portal
        browser = self.browser
        self.login_as_admin()
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        #Create document
        impresso_id = self.create_impresso(PATIENT_ID, PATIENT_URL)
        self.failUnless("As alterações foram salvas." in browser.contents)
        self.failUnless("Criado por" in browser.contents)
        #Edit document
        self.edit_impresso(PATIENT_ID,PATIENT_URL,impresso_id)
        
        #As Doctor----------------------------------
        setRoles(portal, TEST_USER_ID, DOCTOR_ROLES)
        #Create document
        impresso_id = self.create_impresso(PATIENT_ID, PATIENT_URL)
        self.failUnless("As alterações foram salvas." in browser.contents)
        self.failUnless("Criado por" in browser.contents)
        #Edit document
        self.edit_impresso(PATIENT_ID,PATIENT_URL,impresso_id)
        
        print "\n::::Teste criar e editar impresso passou!"
     

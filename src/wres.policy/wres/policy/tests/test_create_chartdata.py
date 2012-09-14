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
from Testing import ZopeTestCase
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
        ZopeTestCase.utils.setupCoreSessions(self.app)
        self.app.REQUEST['SESSION'] = Session()

        self.portal = self.layer['portal']
        self.browser = Browser(self.app)
        
        #Cria P pacientes e D doutores para testes create_patients_doctors(P,D)
        create_members_by_debug_init(self,pats=5,docs=5)
       
    def create_patients_doctors(self,P,D):
        login_as_admin(self)
        for i in range(P):
            self.create_patient()
        for i in range(D):
            self.create_doctor()
        z2.logout()

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
        browser.getControl(name='document_type').value = ["Atestado"]
        browser.getControl(name='doctor').value = doctor_ref
        browser.getControl(name="form.button.save").click()
        return impresso_id

    def edit_impresso(self,PATIENT_ID,PATIENT_URL,impresso_id):
        #TODO:Edicao do documento via python, não deveria ser assim (integration test), mas é feito para testar
        #possiveis problemas de permissão
        portal = self.portal
        browser = self.browser
        
        #Edicao
        patient = getattr(portal.Patients,PATIENT_ID)
        document = getattr(patient.chartFolder.impressos,impresso_id)
        document.setGdocument_body("Escrevendo no corpo do impresso.")
        self.failUnless("Escrevendo no corpo do impresso." in document.getGdocument_body() )        
        
    
    def edit_document(self,PATIENT_ID,PATIENT_URL,document_id):
        #TODO:Edicao do documento via python, não deveria ser assim (integration test), mas é feito para testar
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
            self.assertEqual(True,"id=medications." in browser.contents)
        except:
            print "Nao existe medicamento para editar"
            self.assertEqual(True,"id=medications." in browser.contents)
            
        pag = browser.contents
        inicio = pag.find("id=medications.")
        inicio = inicio + len("id=medications.")
        fim = inicio + pag[inicio:].find("'")
        med_id = pag[inicio:fim]
        
        #Entrar na pagina de edicao
        browser.open(PATIENT_URL + "/chartFolder_hidden/edit_medication?id=medications." + med_id)
        browser.getControl(name='medication').value = "Medicamento Editado"
        browser.getControl(name='concentration').value = "Concentracao Editado"
        browser.getControl(name='quantity').value = "Quantidade Editado"
        browser.getControl(name='use').value = "Uso Editado"
        browser.getControl(name='form.button.save').click()
        
    def inactivate_medications(self,PATIENT_ID,PATIENT_URL):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_medications")
        
        try:
            self.assertEqual(True,"id=medications." in browser.contents)
        except:
            print "Nao existe medicamento para inativar"
            self.assertEqual(True,"id=medications." in browser.contents)
        
        #Pequeno parse para pegar o id de um medicamento, no caso o primeiro da lista
        pag = browser.contents
        inicio = pag.find("id=medications.")
        inicio = inicio + len("id=medications.")
        fim = inicio + pag[inicio:].find("'")
        med_id = pag[inicio:fim]
        
        #Entrar na pagina de Inativação
        browser.open(PATIENT_URL + "/chartFolder_hidden/inactivate_medication?id=medications." + med_id)
        browser.getControl(name='note').value = "Nota do Medicamento inativado"
        browser.getControl(name='form.button.inactivate').click()
    
    def generate_prescription(self,PATIENT_ID,PATIENT_URL):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_medications")
        try:
            self.assertEqual(True,'name="form.button.generate"' in browser.contents)
        except:
            print "Nao existe medicamento para gerar prescricao"
            self.assertEqual(True,'name="form.button.generate"' in browser.contents)
        
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
        inicio = pag.find("id=prescriptions.")
        inicio = inicio + len("id=prescriptions.")
        fim = inicio + pag[inicio:].find('"')
        pre_id = pag[inicio:fim]
        browser.open(PATIENT_URL + "/chartFolder_hidden/print_prescription?id=prescriptions."+ pre_id)
    
    def create_problems(self,PATIENT_ID,PATIENT_URL,problem="Diarréia",code="J00-J99",status="active"):
        portal = self.portal
        browser = self.browser
        
        # Entra e verifica o prontuario de um paciente alem de criar o chartFolder
        self.failUnless(self.verifyChartPatient(PATIENT_ID))
        
        browser.open(PATIENT_URL + "/chartFolder_hidden/show_problem_list")
        
        browser.getControl(name='problem').value = problem
        browser.getControl(name='code').value = code
        browser.getControl(name='started').value = DateTime().Date()
        browser.getControl(name="form.button.save").click()

    
    def edit_problems(self,PATIENT_ID,PATIENT_URL,problem="Diarréia",code="J00-J99",status="active"):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_problem_list")
        
        
        try:
            self.assertEqual(True,'value="problems.' in browser.contents)
        except:
            print "Nao existe problemas para editar"
            self.assertEqual(True,'value="problems.' in browser.contents)
        
        #Pequeno parse para pegar o id de um problema, no caso o primeiro da lista
        pag = browser.contents
        inicio = pag.find('value="problems.')
        inicio = inicio + len('value="problems.')
        fim = inicio + pag[inicio:].find('"')
        pro_id = pag[inicio:fim]
        
        
        #Entrar na pagina de edicao
        browser.open(PATIENT_URL + "/chartFolder_hidden/show_problem_list?form.submitted=1&id=problems." + pro_id + "&form.button.edit=Editar")
        browser.getControl(name='problem').value = problem
        browser.getControl(name='code').value = code
        browser.getControl(name='started').value = DateTime().Date()
        browser.getControl(name="form.button.save").click()
    
    def resolve_problems(self,PATIENT_ID,PATIENT_URL,date=DateTime().Date(),note="Nota editada resolvido"):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_problem_list")
        
        try:
            self.assertEqual(True,'value="problems.' in browser.contents)
        except:
            print "Nao existe problemas para resolver"
            self.assertEqual(True,'value="problems.' in browser.contents)
            return
        
        #Pequeno parse para pegar o id de um problema, no caso o primeiro da lista
        #TODO: fazer esse parser funcionar direito para não só pegar o primeiro da lista
        pag = browser.contents
        inicio = pag.find('value="problems.')
        inicio = inicio + len('value="problems.')
        fim = inicio + pag[inicio:].find('"')
        pro_id = pag[inicio:fim]
        #Entrar na pagina de solução
        browser.open(PATIENT_URL + "/chartFolder_hidden/show_problem_list?form.submitted=1&id=problems." + pro_id + "&form.button.resolve=Resolver")
        browser.getControl(name='note').value = note
        browser.getControl(name="form.button.resolve").click()
    
    def edit_allergy(self,PATIENT_ID,PATIENT_URL,old_allergy="Alergia a cigarro",new_allergy="Alergia a fumaca de cigarro"):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_allergies")
        
        try:
            self.assertEqual(True,'<legend>Alergias Registradas</legend>' in browser.contents)
        except:
            print "Nao existe alergias para editar"
            self.assertEqual(True,'<legend>Alergias Registradas</legend>' in browser.contents)
        
        #Pequeno parse para pegar o id de uma alergia, no caso o primeiro da lista 
        #TODO: fazer esse parser funcionar direito para não só pegar o primeiro da lista
        pag = browser.contents
        inicio = pag.find('id=allergies.')
        inicio = inicio + len('id=allergies.')
        fim = inicio + pag[inicio:].find("'")
        allergy_id = pag[inicio:fim]
        
        
        #Entrar na pagina de edicao
        browser.open(PATIENT_URL + "/chartFolder_hidden/edit_allergy?id=allergies." + allergy_id)
        browser.getControl(name='allergy').value = new_allergy
        browser.getControl(name='reaction').value = "Inflacao da cabeca"
        browser.getControl(name='date').value = DateTime().Date()
        browser.getControl(name="form.button.save").click()
        
    def inactivate_allergy(self,PATIENT_ID,PATIENT_URL,allergy="Alergia a fumaca de cigarro"):
        portal = self.portal
        browser = self.browser
        
        browser.open(PATIENT_URL+"/chartFolder/show_allergies")
        
        try:
            self.assertEqual(True,'<legend>Alergias Registradas</legend>' in browser.contents)
        except:
            print "Nao existe alergias para editar"
            self.assertEqual(True,'<legend>Alergias Registradas</legend>' in browser.contents)
        
        #Pequeno parse para pegar o id de uma alergia, no caso o primeiro da lista 
        #TODO: fazer esse parser funcionar direito para não só pegar o primeiro da lista
        pag = browser.contents
        inicio = pag.find('id=allergies.')
        inicio = inicio + len('id=allergies.')
        fim = inicio + pag[inicio:].find("'")
        allergy_id = pag[inicio:fim]
        
        
        #Entrar na pagina de edicao
        browser.open(PATIENT_URL + "/chartFolder_hidden/inactivate_allergy?id=allergies." + allergy_id)
        browser.getControl(name='note').value = "Curou a alergia"
        browser.getControl(name="form.button.inactivate").click()
    
    def create_allergy(self,PATIENT_ID,PATIENT_URL,allergy="Alergia a cigarro",reaction="Taquicardia",date=DateTime().Date()):
        portal = self.portal
        browser = self.browser
        
        # Entra e verifica o prontuario de um paciente alem de criar o chartFolder
        self.failUnless(self.verifyChartPatient(PATIENT_ID))
        browser.open(PATIENT_URL+"/chartFolder/show_allergies")
        
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
        
        browser.getControl(name='exam_form0').value = exam
        browser.getControl(name='value_form0').value = value
        browser.getControl(name='date_form0').value = date
        browser.getControl(name="form.button.save").click()
    
    def test_create_exam(self):
        print "\n::::Teste criar exames iniciou!" 
        portal = self.portal
        browser = self.browser
        login_as_admin(self)
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        print "As Manager"
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
        print "As Doctor"
        logout(self)
        login_as_doctor(self)
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
        
        
        print "::::Teste criar exames passou!\n" 
       
    
    def test_create_edit_inactivate_allergy(self):
        print "::::Teste criar alergias iniciou!\n" 
        portal = self.portal
        browser = self.browser
        login_as_admin(self)
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        print "As Manager"
        #Cria 3 alergias
        self.create_allergy(PATIENT_ID, PATIENT_URL)
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a cigarro" in browser.contents[browser.contents.find("<legend>Alergias Registradas</legend>"):])
        self.create_allergy(PATIENT_ID, PATIENT_URL,"Alergia a poeira")
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a poeira" in browser.contents[browser.contents.find("<legend>Alergias Registradas</legend>"):])
        self.create_allergy(PATIENT_ID, PATIENT_URL,"Alergia a flores")
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a flores" in browser.contents[browser.contents.find("<legend>Alergias Registradas</legend>"):])
        
        #Edit Alergia
        self.edit_allergy(PATIENT_ID,PATIENT_URL,old_allergy="Alergia a cigarro",new_allergy="Alergia a fumaca de cigarro")
        self.failUnless("Alergia a fumaca de cigarro" in browser.contents[browser.contents.find("<legend>Alergias Registradas</legend>"):])
        
        #Inativa alergia
        self.inactivate_allergy(PATIENT_ID,PATIENT_URL,allergy="Alergia a fumaca de cigarro")
        self.failUnless("Curou a alergia" in browser.contents)
        
        #As Doctor----------------------------------
        print "As Doctor"
        logout(self)
        login_as_doctor(self)
        #Cria 3 alergias
        self.create_allergy(PATIENT_ID, PATIENT_URL)
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a cigarro" in browser.contents[browser.contents.find("<legend>Alergias Registradas</legend>"):])
        self.create_allergy(PATIENT_ID, PATIENT_URL,"Alergia a poeira")
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a poeira" in browser.contents[browser.contents.find("<legend>Alergias Registradas</legend>"):])
        self.create_allergy(PATIENT_ID, PATIENT_URL,"Alergia a flores")
        self.failUnless("Alergia adicionada." in browser.contents)
        self.failUnless("Alergia a flores" in browser.contents[browser.contents.find("<legend>Alergias Registradas</legend>"):])
        
        #Edita alergia
        self.edit_allergy(PATIENT_ID,PATIENT_URL,old_allergy="Alergia a cigarro",new_allergy="Alergia a fumaca de cigarro")
        self.failUnless("Alergia a fumaca de cigarro" in browser.contents[browser.contents.find("<legend>Alergias Registradas</legend>"):])
        
        #Inativa alergia
        self.inactivate_allergy(PATIENT_ID,PATIENT_URL,allergy="Alergia a fumaca de cigarro")
        self.failUnless("Curou a alergia" in browser.contents)
        
        
        print "::::Teste criar alergias passou!\n" 
        
        
    
    def test_create_edit_resolve_problems(self):
        print "::::Teste criar, editar, resolver problemas iniciou!\n" 
        portal = self.portal
        browser = self.browser
        login_as_admin(self)
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        print "As Manager"
        print "Demora um bocado..."
        
        #Cria 3 problemas(um já resolvido), depois edita um mudando o status para resolvido, depois resolve outro diretamente.
        #Create problems
        self.create_problems(PATIENT_ID, PATIENT_URL)
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        self.create_problems(PATIENT_ID, PATIENT_URL,"Dor de cabeca")
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        self.failUnless("Dor de cabeca" in browser.contents)
        
        #Testa se "Dor de braço" dentro do fildset "Resolvidos" por causa do status "inactive"
        self.create_problems(PATIENT_ID, PATIENT_URL,"Dor de braço","456 7897")
        inicio = browser.contents.find('<legend> Ativos </legend>')
        self.failUnless("Dor de braço" in browser.contents[inicio:])
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        #Edit Problems
            #Edita a diarreia
        self.edit_problems(PATIENT_ID,PATIENT_URL,problem="Dor de dente")
        self.failUnless("Dor de dente" in browser.contents)
        #Resolve problem
            #Resolve dor de cabeça
        self.resolve_problems(PATIENT_ID,PATIENT_URL)
        self.failUnless("Nota editada resolvido" in browser.contents[browser.contents.find("Resolvidos"):])
        
        #As Doctor----------------------------------
        print "As Doctor"
        print "Demora um bocado tambem..."
        logout(self)
        login_as_doctor(self)
        #Cria 3 problemas(um já resolvido), depois edita um mudando o status para resolvido, depois resolve outro diretamente.
        #Create problems
        self.create_problems(PATIENT_ID, PATIENT_URL)
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        self.create_problems(PATIENT_ID, PATIENT_URL,"Dor de cabeca")
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        self.failUnless("Dor de cabeca" in browser.contents)
        
        #Testa se "Dor de braço" dentro do fildset "Resolvidos" por causa do status "inactive"
        self.create_problems(PATIENT_ID, PATIENT_URL,"Dor de braco","456 7897")
        inicio = browser.contents.find('<legend> Ativos </legend>')
        self.failUnless("Dor de braco" in browser.contents[inicio:])
        self.failUnless("Diagnóstico adicionado." in browser.contents)
        #Edit Problems
            #Edita a diarreia
        self.edit_problems(PATIENT_ID,PATIENT_URL,problem="Dor de mao")
        self.failUnless("Dor de mao" in browser.contents)
        #Resolve problem
            #Resolve dor de cabeça
        self.resolve_problems(PATIENT_ID,PATIENT_URL)
        self.failUnless("Nota editada resolvido" in browser.contents[browser.contents.find("Resolvidos"):])
        
        print "::::Teste criar, editar, resolver problemas passou!\n" 
        
        
        
    def test_create_edit_inactivate_medications_and_show_prescriptions(self):
        print "::::Teste criar, editar, inativar medicamentos e apresentar prescrições iniciou!\n" 
        portal = self.portal
        browser = self.browser
        login_as_admin(self)
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        print "As Manager"
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
        self.failUnless('id="pres_data"' in browser.contents)
        self.failUnless("CRM:" in browser.contents)
        #Visualize Prescription
        self.visualize_prescription(PATIENT_ID,PATIENT_URL)
        self.failUnless("CRM:" in browser.contents)
        self.failUnless('id="pres_data"' in browser.contents)
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
        print "As Doctor"
        logout(self)
        login_as_doctor(self)
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

        print "::::Teste criar, editar, inativar medicamentos e apresentar prescrições passou!\n" 
        
        
        
        
    def test_create_edit_document(self):
        print "::::Teste criar e editar documento iniciou!\n" 
        portal = self.portal
        browser = self.browser
        login_as_admin(self)
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        print "As Manager"
        #Create document
        document_id = self.create_document(PATIENT_ID, PATIENT_URL)
        self.failUnless("As alterações foram salvas." in browser.contents)
        self.failUnless("Criado por" in browser.contents)
        #Edit document
        self.edit_document(PATIENT_ID,PATIENT_URL,document_id)
        
        #As Doctor----------------------------------
        print "As Doctor"
        logout(self)
        login_as_doctor(self)
        #Create document
        document_id = self.create_document(PATIENT_ID, PATIENT_URL)
        self.failUnless("As alterações foram salvas." in browser.contents)
        self.failUnless("Criado por" in browser.contents)
        #Edit document
        self.edit_document(PATIENT_ID,PATIENT_URL,document_id)
        
        print "::::Teste criar e editar documento passou!\n" 
        
        
    def test_create_edit_impresso(self):
        print "::::Teste criar e editar impresso iniciou!\n" 
        portal = self.portal
        browser = self.browser
        login_as_admin(self)
        
        PATIENT_ID = "pteste"
        PATIENT_URL = portal.absolute_url() + "/Patients/" + PATIENT_ID
        
        #As Manager----------------------------------
        print "As Manager"
        #Create document
        impresso_id = self.create_impresso(PATIENT_ID, PATIENT_URL)
        self.failUnless("As alterações foram salvas." in browser.contents)
        self.failUnless("Criado por" in browser.contents)
        #Edit document
        self.edit_impresso(PATIENT_ID,PATIENT_URL,impresso_id)
        
        #As Doctor----------------------------------
        print "As Doctor"
        logout(self)
        login_as_doctor(self)
        #Create document
        impresso_id = self.create_impresso(PATIENT_ID, PATIENT_URL)
        self.failUnless("As alterações foram salvas." in browser.contents)
        self.failUnless("Criado por" in browser.contents)
        #Edit document
        self.edit_impresso(PATIENT_ID,PATIENT_URL,impresso_id)
        
        print "::::Teste criar e editar impresso passou!\n"
     

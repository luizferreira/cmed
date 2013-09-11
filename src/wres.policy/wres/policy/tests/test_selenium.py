#coding=utf-8
import Products.PloneTestCase.PloneTestCase
import gocept.selenium.tests.isolation
import gocept.selenium.zope2
import gocept.selenium.zope2.testing
import gocept.selenium.plone
from wres.policy.testing import WRES_POLICY_SELENIUM_FUNCTIONAL_TESTING
from wres.policy.test_browser_utils import Session
from Testing import ZopeTestCase
import gocept.selenium.plonetesting.testing_plone
from datetime import datetime

Products.PloneTestCase.PloneTestCase.setupPloneSite(id='plone')

wait_time = 3000
login_url = "/plone/login_form"

def wait(browser):
    browser.implicitly_wait(wait_time)

class Plone4Tests(gocept.selenium.plone.TestCase):

    layer = gocept.selenium.zope2.Layer(WRES_POLICY_SELENIUM_FUNCTIONAL_TESTING)

    def setUp(self):
		self.app =  WRES_POLICY_SELENIUM_FUNCTIONAL_TESTING["app"]
		self.portal = WRES_POLICY_SELENIUM_FUNCTIONAL_TESTING["portal"]
		ZopeTestCase.utils.setupCoreSessions(self.app)
		self.app.REQUEST["SESSION"] = Session()
		
    def test_create_documents(self):
        sel = self.selenium
        #   INICIA A INSTANCIA
        sel.open("/plone")
        # sel.click("id=personaltools-login")
        sel.waitForPageToLoad()
        #   LOGA COMO ADMIN
        sel.type("id=__ac_name", "admin")
        sel.type("id=__ac_password", "secret")
        sel.click("name=submit")
        sel.waitForPageToLoad()
        #   EXECUTA DEBUG_INIT
        sel.open("/plone/debug_init")
        # sel.waitForPageToLoad()
        #   SAI DO ADMIN E ENTRA COMO DTESTE
        sel.open("/plone")
        sel.waitForPageToLoad()
        sel.click("id=user-name")
        sel.click("link=Sair")
        sel.waitForPageToLoad()
        sel.type("id=__ac_name", "dteste")
        sel.type("id=__ac_password", "senha1")
        sel.click("name=submit")
        sel.waitForPageToLoad()
        #   ACESSA A ABA DE MODELOS
        sel.click('//*[@id="portaltab-Templates"]/a')
        sel.waitForPageToLoad()
        #   ADICIONA UM NOVO DOCUMENTO
        sel.click('id=add_Consultas')
        sel.waitForPageToLoad()
        sel.click('//*[@id="archetypes-fieldname-template_body"]/div[4]/div/div/a')
        sel.waitForPageToLoad()
        sel.type("name=title","Documento de Testes")
        sel.type("name=description","Descricao do documento de teste")
        sel.type("name=template_body","Conteudo de teste do documento")
        sel.click('//*[@id="template-base-edit"]/div[4]/input[7]')
        sel.waitForPageToLoad()
        #   TESTA O PROCESSO
        sel.assertTextPresent("Documento de Testes")
        sel.assertTextPresent("Descricao do documento de teste")
        sel.assertTextPresent("Conteudo de teste do documento")
        #   INICIA O TESTE DE ADICAO SOB O PACIENTE
        sel.open("/plone/Patients/pteste/chartFolder_hidden/documents")
        sel.waitForPageToLoad()
        sel.click("id=genericdocument")
        sel.waitForPageToLoad()
        #   ADICIONA O DOCUMENTO CRIADO PARA O PACIENTE TESTE
        sel.select("id=document_type", "label=Consulta")
        sel.type("name=medicalNote","Observacoes do Medico")
        sel.click("id=fieldsetlegend-corpo-do-documento")
        sel.pause(1000)
        sel.click("id=templates_button")
        sel.pause(1000)
        sel.select("id=template_select", "label=Documento de Testes")
        #   SALVA E TESTA
        sel.click("name=form.button.save")
        sel.waitForPageToLoad()
        sel.assertTextPresent("Paciente Teste")
        sel.assertTextPresent(u"As alterações foram salvas.")
        print "\nTeste criar documento concluido"

    def test_create_appointment(self):
        strBegin = strEnd = datetime.now().strftime("%Y-%m-%d")

        # Inicialização da instância e debug_init

        print "\nTeste criar consulta, SELENIUM, comecou"
        sel = self.selenium
        sel.open("/plone")
        sel.click("id=personaltools-login")
        sel.waitForPageToLoad()
        sel.type("id=__ac_name", "admin")
        sel.type("id=__ac_password", "secret")
        sel.click("name=submit")
        sel.waitForPageToLoad()
        sel.open("/plone/debug_init")
        sel.waitForPageToLoad()
        sel.open("/plone")
        sel.waitForPageToLoad()
        sel.click("id=user-name")
        sel.click("link=Sair")

        # Acesso à nova instância

        sel.waitForPageToLoad()
        sel.type("id=__ac_name", "dteste")
        sel.type("id=__ac_password", "senha1")
        sel.click("name=submit")
        sel.waitForPageToLoad()

        # Acessa calendário

        sel.click('//*[@id="portaltab-calendar"]/a')
        sel.waitForPageToLoad()
        calendarioLink = sel.getLocation()

        # Clica no campo referente à data de hoje, 13:30 às 13:45, e preenche formulários

        sel.open("/plone/Appointments/dteste/createSFEvent?startDate=%s+13:30&endDate=%s+13:45&type_name=Visit" % (strBegin,strEnd))        
        sel.waitForPageToLoad()

        # Preenche campo de busca pelo nome do paciente (já cadastrado) e seleciona os parametros da visita

        sel.type("id=searchGadget","pte")
        sel.pause(1000)
        sel.click("//a[@class='contenttype-patient']")
        sel.type("name=duration","25")
        sel.select("id=visit_type", "label=Consulta")
        sel.select("id=visit_reason", "label=Check up")
        sel.select("id=insurance", "label=Unimed")

        # Salva visita e verifica no calendário

        sel.click("name=form.button.save") 
        sel.open(calendarioLink)
        sel.waitForPageToLoad()
        sel.assertTextPresent("Paciente Teste")

        # Clica no campo referente à data de hoje, 13:45 às 14:00, e preenche formulários

        sel.open("/plone/Appointments/dteste/createSFEvent?startDate=%s+13:45&endDate=%s+14:00&type_name=Visit" % (strBegin,strEnd))        
        sel.waitForPageToLoad()

        # Preenche campo de busca pelo nome do paciente não cadastrado e click em 'Adicionar Novo Paciente'

        sel.type("id=searchGadget","car")
        sel.pause(1000)
        sel.click("//a[@class='link']")

        # Preenche dados principais do novo paciente e o registra

        sel.type("name=firstName","Paciente")
        sel.type("name=lastName","Teste2")
        sel.select('//*[@id="ahomePhone"]', "label=12")
        sel.type('//*[@id="archetypes-fieldname-homePhone"]/input[1]', "34567890")
        sel.select('//*[@id="amobile"]', "label=98")
        sel.type('//*[@id="archetypes-fieldname-mobile"]/input[1]', "76543210")
        sel.click('//*[@id="cphone_residencial"]')
        sel.click('id=registerButton')
        sel.pause(1000)

        # A partir do novo usuárui cadastrado, preenche os dados da visita

        sel.type("name=duration","25")
        sel.select("id=visit_type", "label=Consulta")
        sel.select("id=visit_reason", "label=Check up")
        sel.select("id=insurance", "label=Unimed")

        # Salva visita e verifica no calendário
        
        sel.click("name=form.button.save")
        sel.open(calendarioLink)
        sel.waitForPageToLoad()
        sel.assertTextPresent("Paciente Teste2")

        print "\nTeste criar consulta, SELENIUM, terminou"
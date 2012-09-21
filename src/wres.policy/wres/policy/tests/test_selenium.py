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
		
    def test_create_appointment(self):
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
        sel.waitForPageToLoad()
        sel.type("id=__ac_name", "dteste")
        sel.type("id=__ac_password", "senha1")
        sel.click("name=submit")
        sel.waitForPageToLoad()
        sel.click('//*[@id="portaltab-calendar"]/a')
        sel.waitForPageToLoad()
        sel.click('//*[@id="contentview-solgemafullcalendar_view"]/a')
        sel.waitForPageToLoad()
        sel.select("id=form-widgets-defaultCalendarView", u"value=basicWeek")
        sel.click('id=form-buttons-apply')
        sel.waitForPageToLoad()
        sel.mouseDownAt('//*[@id="calendar"]/div[1]/div/table/tbody/tr/td[3]','')
        sel.mouseUp('//*[@id="calendar"]/div[1]/div/table/tbody/tr/td[3]')
        print "\n------>Forced Sleep: 2000 ms to create iframe"
        sel.pause(2000)
        sel.selenium.select_frame("SFEventEditIFRAME")
        print "\n------>Forced Sleep: 1000 ms get search_patient buttom"
        sel.pause(1000)
        sel.click("id=popup_search_patient")
        #Go to child window
        sel.waitForPopUp("_blank")
        sel.selectPopUp()
        sel.type("id=searchGadget", "pte")
        print "\n------>Forced Sleep: 2000 ms to get ajax service"
        sel.pause(2000)
        #Precisa de um wait aqui!
        sel.click("class=contenttype-patient")
        #Back to parent window
        sel.selenium.select_window("null")
        sel.select("id=visit_reason", u"value=outro")
        sel.type("id=other_document_type", "Urgencia")
        sel.select("id=insurance", u"value=outro_plano")
        sel.type("id=other_insurance", "Salvador das Vidas")
        sel.click("name=form.button.save") 
        print "------>Forced Sleep: 1000 ms to back to parent iframe"
        sel.pause(1000)
        sel.assertTextPresent("Paciente Teste")
        print "\nTeste criar consulta, SELENIUM, terminou"
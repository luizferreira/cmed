from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD, SITE_OWNER_NAME, SITE_OWNER_PASSWORD
import unittest2 as unittest
from plone.testing.z2 import Browser
from plone.testing import z2
from plone.app.testing import setRoles

from Testing.ZopeTestCase.utils import  startZServer

from Products.CMFCore.utils import getToolByName


PW = "senha1"

def login_as_admin(self):
        # Go admin
        portal = self.portal
        browser = self.browser
        
        browser.open(portal.absolute_url() + "/login_form")
        browser.getControl(name='__ac_name').value = "admin"
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()
        browser.open(portal.absolute_url() + '/view')
        
        #Testa realmente se estou logado como admin
        inicio = browser.contents.find('id="user-name"')
        fim = inicio + browser.contents[inicio:].find("</a>")
        self.failUnless("admin" in browser.contents[inicio:fim])

def login_as_doctor(self):
        # Go admin
        portal = self.portal
        browser = self.browser
        browser.open(portal.absolute_url() + "/login_form")
        browser.getControl(name='__ac_name').value = "dteste"
        browser.getControl(name='__ac_password').value = PW
        browser.getControl(name='submit').click()
        
        #Testa realmente se estou logado como dteste
        inicio = browser.contents.find('id="user-name"')
        fim = inicio + browser.contents[inicio:].find("</a>")
        self.failUnless("DoutorTeste" in browser.contents[inicio:fim])

def login_as_secretary(self):
        # Go admin
        portal = self.portal
        browser = self.browser
        
        browser.open(portal.absolute_url() + "/login_form")
        browser.getControl(name='__ac_name').value = "steste"
        browser.getControl(name='__ac_password').value = PW
        browser.getControl(name='submit').click()
        browser.open(portal.absolute_url() + '/view')
        
        #Testa realmente se estou logado como steste
        inicio = browser.contents.find('id="user-name"')
        fim = inicio + browser.contents[inicio:].find("</a>")
        self.failUnless("SecretariaTeste" in browser.contents[inicio:fim])
    
def logout(self):
        browser = self.browser
        portal = self.portal
        
        browser.open(portal.absolute_url() + "/logout")

def create_members_by_debug_init(self,secs=1,pats=1,docs=1,admins=1,clins=1):
    browser = self.browser
    portal = self.portal
    login_as_admin(self)
    print "\nRunning debug_init for tests"
    #print "Criando " + str(secs) + " Secretarias, " + str(pats) + " Pacientes, " + str(docs) + " Doutores, " + str(admins) + " Administradores e " + str(clins) + " Clinicas."
    #browser.open(portal.absolute_url() + "/debug_init?pat="+str(pats)+"&doc="+str(docs)+"&sec="+str(secs)+"&adm="+str(admins)+"&cli="+str(clins)+"&full=1")
    browser.open(portal.absolute_url() + "/Templates/debug_init")
    logout(self)

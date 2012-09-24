#coding=utf-8
import unittest2 as unittest
from wres.archetypes.tests.IntegrationLayer import WRES_ARCHETYPES_INTEGRATION_TESTING
from wres.archetypes.content.chartdata import Event, ChartItemEventWrapper
from wres.archetypes.tests.utilsPatient import create_patient
from wres.policy.utils.utils import createVisitObject
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from DateTime import DateTime
from repoze.catalog.query import Eq

class TestSetup(unittest.TestCase):
    layer = WRES_ARCHETYPES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.pc = getToolByName(self.portal,"portal_catalog")
        self.cct = getToolByName(self.portal,"cmed_catalog_tool")
        self.pr = getToolByName(self.portal, 'portal_registration')
        
        #Set me as Manager
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        
        #Cria objetos para ser usado nos testes
        create_patient(self.portal,self.pr,"Peter","Parker")        
        query = self.pc.searchResults({'id':'pparker'})
        self.patient = query[0].getObject()
        
    #Classe Event
    def test___init__(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:__init__"
        print "Modulo: ContentChartData   Test:catalog_me"
        print "----------------------------------------------"
        #Get requirements
        ev = Event(self.patient, 1000, DateTime(), self.patient)
        self.assertTrue(self.cct.event_catalog.query(Eq('date', ev.date))[0])
        print "Done"

    def test_event_url(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:event_url"
        print "----------------------------------------------"
        #Get requirements
        ev = Event(self.patient, 1000, DateTime(), self.patient)
        parts = ev.event_url().split('/')
        self.assertTrue('Patients' in parts)
        self.assertTrue('pparker' in parts)
        print "Done"

    def test_eprint(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:eprint"
        print "Modulo: ContentChartData   Test:prefix"
        print "Modulo: ContentChartData   Test:posfix"
        print "Modulo: ContentChartData   Test:_author"
        print "----------------------------------------------"
        #Get requirements
        ev = Event(self.patient, 1000, DateTime(), self.patient)
        autor = ev._author()
        parts = ev.eprint().split(' ')
        self.assertTrue('href="/plone/Patients/pparker"' in parts)
        self.assertTrue('Paciente' in parts)
        self.assertTrue('adicionado.' in parts)
        self.assertTrue(autor, 'admin')
        print "Done"

    def test_event_cmp(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:_event_cmp"
        print "----------------------------------------------"
        #Get requirements
        ev = Event(self.patient, 1000, DateTime(), self.patient)
        ev2 = Event(self.patient, 1000, DateTime()+1, self.patient)
        result = ev._event_cmp(ev2)
        self.assertEqual(result, -1)
        print "Done"

    def test_visit_review_state(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:_visit_review_state"
        print "----------------------------------------------"
        #Get requirements
        visit = createVisitObject(self.portal, 'teste')
        visit.reindexObject()
        ev = Event(visit, 1000, DateTime(), visit)
        result = ev._visit_review_state()
        self.assertEqual(result, ' (nao agendada).')
        print "Done"

    #Classe ChartItemEventWrapper
    def test_ChartItemEventWrapper(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:ChartItemEventWrapper"
        print "----------------------------------------------"
        #Get requirements
        cw = ChartItemEventWrapper('problems', self.patient, **{'problem': 'teste'})
        self.assertEqual(cw.getId(), 'pparker_problems_teste')
        self.assertEqual(cw.Title(), 'teste')
        parts = cw.absolute_url_path().split('/')
        self.assertTrue('Patients' in parts)
        self.assertTrue('pparker' in parts)
        self.assertTrue('show_problem_list' in parts)
        print "Done"
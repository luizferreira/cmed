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
        ev = Event(self.patient, Event.CREATION, DateTime(), self.patient)
        self.assertTrue(self.cct.event_catalog.query(Eq('date', ev.date))[0])
        print "Done"

    def test_event_url(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:event_url"
        print "----------------------------------------------"
        #Get requirements
        ev = Event(self.patient, Event.CREATION, DateTime(), self.patient)
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
        ev = Event(self.patient, Event.CREATION, DateTime(), self.patient)
        parts = ev.eprint().split(' ')
        self.assertTrue('href="/plone/Patients/pparker">' in parts)
        self.assertTrue('Paciente' in parts)
        self.assertTrue('adicionado.' in parts)
        print "Done"

    def test_event_cmp(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:_event_cmp"
        print "----------------------------------------------"
        #Get requirements
        ev = Event(self.patient, Event.CREATION, DateTime(), self.patient)
        ev2 = Event(self.patient, Event.CREATION, DateTime()+1, self.patient)
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
        ev = Event(visit, Event.CREATION, DateTime(), visit)
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
        pat = cw.patient
        self.assertTrue('pparker' == pat.getId())
        self.assertTrue('/show_problem_list' == cw.url_sufix)
        print "Done"

    #Classe ChartData
    def test_ChartData(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:__init__"
        print "Modulo: ContentChartData   Test:clean_chart"
        print "Modulo: ContentChartData   Test:update_chart"
        print "----------------------------------------------"
        #Get requirements
        self.assertTrue(self.patient.chart_data)
        self.patient.create_event(Event.CREATION, DateTime(), self.patient)
        self.assertTrue(self.patient.get_events()) #init
        self.patient.chart_data.clean_chart()
        self.assertFalse(self.patient.get_events()) #clean
        del self.patient.chart_data.events
        self.assertFalse(hasattr(self.patient.chart_data, 'events'))
        self.patient.chart_data.update_chart()
        self.patient.create_event(Event.CREATION, DateTime(), self.patient)
        self.assertTrue(dict(self.patient.chart_data.events)) #update
        print "Done"

    def test_raise_event(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:raise_event"
        print "----------------------------------------------"
        #Get requirements
        patient = self.patient
        patient.chart_data.clean_chart()
        medication = {'status': 'active', 'submitted_by': 'admin', 'use': '1 cp quando houver do de cabe\xc3\xa7a', 'medication': 'Tylenol dc', 'end_date': DateTime('2012/05/07 17:06:14.061165 GMT-3'), 'note': '', 'start': '07/05/2012', 'concentration': '80mg', 'quantity': '12'}
        patient.chart_data.raise_event(patient, 'medications', Event.CREATION, **medication)
        self.assertTrue(dict(self.patient.chart_data.events))
        print "Done"

    def test_manage_data(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentChartData   Test:save_entry"
        print "Modulo: ContentChartData   Test:edit_entry"
        print "Modulo: ContentChartData   Test:get_entry"
        print "Modulo: ContentChartData   Test:get_entry_item"
        print "----------------------------------------------"
        #Get requirements
        patient = self.patient
        patient.chart_data.clean_chart()
        medication = {'status': 'active', 'submitted_by': 'admin', 'use': '1 cp quando houver do de cabe\xc3\xa7a', 'medication': 'Tylenol dc', 'end_date': DateTime('2012/05/07 17:06:14.061165 GMT-3'), 'note': '', 'start': '07/05/2012', 'concentration': '80mg', 'quantity': '12'}
        med_id = patient.chart_data.save_entry(patient, 'medications', **medication)
        self.assertTrue(dict(self.patient.chart_data.medications)) #save_entry
        medication['submitted_by'] = 'pparker'
        patient.chart_data.edit_entry(med_id, 'medications', **medication)
        saved_med = patient.chart_data.get_entry_item(med_id, 'medications')
        self.assertTrue(saved_med) #get_enty_item
        self.assertEqual(saved_med['submitted_by'], 'pparker') #edit_entry
        patient.chart_data.save_entry(patient, 'medications', **medication)
        patient.chart_data.save_entry(patient, 'medications', **medication)
        all_med = patient.chart_data.get_entry('medications')
        self.assertEqual(len(all_med), 3) #get_entry
        print "Done"
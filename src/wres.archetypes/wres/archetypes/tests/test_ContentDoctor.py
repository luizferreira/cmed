#coding=utf-8
import unittest2 as unittest
from wres.archetypes.tests.IntegrationLayer import WRES_ARCHETYPES_INTEGRATION_TESTING
from wres.archetypes.tests.utilsDoctor import create_doctor
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from wres.policy.utils.roles import DOCTOR_GROUP

class TestSetup(unittest.TestCase):
    layer = WRES_ARCHETYPES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.pc = getToolByName(self.portal,"portal_catalog")
        self.pr = getToolByName(self.portal, 'portal_registration')
        
        #Set me as Manager
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        
        #Cria um médico para ser usado nos testes 
        create_doctor(self.portal,self.pr,"Dr. Victor","Frankenstein")        
        
        #Make patient easy to access
        query = self.pc.searchResults({'id':'dfrankenstein'})
        self.doctor = query[0].getObject()
        
    def test_add_visits_folder(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:add_visits_folder"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        self.assertTrue(getattr(self.portal.Appointments, self.doctor.getId()))
        print "Done"

    def test_at_post_create_script(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:at_post_create_script"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        pm = getToolByName(self.portal, 'portal_membership')
        self.assertTrue(pm.getMemberById(doctor.getId()))
        #Check if DR. VICTOR becomes Dr.Victor
        self.assertEqual(doctor.getFullName(), 'Dr. Victor Frankenstein')
        print "Done"

    def test_at_post_edit_script(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:at_post_edit_script"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        doctor.setFirstName('DR. VICTOR')
        doctor.at_post_edit_script()
        self.assertEqual(doctor.getFullName(), 'Dr. Victor Frankenstein')
        print "Done"

    def test_getGroup(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:getGroup"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        self.assertTrue(doctor.getGroup(), DOCTOR_GROUP)
        print "Done"

    def test_Title(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:Title"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        self.assertEqual(doctor.getFullName(), doctor.Title())
        print "Done"

    def test_asc2title(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:asc2title"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        doctor.setLastName('Frankénsteín')
        self.assertEqual(doctor.asc2title(), 'Dr. Victor Frankenstein')
        print "Done"

    def test_get_home_url(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:get_home_url"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        parts = doctor.get_home_url().split('/')
        self.assertTrue('Appointments' in parts)
        self.assertTrue('sec_desk' in parts)
        print "Done"

    def test_getAppointmentsURL(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:getAppointmentsURL"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        parts = doctor.getAppointmentsURL().split('/')
        self.assertTrue('Appointments' in parts)
        self.assertTrue(doctor.getId() in parts)
        self.assertTrue('Agenda' in parts)
        print "Done"

    def test_validateSignPassword(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:validateSignPassword"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        self.assertTrue(doctor.validateSignPassword('senha1'))
        print "Done"

    def test_getCourseTypes(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:getCourseTypes"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        clist = doctor.getCourseTypes()
        for item in clist:
            self.assertTrue(item in ['college', 'specialization'])
        print "Done"

    def test_getSchemaFields(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:getSchemaFields"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor
        sfields = doctor.getSchemaFields()
        self.assertEqual(sfields, doctor.schema.fields())
        print "Done"

    def test_fillFirstDoctorInfo(self):
        print "\n"
        print "----------------------------------------------"
        print "Modulo: ContentDoctor   Test:fillFirstDoctorInfo"
        print "----------------------------------------------"
        #Get requirements
        doctor = self.doctor

        info = {
            'doctor_firstName': 'Dráuzio',
            'doctor_lastName': 'Varela',
            'doctor_ssn': '012302301',
            'doctor_phone': '3133334444',
            'doctor_email': 'aa@aa.com',
            'doctor_email_conf': 'aa@aa.com',
            'doctor_especialty1': 'cardiology',
            'doctor_especialty2': 'internal'
        }
        doctor.fillFirstDoctorInfo(info)
        self.assertEqual(doctor.getFullName(), 'Dráuzio Varela')
        self.assertEqual(doctor.getSsn(), '012302301')
        print "Done"
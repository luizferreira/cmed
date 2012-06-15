# coding=utf-8

"""Definition of the Patient content type
"""
from DateTime import DateTime
from AccessControl import ClassSecurityInfo

import json

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from ComputedAttribute import ComputedAttribute

from wres.archetypes.interfaces import IPatient
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.archetypes.content.chartdata import ChartData #,Prescription, Maintenance, Note, Problem 
from wres.archetypes.content.schemas.patient import PatientSchema

from wres.policy.utils.roles import *

schemata.finalizeATCTSchema(
    PatientSchema,
    folderish=True,
    moveDiscussion=False
)

class Patient(wresuser.WRESUser):
    """Patient type for WRES website"""
    implements(IPatient)

    meta_type = "Patient"
    schema = PatientSchema

    security = ClassSecurityInfo()
    
    def SearchableText(self):
        pid = self.getId()
        cpf = self.getSocialSecurity()
        fullname = self.getFullName()
        return [pid, cpf, fullname]

    # retorna um objeto do tipo json (JavaScript Object Notation),
    # utilizado no tipo visita (BuildingBlocksWidget)
    def getInformation(self):
        return json.dumps({'getLastVisitDate': self.getLastVisitDate(), 'getContactPhone': self.getContactPhone(), 'UID': self.UID()})
        
    def getGroup(self):
        return PATIENT_GROUP

    def createHiddenKey(self, key):
        return key + '_hidden'

    def existSubObject(self, key):
        hidden_key = self.createHiddenKey(key)
        return hasattr(self, hidden_key)

    def createChartFolder(self, id):
        from wres.archetypes.content.chartfolder import addChartFolder
        addChartFolder(self, id=id, title='Chart Folder')

    def createMissingObject(self, key):
        hidden_key = self.createHiddenKey(key)
        if not self.existSubObject(key):
            if key == 'chartFolder':
                self.createChartFolder(hidden_key)
#            elif key == 'casesFolder':
#                self.createCasesFolder(hidden_key)
        return hidden_key

    def _getSubObject(self, key):
        hidden_key = self.createHiddenKey(key)
        if not self.existSubObject(key):
            self.createMissingObject(key)
#        obs: esse trecho considera que essa função será utilizada
#        apenas para objetos chartFolder.
        chart = getattr(self, hidden_key)
        chart.setTitle('Prontuário')
        return chart
    
    def chartFolder(self):
        """ """
        return self._getSubObject('chartFolder')
    
    chartFolder = ComputedAttribute(chartFolder, 1)
    
    #def getEncounters(self):
        #pc = self.portal_catalog
        #chart_folder = self.chartFolder
        #brains = pc.search({'meta_type': 'Encounter',
                            #'path': '/'.join(chart_folder.getPhysicalPath()),
                            #})
        #encounters = [b.getObject() for b in brains]
        #encounters = [e for e in encounters if e.getDate_of_visit() is not None]
        #return encounters

#    def getRetirementdate(self):
#        field = self.getField('retirementdate')
#        value = field.get(self)
#        if type(value) == type(u'unicode'):
#            self.setRetirementdate(value)
#            value = field.get(self)
#        return value


#    as duas funcoes abaixo sao necessarias no tipo Visit.
    security.declarePublic('getLastVisitDate')
    def getLastVisitDate(self, strftime='%d/%m/%Y'):
        """ """
        if not hasattr(self, 'lastVisitDate'):
            return 'No visits concluded'
        else:
            return self.lastVisitDate.strftime(strftime)

    security.declarePublic('setLastVisitDate')
    def setLastVisitDate(self, date):
        """ """
        self.lastVisitDate = date

    def Title(self):
        """ """
        if self.getFirstName() == '':
            return 'Sem Nome'
        else:
            return '%s %s' %(self.getFirstName(),
                             self.getLastName(),
                            )

    def lower_title(self):
        """ self.Title().lower() """
        return self.Title().lower()

#    def getInsuranceData(self):
#        case = self.getInsurance()
#        if case:
#            insurances = [policy.getInsurance() for policy in case.objectValues()]
#        else:
#            insurances = []
#        return insurances

#    def manage_beforeDelete(self, item, container):
#        brefs = item.getBRefs('patient')
#
#        for bref in brefs:
#            parent = bref.aq_parent
#            parent.manage_delObjects([bref.id])
#
#        wresuser.manage_beforeDelete(self, item, container)

#    def at_post_edit_script(self):
#        wresuser.at_post_create_script(self)
#        self.updateRelatedVisits()

    def at_post_create_script(self):
        wresuser.WRESUser.at_post_create_script(self)
#        self.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE], acquire = False)
#        self.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE], #acquire = False)
#        self.reindexObject()

#    def updateRelatedVisits(self):
#        visit_list = []
#        visit_list = self.getBRefs('patient')
#        for visit in visit_list:
#            visit_state = self.portal_workflow.getInfoFor(visit, 'review_state', '')
#            if  visit_state != 'concluded' and visit_state != 'canceled':
#                visit.setContactPhone(self.getContactPhone())
#                visit.reindexObject(idxs='getContactPhone')

    #the 3 functions bellow are needed to create a patient user
    def getFullName(self):
        return self.Title()

    def get_home_url(self):
        return self.absolute_url_path() + '/patient_desktop_view'

    #security.declareProtected(VIEW_PATIENT, 'questionnaire_filled')
#    def questionnaire_filled(self):
#        """ return true if questionnarie has been filled."""
#        if not hasattr(self, '_questionnaire_filled'):
#            return False
#        return self._questionnaire_filled
        
    #security.declareProtected(EDIT_PATIENT, 'set_questionnaire_filled')
#    def set_questionnaire_filled(self):
#        """ mark questionnaire as filled."""
#        self._questionnaire_filled = True

#    def fill_questionnaire(self, dict):
#        """ fill the questionnaire """
#        self.chart_data.questionnaire.update(dict.items())

#    def questionnaire_data(self):
#        result = {}
#        questionnaire = self.chart_data.questionnaire
#        for key in questionnaire.keys():
#            result[key] = questionnaire[key]
#        return result

    def __create_chart_data(self):
        clean_self = self.aq_base
        if not hasattr(clean_self, 'chart_data_hidden'):
            self.chart_data_hidden = ChartData()
            self._p_changed = 1
        return self.chart_data_hidden
    chart_data = ComputedAttribute(__create_chart_data, 1)

#    def distribute_questionnaire(self, data=None):
#        self.chart_data.distribute_questionnaire(data)

#    def cleanChartData(self):
#        self.chart_data.clean_chart()

#    def updateChartData(self):
#        self.chart_data.update_chart()

    #def getFamilyHistory(self):
        #return dict(self.chart_data.family_history)

    #def getPastMedicalHistory(self):
        #return dict(self.chart_data.past_medical_history)

    # def getAllergies(self):
    #     return dict(self.chart_data.allergies)
        
    #def getLaboratory(self):
        #return [dict(value) for value in self.chart_data.laboratory.values()]

    #def getNotSignedAllergies(self):
        #return dict(self.chart_data.not_signed_allergies)

    #def getMedications(self):
        #return dict(self.chart_data.medications)

    #def getTests(self):
        #return dict(self.chart_data.tests)

    #def getImmunizations(self):
        #return dict(self.chart_data.immunizations)

    #def getReviewOfSystems(self):
        #return dict(self.chart_data.review_of_systems)

    #def getSocialHistory(self):
        #return dict(self.chart_data.social_history)

    #def getFollowUpNotes(self):
        #return [value for value in self.chart_data.follow_up_notes.values()]

    #def getVitalSigns(self):
        #return [dict(value) for value in self.chart_data.vital_signs.values()]

    # metodo utilizado apenas no debug_patientchartdata
    def get_chart_data_map(self):
        return ChartData.mapping
        

    def chart_data_summary(self):
        '''
        method used in migration and in debug_patientchartdata.
        just return the chart_data in format of dictionaries.
        '''
        keys = ['review_of_systems', 'medications', 'prescriptions', 
        'allergies', 'problems', 'not_signed_allergies', 'laboratory']

        dic_chartdata = {}
        dic_chartdata['allergies'] = dict(self.chart_data.allergies)
        dic_chartdata['review_of_systems'] = dict(self.chart_data.review_of_systems)
        dic_chartdata['medications'] = dict(self.chart_data.medications)
        dic_chartdata['prescriptions'] = dict(self.chart_data.prescriptions)
        dic_chartdata['problems'] = dict(self.chart_data.problems)
        dic_chartdata['not_signed_allergies'] = dict(self.chart_data.not_signed_allergies)
        dic_chartdata['laboratory'] = dict(self.chart_data.laboratory)
        return dic_chartdata

    def import_chartdata(self, chart_dic):
        '''
        used exclusively in migration. 
        '''
        from BTrees.OOBTree import OOBTree
        keys = ['review_of_systems', 'medications', 'prescriptions', 
        'allergies', 'problems', 'not_signed_allergies', 'laboratory']

        for key in self.chart_data.mapping.keys():
            setattr( self.chart_data, key, OOBTree(chart_dic[key]) )

#    def saveMaintenance(self, **maintenance):
#        maints = self.chart_data.maintenances
#        new_maintenance = Maintenance(**maintenance)
#        maints[new_maintenance.maintenance] = new_maintenance

#    def editMaintenance(self, **data):
#        maintenance = data['maintenance']
#        maints = self.chart_data.maintenances
#        maint = maints[maintenance]
#        maint.due_by = data['due_by']
#        maint.recommended_for = data['recommended_for']
#        encounters = data.get('encounters', None)
#        if encounters is not None:
#            maint.encounters = encounters
#        maints[maintenance] = maint

#    def completeMaintenance(self, maintenance):
#        maints = self.chart_data.maintenances
#        maint = maints[maintenance]
#        maint.state = 'historical'
#        maints[maintenance] = maint

#    def getMaintenance(self, maintenance):
#        maints = self.chart_data.maintenances
#        maint = maints[maintenance]
#        return maint.toDict()

#    security.declarePublic('getMaintenances')
    #def getMaintenances(self):
        #""" """
        #maints = self.chart_data.maintenances.values()
        #return [maint.toDict() for maint in maints]

#    def saveNote(self, **note):
#        notes = self.chart_data.notes
#        new_note = Note(**note)
#        notes[new_note.id] = new_note

#    def editNote(self, **data):
#        note_id = data['id']
#        notes = self.chart_data.notes
#        note = notes[note_id]
#        for key, value in data.items():
#            if hasattr(note, key):
#                setattr(note, key, value)
#        notes[note_id] = note

    #def saveAllergy(self, **allergy):
        #allergies = self.chart_data.allergies
        #entry = {'date': DateTime(), 'came_from': 'template'}
        #id = self.generateUniqueId('Allergy')
        #entry['id'] = id
        #allergy['id'] = id
        #entry['data'] = allergy
        #allergies[id] = entry
    
    #def saveLaboratory(self,**exam):
        #exams = self.chart_data.laboratory
        #entry = {'date':DateTime(),'came_from':'template'}
        #id = self.generateUniqueId('Exam')
        #entry['id'] = id
        #exam['id'] = id
        #entry['data'] = exam
        #exams[id] = entry

    #def getNotes(self):
        #notes = self.chart_data.notes.values()
        #return [note.toDict() for note in notes]

    #def saveProblem(self, **problem):
        #problems = self.chart_data.problems
        #entry = {'date': DateTime(), 'came_from': 'template'}
        #id = self.generateUniqueId('Problem')
        #entry['id'] = id
        #problem['id'] = id
        #entry['data'] = problem
        #problems[id] = entry

    #def editProblem(self, id, **data):
        #problem_id = id
        #problems = self.chart_data.problems
        #problem = problems[problem_id]
        #for key, value in data.items():
            #problem[key] = value
        #problems[problem_id] = problem
    
    #def getProblems(self):
        #problems = self.chart_data.problems.values()
        #return [problem for problem in problems]

    #def getProblem(self, id):
        #problems = self.chart_data.problems
        #problem = problems[id]
        #if 'state' not in problem.keys():
            #problem['state'] = 'active'
        #return problems[id]
        
    #def saveMedication(self, **medication):
        #medications = self.chart_data.medications
        #entry = {'date': DateTime(), 'came_from': 'template'}
        #id = self.generateUniqueId('Medication')
        #medication['id'] = id
        #entry['id'] = id
        #entry['data'] = medication
        #medications[id] = entry
        
    #def editMedication(self, id, **data):
        #medication_id = id
        #medications = self.chart_data.medications
        #medication = medications[medication_id]
        #for key, value in data.items():
            #medication[key] = value
        #medications[medication_id] = medication
        
    #def getMedication(self, id):
        #medications = self.chart_data.medications
        #medication = medications[id]
        #return medication

    #def savePrescription(self, **prescription):
        #prescriptions = self.chart_data.prescriptions
        #entry = {}
        #id = self.generateUniqueId('Prescription')
        #prescription['id'] = id
        #entry['id'] = id
        #entry['data'] = prescription
        #prescriptions[id] = entry
        #return id

    #def editPrescription(self, id, **data):
        #prescription_id = id
        #prescriptions = self.chart_data.prescriptions
        #prescription = prescriptions[prescription_id]
        #for key, value in data.items():
            #if hasattr(prescription, key):
                #setattr(prescription, key, value)
        #prescriptions[prescription_id] = prescription

    #def getPrescriptions(self, ids=None):
        #prescriptions = self.chart_data.prescriptions.values()
        #return [prescription for prescription in prescriptions]

    #def getPrescription(self, id):
        #prescriptions = self.chart_data.prescriptions
        #return prescriptions[id]

#    def special_fields(self, key):
#        dict = {'main_information': ['chart', 'confirmedChartNumber',
#                                     'firstName', 'lastName',
#                                     'socialSecurity', 'identidade', 'orgaoEmissor',
#                                     'birthDate', 'sex',
#                                     'type_of_patient', 'primaryDoctor',
#                                     'referredBy', 'nomeDoPai', 'nomeDaMae', 
#                                     'cartaoNacionalDeSaude',],
#                'contact_information': ['address1', 'address2', 'city', 'state',
#                                        'nacionalidade', 'zipCode', 'homePhone', 'contactPhone',
#                                        'ext', 'mobile', 'email'],
#                }
#        if key == 'guarantor_information':
#            return self.guarantor_special_fields()
#        else:
#            schema = self.Schema()
#            fields = [schema.getField(field_id) for field_id in dict[key]]
#            return fields
#    def guarantor_special_fields(self):
#        if self.getIsGuarantor():
#            return [GUARANTOR.get('isGuarantor')]
#        else:
#            return GUARANTOR.fields()

#    def break_in_groups(self, fields):
#        def visible(field):
#            return (field.widget.isVisible(self) == 'visible')
#        filtered = [field for field in fields if visible(field)]
#        size = 3
#        position = 0
#        groups = []
#        while position < len(filtered):
#            groups.append(filtered[position:position + size])
#            position += size
#        return groups

#    def validate_birthDate(self, value):
#        request = self.REQUEST
#        birth_string = request.get('visible_birthDate')
#        birthDate = self.Schema().getField('birthDate')
#        if birth_string and not value:
#            return "Please correct the date format"
#        return None

#    def isIdIncoherent(self):
#        id = self.getId()
#        if id == 'dummy_patient':
#            return False
#        return wresuser.isIdIncoherent(self)

#def modify_fti(fti):
    # hide unnecessary tabs (usability enhancement)
#    for a in fti['actions']:
#        if a['id'] not in ('view', 'edit', 'quest', 'insurance_policy',\
#                           'add_patient'):
#            a['visible'] = 0
#    return fti 

atapi.registerType(Patient, PROJECTNAME)

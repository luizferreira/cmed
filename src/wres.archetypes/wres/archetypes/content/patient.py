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
        return json.dumps({'getLastDate': self.getLastVisitDate(), 'getContactPhone': self.getContactPhone(), 'UID': self.UID()})
        
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

    def at_post_create_script(self):
        wresuser.WRESUser.at_post_create_script(self)
        
    def at_post_edit_script(self):
        wresuser.WRESUser.at_post_edit_script(self)


    #the 3 functions bellow are needed to create a patient user
    def getFullName(self):
        return self.Title()

    def get_home_url(self):
        return self.absolute_url_path() + '/patient_desktop_view'

    def __create_chart_data(self):
        clean_self = self.aq_base
        if not hasattr(clean_self, 'chart_data_hidden'):
            self.chart_data_hidden = ChartData()
            self._p_changed = 1
        return self.chart_data_hidden
    chart_data = ComputedAttribute(__create_chart_data, 1)

#        # metodo utilizado apenas no debug_patientchartdata
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

atapi.registerType(Patient, PROJECTNAME)

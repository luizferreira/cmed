# coding=utf-8

"""Definition of the Patient content type
"""
from datetime import date
from AccessControl import ClassSecurityInfo
from DateTime import DateTime

import json

from zope.interface import implements
from zope.app.component.hooks import getSite

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata

from ComputedAttribute import ComputedAttribute

from wres.archetypes.interfaces import IPatient
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content import wresuser
from wres.archetypes.content.chartdata import ChartData, Event #,Prescription, Maintenance, Note, Problem
from wres.archetypes.content.schemas.patient import PatientSchema
from Products.CMFCore.utils import getToolByName

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

    def genericColumn1(self):
        """
        genericColumn1 é uma metadata column de propósitos gerais
        """
        return self.getBirthDate()

    def genericColumn2(self):
        """
        genericColumn2 é uma metadata column de propósitos gerais
        """
        return self.getContactPhone()

    def addInsurance(self):
        """
        Verifica se o convênio preenchido já existe no vocabulário. Caso não
        exista, o mesmo é adicionado.
        """
        new_insurance = self.getInsurance()
        dl = self.getInsurancesNames()
        if new_insurance not in dl:
            portal = getSite()
            vt = getToolByName(portal, 'vocabulary_tool')
            vt.add2vocabulary('insurance', new_insurance, 1, 1)

    def SearchableText(self):
        """
        Returns strings that can be searched by the SearchableText catalog index.
        Example input:
            pid = jsilva, cpf = 0123456790, fullname = Joao Silva
        Example output:
            ['jsilva', '0123456789', 'Joao Silva']
        """
        pid = self.getId()
        cpf = self.getSocialSecurity()
        fullname = self.getFullName()
        return [pid, cpf, fullname]

    def getInformation(self):
        """
        Retorna um objeto do tipo json (JavaScript Object Notation).
        Utilizado no tipo visita
        """
        return json.dumps({
            'UID': self.UID(),
            'fullName': "%s (%s)" % (self.getFullName(), self.getLastVisitDate()),
            'getContactPhone': self.getContactPhone(),
            'getInsurance': self.getInsurance(),
        })

    def getInsurancesNames(self):
        """
        Consulta vocabulário de convênios e retorna a lista.
        """
        dl = atapi.DisplayList()
        dl.add('', '')
        portal = getSite()
        vt = getToolByName(portal, 'vocabulary_tool')
        vocab_list = vt.get_vocabulary('insurance', 2)
        for vocab in vocab_list:
            dl.add(vocab, vocab)
        dl.add('outro_plano', 'Outro')
        return dl

    def getGroup(self):
        """
        Return patient group: "Patient"
        """
        return PATIENT_GROUP

    def createHiddenKey(self, key):
        """
        Return string: key + '_hidden'
        """
        return key + '_hidden'

    def existSubObject(self, key):
        """
        Sees if patient has hidden atributes of the key: key+"_hidden"
        """
        hidden_key = self.createHiddenKey(key)
        return hasattr(self, hidden_key)

    def createChartFolder(self, id):
        """
        Create chart folder in patient.
        After execute:
        all_chartfolder = id list of all chartfolders indexed in system
        assertTrue("documents" in all_chartfolders)     assertTrue("impressos" in all_chartfolders)
        assertTrue("exams" in all_chartfolders)         assertTrue("upload" in all_chartfolders)
        """
        from wres.archetypes.content.chartfolder import addChartFolder
        addChartFolder(self, id=id, title='Chart Folder')

    def createMissingObject(self, key):
        """
        Create object "key" if it doesn't exists
        Obs: Nome fantasia, só funciona para chartFolder
        """
        hidden_key = self.createHiddenKey(key)
        if not self.existSubObject(key):
            if key == 'chartFolder':
                self.createChartFolder(hidden_key)
#            elif key == 'casesFolder':
#                self.createCasesFolder(hidden_key)
        return hidden_key

    def _getSubObject(self, key):
        """
        Return patient's chartFolder (if it doen't exists, chartFolder is created')
        Obs: Nome fantasia, só funciona para chartFolder
        """
        hidden_key = self.createHiddenKey(key)
        if not self.existSubObject(key):
            self.createMissingObject(key)
#        obs: esse trecho considera que essa função será utilizada
#        apenas para objetos chartFolder.
        chart = getattr(self, hidden_key)
        chart.setTitle('Prontuário')
        return chart

    def chartFolder(self):
        """
        Just create the function used by ComputedAttribute() to create chartFolder attribute.
        """
        return self._getSubObject('chartFolder')
    chartFolder = ComputedAttribute(chartFolder, 1)

    def initChart(self):
        """
        Inicializa chartFolder_hidden e redireciona para o mesmo.
        É a maneira correta de acessar o prontuário, caso não se tenha certeza
        que ele já foi criado.
        """
        chart = self._getSubObject('chartFolder')
        return self.REQUEST.response.redirect('/'.join(chart.getPhysicalPath()), 301)

#    as duas funcoes abaixo sao necessarias no tipo Visit.
    security.declarePublic('getLastVisitDate')
    def getLastVisitDate(self, strftime='%d/%m/%Y'):
        """
        Return the patient's attribute: lastVisitDate in %d/%m/%Y
        If it not exists return "Nenhuma visita concluída anteriormente"
        """
        if not hasattr(self, 'lastVisitDate'):
            return "Nenhuma visita concluída anteriormente"
        else:
            return "Última visita: %s" % self.lastVisitDate.strftime(strftime)

    security.declarePublic('setLastVisitDate')
    def setLastVisitDate(self, date):
        """
        Just set the patient's attribute: lastVisitDate
        Obs: O parametro "date" precisar possuir a funcao strftime()
        """
        self.lastVisitDate = date
        if not hasattr(date, "strftime"):
            raise ValueError("Tipo de data invalida")

    def Title(self):
        """
        If patient.firstName = 'Joao' and patient.lastName = 'Silva'
        This function will return 'Joao Silva'
        If it doesn't has a first and a last name, the function will return "Sem Nome"
        """
        if self.getFirstName() == '' and self.getLastName() == '':
            return 'Sem Nome'
        else:
            return '%s %s' %(self.getFirstName(),
                             self.getLastName(),
                            )

    def lower_title(self):
        """
        Return all patient.Title() letters in lower case.
        """
        return self.Title().lower()

    def setPatientChartSystemID(self):
        """
        Set auto-increment chartSystemID field
        """
        patientFolder = self.getParentNode()
        nextChartSystemID = patientFolder.getLastChartSystemID() + 1
        self.setChartSystemID(nextChartSystemID)
        patientFolder.setLastChartSystemID(nextChartSystemID)

    def at_post_create_script(self):
        """
        Create evente about patient creation
        Set chartSystemID
        Execute WRESUser.at_post_create_script(), basically register
        the patient object as portal member
        """
        self.create_event(Event.CREATION, self.created(), self)
        self.setPatientChartSystemID()
        #lastChartSystemID = self.getParentNode().getLastChartSystem
        wresuser.WRESUser.at_post_create_script(self)
        self.setReaderLocalRole()

    def at_post_edit_script(self):
        """
        Just execute WRESUser.at_post_edit_script(), basically if the patient
        name was changed, the name will be formated.
        """
        wresuser.WRESUser.at_post_edit_script(self)
        self.reindexVisits() # atualize o Title das visitas caso necessário
        self.addInsurance()  # verifica se o convênio preenchido já existe no vocab


    #the 3 functions bellow are needed to create a patient user
    def getFullName(self):
        """
        See self.Title() documentation
        """
        return self.Title()

    def get_home_url(self):
        """
        Concatenate the patient url with "/patient_desktop_view"
        """
        #TODO: Seria mais otimizado se get_home_url fosse um atributo
        return '/'.join(self.getPhysicalPath()) 
        
    def __create_chart_data(self):
        """
        Create chart_data_hidden attribute
        """
        clean_self = self.aq_base
        if not hasattr(clean_self, 'chart_data_hidden'):
            self.chart_data_hidden = ChartData()
            self._p_changed = 1
        return self.chart_data_hidden

    chart_data = ComputedAttribute(__create_chart_data, 1)

    def create_event(self, ev_type, date, related_obj, author=None):
        """
        Register an event. all modules that creates events use this method.
        Exemple: Register event at creation o patient
        author param is used only in importation of ChartDataItemWrapper's.
        """
        chart_data = self.chart_data # garante a criacao do chart_data
        events = chart_data.events
        new_event = Event(self, ev_type, date, related_obj, author)
        events[new_event.id] = new_event

    def get_events(self):
        """
        Return a list of events sorted by date.
        """
        dic = dict(self.chart_data.events)
        events_list = dic.values()
        events_list.sort(cmp=Event._event_cmp)
        return events_list

#   Metodo utilizado apenas no debug_patientchartdata
    def get_chart_data_map(self):
        """
        Return chardata map as:
        {'review_of_systems': <type 'BTrees.OOBTree.OOBTree'>,
         'not_signed_allergies': <type 'BTrees.OOBTree.OOBTree'>,
         'medications': <type 'BTrees.OOBTree.OOBTree'>,
         'prescriptions': <type 'BTrees.OOBTree.OOBTree'>,
         'laboratory': <type 'BTrees.OOBTree.OOBTree'>,
         'allergies': <type 'BTrees.OOBTree.OOBTree'>,
         'problems': <type 'BTrees.OOBTree.OOBTree'>,
         'events': <type 'BTrees.OOBTree.OOBTree'>}
        """
        return ChartData.mapping

    def chart_data_summary(self):
        """
        Method used in migration and in debug_patientchartdata.
        Just return the chart_data in format of dictionaries.
        """

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
        """
        Used exclusively in migration.
        """
        from BTrees.OOBTree import OOBTree

        for key in self.chart_data.mapping.keys():
            if chart_dic.has_key(key): # increase upgrade compatibility
                setattr( self.chart_data, key, OOBTree(chart_dic[key]) )

    def doWorkflowAction(self,action):
        portal = self.portal_url.getPortalObject()
        pw = getToolByName(portal,"portal_workflow")
        patient_workflow = pw.getWorkflowById("patient_workflow")
        patient_workflow.doActionFor(self,action)
        state = pw.getStatusOf("patient_workflow",self)
        return state

    def getState_cmed(self):
        portal = self.portal_url.getPortalObject()
        pw = getToolByName(portal,"portal_workflow")
        state = pw.getStatusOf("patient_workflow",self)
        return state['review_state']

    def reindexVisits(self):
        """
        Visits title are based on patient title. So, when editing a patient we
        need to reindex visits (just present and future ones) in order to garantee
        that their name are ok
        """
        start = DateTime().earliestTime() # nao precisamos reindexar visitas antigas
        end = DateTime(2100, 1, 1)   # far away in the future
        date_range_query = {'query': (start, end), 'range': 'min:max'}
        brains = self.portal_catalog(portal_type='Visit', LTitle=self.getId(), start=date_range_query)
        for br in brains:
            br.getObject().reindexObject() # reindexa a visita

    def setReaderLocalRole(self):
        #Add Reader Role
        acl = self.acl_users
        self.manage_setLocalRoles(self.getId(),[READER_ROLE])
        
        #Set Reader to view
        self.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, READER_ROLE], acquire = False)
        self.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, READER_ROLE], acquire = False)        

    def formattedAge(self):
        """
        Retorna a idade formatada, por ex: 10a2m (10 anos e 2 meses)
        """

        birthdate = self.getBirthDate()
        birthdate = date(birthdate.year(), birthdate.month(), birthdate.day())
        today = date.today()
        
        year_age = today.year - birthdate.year

        # não se faz aniversário na virada do ano, precisamos ajustar
        try:
            birthday_this_year = date(today.year, birthdate.month, birthdate.day)
        except: # caso tenha nascido em 29/02 de um ano bissexto
            birthday_this_year = date(today.year, birthdate.month, birthdate.day-1)
        if not today >= birthday_this_year: # se o aniversario ainda nao aconteceu neste ano
            year_age -= 1

        month_age = today.month - birthdate.month

        # um mês é completado apenas quando o dia na data de aniversário é ultrapassado pela data de hoje
        if not today.day >= birthdate.day:
            month_age -= 1

        month_age = month_age % 12

        return '%sa%sm' % (year_age, month_age)

    def showOrHide(self, action):
        """
        Este método é usado para expirar ou "desespirar" o paciente dependendo do estado
        que ele assume.
        Com isso, caso o paciente esteja Inativo, ele não será mostrado nas buscas.
        """
        if action == 'inactivate':
            self.setExpirationDate("2000/01/01")  # expira o paciente
        elif action == 'activate':
            self.setExpirationDate("2499/12/31")  # desespira o paciente

        self.reindexObject()


atapi.registerType(Patient, PROJECTNAME)

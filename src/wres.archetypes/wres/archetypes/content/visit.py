## encoding=utf-8
"""Definition of the Visit content type
"""

from Products.Archetypes.atapi import *
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

from DateTime import DateTime

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import event
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from wres.archetypes.content.chartdata import Event
from wres.archetypes.interfaces import IVisit
from wres.archetypes.config import PROJECTNAME

from wres.archetypes.content.schemas.visit import VisitSchema

schemata.finalizeATCTSchema(VisitSchema, moveDiscussion=False)

# usada para adicionar minutos do campo duração à data/hora de inicio
# da visita
def addMinutes2Date (date, minutes):
    if (date._minute + minutes) >= 60:
        new_date_minute = date._minute + minutes - 60
        new_date_hour = date._hour + 1
        while new_date_minute >= 60:
            new_date_minute = new_date_minute - 60
            new_date_hour = new_date_hour + 1
    else:
        new_date_minute = date._minute + minutes
        new_date_hour = date._hour
    new_date = DateTime(date._year, date._month, date._day, new_date_hour, new_date_minute)
    return new_date


class Visit(event.ATEvent):
    """Visit"""
    implements(IVisit)

    meta_type = "Visit"
    schema = VisitSchema

    def getDoctor(self):
        portal = getSite()
        pai = self.getParentNode()
        doctor_id = pai.getId()
        return getattr(portal.Doctors, doctor_id)
        
    def getProviderId(self):
        portal = getSite()
        pai = self.getParentNode()
        doctor_id = pai.getId()
        return doctor_id
        
    def getTagDefault(self):
        return 'tag'

    def getTypesOfVisit(self):
        dl = DisplayList()
        # dl.add('', 'Selecione')
        portal = getSite()
        vt = getToolByName(portal, 'vocabulary_tool')
        vocab_list = vt.get_vocabulary('visit_types', 2)
        for vocab in vocab_list:
            # dl_entry = (vocab, vocab)
            dl.add(vocab, vocab)
        # dl.add('outro', 'Outro')
        return dl

    def getVisitReason(self):
        dl = DisplayList()
        dl.add('', 'Selecione')
        portal = getSite()
        vt = getToolByName(portal, 'vocabulary_tool')
        vocab_list = vt.get_vocabulary('visit_reason', 1)
        for vocab in vocab_list:
            # dl_entry = (vocab, vocab)
            dl.add(vocab, vocab)
        dl.add('outro', 'Outro')
        return dl        

    def at_post_create_script(self):
        """ Esse método é chamado no momento da criação de um objeto da classe.
        Ele preenche o campo subject (tags) com um id de um médico.
        """
        patient = self.getPatient()
        patient.create_event(Event.CREATION, self.startDate, self)

        # make scheduled the initial state. This code needs to be here, not in 
        # at_post_edit.
        self.portal_workflow.doActionFor(self, 'schedule')

        self.setTitle(patient.Title())
        self.setSubject('CalendarShow')
        visit_type = self.getVisit_type()
        dl = self.getTypesOfVisit()
        if visit_type not in dl:
            portal = getSite()
            vt = getToolByName(portal, 'vocabulary_tool')        
            vt.add2vocabulary('visit_types', visit_type, 1)     

        visit_reason = self.getVisit_reason()
        dl = self.getVisitReason()
        if visit_reason not in dl:
            portal = getSite()
            vt = getToolByName(portal, 'vocabulary_tool')        
            vt.add2vocabulary('visit_reason', visit_reason, 1) 
        self.at_post_edit_script()

    def addInsurance(self):
        new_insurance = self.getInsurance()
        dl = self.getInsurancesNames()
        if new_insurance not in dl:
            portal = getSite()
            vt = getToolByName(portal, 'vocabulary_tool')        
            vt.add2vocabulary('insurance', new_insurance, 1)
        # self.setTitle(dl.getValue(self.getDocument_type()))

    def at_post_edit_script(self):
#        if self.isAppointment():
#            self.setDefaultPatientId()
#            self.updateTypeOfPatient()
#            self.updateOtherVisitsContactPhone()
#        self.updateObjectOwner()
#        self.updateScheduleFolderSettings()
#        self.setEndDate(self.getEndDate())#what is this for?
        #change the state from non-scheduled to scheduled.
        #Do we need this here?
        # TODO: Retirar em 2013. Eh interessante isso msm? (voltar
        # pro Agendada toda vez que houver uma edicao)
        # self.portal_workflow.doActionFor(self, 'schedule')

        #esse trecho calcula o endDate com base no startDate e na duracao da consulta.
        self.endDate = addMinutes2Date(self.start(), self.getDuration())
        self.addInsurance()
        self.reindexObject()

    def getStartDate(self):
        return self.startDate
        
    def getSocialSecurity(self):
        patient = self.getPatient()
        return patient.getSocialSecurity()        
    
    # utilizado pela BuildingBlocksWidget para pegar um script do
    # portal_skins    
    def popup_search_script(self, arg=None):
        portal = getSite()
        portal_skins = getToolByName(portal, 'portal_skins')
        script = portal_skins.wres_theme_widget.popup_search_script
        return script
    
    # utilizado pelo PatientWrapper em secretarydesktop    
    def getPatientInfo(self):
        info = {}
        try:
            patient = self.getPatient()
            info['absolute_url'] = patient.absolute_url()
            info['absolute_url_path'] = patient.absolute_url_path()
            info['getContactPhone'] = patient.getContactPhone()
            info['getHomePhone'] = patient.getHomePhone()
            # info['getConfirmedChartNumber'] = patient.getConfirmedChartNumber()
            info['Title'] = patient.Title()
        except:
            info['absolute_url'] = ''
            info['absolute_url_path'] = ''
            info['getContactPhone'] = ''
            info['getHomePhone'] = ''
            # info['getConfirmedChartNumber'] = ''
            info['Title'] = ''
        return info        
        
    def getInsurancesNames(self):
        dl = DisplayList()
        dl.add('', 'Selecione')
        portal = getSite()
        vt = getToolByName(portal, 'vocabulary_tool')
        vocab_list = vt.get_vocabulary('insurance', 2)
        for vocab in vocab_list:
            dl.add(vocab, vocab)
        dl.add('outro_plano', 'Outro')
        return dl

atapi.registerType(Visit, PROJECTNAME)

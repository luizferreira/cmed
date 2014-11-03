## encoding=utf-8
"""Definition of the Visit content type
"""

from Products.Archetypes.atapi import *
from Products.statusmessages.interfaces import IStatusMessage
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

    def lower_title(self):
        """
        Método referente ao índice LTitle que guardará o ID do paciente
        """
        patient = self.getPatient()
        if patient:
            return patient.getId()

    def Title(self):
        patient = self.getPatient()
        if patient:
            return patient.Title()
        return ''

    def getRemoteUrl(self):
        """
        Usamos essa metadata column para guardar a URL do paciente. Com isso 
        evitamos um getObject na Agenda (sec_desk)
        """
        patient = self.getPatient()
        if patient:
            return patient.absolute_url()

    def getDoctor(self):
        portal = getSite()
        pai = self.getParentNode()
        doctor_id = pai.getId()
        return getattr(portal.Doctors, doctor_id)

    def getProviderId(self):
        pai = self.getParentNode()
        doctor_id = pai.getId()
        return doctor_id

    def getTypesOfVisit(self):
        '''
        For now, the fild visit type will not have the 'Outro' option. The reason is that, if we
        let the doctor create his own visit types, the tags filter probably will poluted, and frequentely
        we will need to clean manually.
        '''
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
        Ele preenche o campo subject (tags) com visit type no edit.
        """
        patient = self.getPatient()
        patient.create_event(Event.CREATION, self.startDate, self)

        # make scheduled the initial state. This code needs to be here, not in at_post_edit
        self.portal_workflow.doActionFor(self, 'schedule')

        self.setTitle(patient.Title())

        # limpa a pilha de messagens e evita que apareça a mensagem "Suas alteraçoes
        # foram salvas." fora de contexto (já que Visit é salva utilizando Ajax)
        messages = IStatusMessage(self.REQUEST)
        messages.show() 

        self.at_post_edit_script()

    def at_post_edit_script(self):
        # set the tag with the visit type, needed to the visit become showed in calendar.
        self.setSubject(self.getVisit_type())

        # add the visit type as a subject criteria, if it wasnt included yet.
        # that way, if the doctor ask, we just need to create the new visit type in the correspondent
        # vocabulary, and after a visit is created with that type, the system will update the criteria.
        visit_folder = self.getParentNode()
        try:
            collection = getattr(visit_folder, 'Agenda')
        except:
            raise AttributeError("Ow! I can't get the collection Agenda from the visit_folder %s" % visit_folder.getId())
        criteria = getattr(collection, 'crit__Subject_ATSelectionCriterion')
        tags = criteria.getRawValue()
        if self.getVisit_type() not in tags:
            new_tags = tags + (self.getVisit_type(), )
            criteria.setValue(new_tags)
            collection.reindexObject()

        # TODO: maybe we need to test if the contact phone here is the same as the registered one in the
        # patient chart.

        #change the state from non-scheduled to scheduled.
        #Do we need this here?
        # TODO: Retirar em 06/2013. Eh interessante isso msm? (voltar
        # pro Agendada toda vez que houver uma edicao)
        # talvez sim, pq se o médico mover no calendário para outra data, talvez seja interessante
        # voltar ao estado inicial, para recomeçar o processo de confirmaçao, etc.
        # self.portal_workflow.doActionFor(self, 'schedule')

        # preenche o campo convênio de paciente com o convênio desta visita.
        patient = self.getPatient()
        patient.setInsurance(self.getInsurance())

        #esse trecho calcula o endDate com base no startDate e na duracao da consulta.
        self.endDate = addMinutes2Date(self.start(), self.getDuration())
        self.addVisitType()
        self.addVisitReason()
        self.addInsurance()
        self.reindexObject()

    def addVisitType(self):
        visit_type = self.getVisit_type()
        dl = self.getTypesOfVisit()
        if visit_type not in dl:
            portal = getSite()
            vt = getToolByName(portal, 'vocabulary_tool')
            vt.add2vocabulary('visit_types', visit_type, 1, 1)

    def addVisitReason(self):
        visit_reason = self.getVisit_reason()
        dl = self.getVisitReason()
        if visit_reason not in dl:
            portal = getSite()
            vt = getToolByName(portal, 'vocabulary_tool')
            vt.add2vocabulary('visit_reason', visit_reason, 1, 1)

    def addInsurance(self):
        new_insurance = self.getInsurance()
        dl = self.getInsurancesNames()
        if new_insurance not in dl:
            portal = getSite()
            vt = getToolByName(portal, 'vocabulary_tool')
            vt.add2vocabulary('insurance', new_insurance, 1, 1)

    def getStartDate(self): 
        return self.startDate

    def getSocialSecurity(self):
        patient = self.getPatient()
        return patient.getSocialSecurity()

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

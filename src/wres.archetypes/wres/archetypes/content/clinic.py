## coding=utf-8

"""Definition of the Clinic content type
"""

# from Products.DataGridField import DGFMessageFactory as _

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.CMFCore.utils import getToolByName
from wres.archetypes.content.schemas.clinic import ClinicSchema

# -*- Message Factory Imported Here -*-

from wres.archetypes.interfaces import IClinic
from wres.archetypes.config import PROJECTNAME

import sys

class Clinic(base.ATCTContent):
    """Clinic type for WRES Website"""
    implements(IClinic)

    meta_type = "Clinic"
    schema = ClinicSchema

    def fillClinicInformation(self, info):
        self.setName(info['clinic_name'])
        self.setStreet(info['clinic_street'])
        self.setNumber(info['clinic_number'])
        self.setComplemento(info['clinic_complemento'])
        self.setCity(info['clinic_city'])
        self.setState(info['clinic_state'].lower())
        # self.setPhone(info['clinic_phone'])
        # self.setEmail(info['E-mail'])

    def getPatientsCreated(self):
        val = []
        pc = getToolByName(self,"portal_catalog")
        for i in pc.search({"meta_type":"Patient"}):
            val.append([int(i.created.millis()/86400000),1])
        val = sorted(val, key=lambda tup: (-tup[1], tup[0]))
        return val

    def getDocumentsCreated(self):
        val = []
        out = []
        pc = getToolByName(self,"portal_catalog")
        for i in pc.search({"Type":"Documento"}):
            val.append([int(i.created.millis()/86400000),1])
        val = sorted(val, key=lambda tup: (-tup[1], tup[0]))
        return val

    def getVisitsStatus(self):
        val = [['Ausente',0],['Concluida',0],['Desmarcada',0]]
        pc = getToolByName(self,"portal_catalog")
        for i in pc.search({"Type":"Visit"}):
            if i.review_state=="non-show":
                val[0][1] +=1
            if i.review_state=="concluded":
                val[1][1] +=1
            if i.review_state=="unscheduled":
                val[2][1] +=1
        return val

    def getVisitsInsurance(self):
        val = []
        pc = getToolByName(self,"portal_catalog")
        for i in pc.search({"Type":"Visit"}):
            add = 1
            if i.getInsurance!="":
                for j in range(0, len(val)):
                    if val[j][0] == i.getInsurance:
                        val[j][1]+= 1
                        add = 0
                        break
                if add==1:
                    val.append([i.getInsurance,1])
        val = sorted(val, key=lambda tup: (-tup[1], tup[0]))
        return val

    def getVisitsReason(self):
        val = []
        pc = getToolByName(self,"portal_catalog")
        for i in pc.search({"Type":"Visit"}):
            add = 1
            if i.getVisit_reason!="":
                for j in range(0, len(val)):
                    if val[j][0] == i.getVisit_reason:
                        val[j][1]+= 1
                        add = 0
                        break
                if add==1:
                    val.append([i.getVisit_reason,1])
        val = sorted(val, key=lambda tup: (-tup[1], tup[0]))
        return val
atapi.registerType(Clinic, PROJECTNAME)

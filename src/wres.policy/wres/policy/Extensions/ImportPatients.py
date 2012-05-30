# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from wres.archetypes.content.wresuser import create_base_of_id
import codecs

def import_patients(self):

    pc = getToolByName(self, 'portal_catalog')
    pf = getToolByName(self, 'portal_factory')
    patients = getToolByName(self, 'Patients')

    idlist = []

    brains = pc.search({'meta_type': 'Patient'})

    for record in brains:
        idlist.append(record.getObject().getId())

    #referenceDoctor = 'bmorais'
    #brains = pc.search({'meta_type': 'Doctor', 'getId': referenceDoctor})
    #doctor_object = brains[0].getObject()

    file = codecs.open('/tmp/patients', 'r', 'utf-8')
    #field_list = ['firstName', 'lastName', 'contactPhone', 'email']    

    for line in file:
        parts = line.split(';')
        patients.invokeFactory("Patient", create_id(parts[0], parts[1], idlist), firstName=parts[0], lastName=parts[1], contactPhone=parts[2], email=parts[3])
    patients.update()

def create_id(first_name, last_name, idlist):
    base = create_base_of_id(first_name, last_name)
    new_id = base
    num = 0
    while new_id in idlist:
        num += 1
        new_id = "%s%s" % (base, num)
    idlist.append(new_id)
    return new_id

# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
import codecs

def export_patients(self):

    pc = getToolByName(self, 'portal_catalog')
    results = pc(meta_type = 'Patient')

    file = codecs.open('/tmp/patients', 'w', 'utf-8')
    field_list = ['firstName', 'lastName', 'contactPhone', 'email']

    #for field in field_list:
    #    file.write(field+',')
    #file.write('\n')

    for result in results:
        obj = result.getObject()
        for field in field_list:
            if getattr(obj, field, ''):
                file.write(getattr(obj, field, '')+';')
        file.write('\n')


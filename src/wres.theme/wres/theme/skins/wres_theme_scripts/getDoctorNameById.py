##parameters=provider_id
from Products.CMFCore.utils import getToolByName

pc = getToolByName(context, 'portal_catalog')
brains = pc.search({'meta_type': 'Doctor', 'id': provider_id})
try:
    doctor = brains[0].getObject()
    doctor_name = doctor.getFirstName() + ' ' + doctor.getLastName()
except:
    doctor_name = ''
return doctor_name

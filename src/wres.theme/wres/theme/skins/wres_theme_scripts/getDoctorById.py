##parameters=provider_id
from Products.CMFCore.utils import getToolByName

pc = getToolByName(context, 'portal_catalog')
brains = pc.search({'meta_type': 'Doctor', 'id': provider_id})
try:
    doctor = brains[0].getObject()
except:
    doctor = ''
return doctor

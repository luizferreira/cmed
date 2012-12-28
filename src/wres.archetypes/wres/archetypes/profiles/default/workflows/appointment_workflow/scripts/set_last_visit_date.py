## Script (Python) "set_last_visit_date"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state_change
##title=
##
obj = state_change.object
date = obj.getStartDate()
patient = obj.getPatient()
if patient != None: # in importation, the patient field won't be setted yet.
    patient.setLastVisitDate(date)

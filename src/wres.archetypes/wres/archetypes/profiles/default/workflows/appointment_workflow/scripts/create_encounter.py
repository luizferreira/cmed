## Script (Python) "create_encounter"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state_change
##title=
##
def sameDay(date1, date2):
    return (date1.year() == date2.year() and date1.month() == date2.month() and date1.day() == date2.day())

obj = getattr(state_change, 'object')
patient = obj.getPatient()
type_name = 'Encounter'

date_of_visit = obj.start().earliestTime()
encounters = patient.chartFolder.encounters
encounter = None

for element in encounters.values():
    if sameDay(element.getDate_of_visit(), date_of_visit):
        encounter = element

if encounter == None:
    id = obj.generateUniqueId(type_name)
    encounters.invokeFactory(id=id, type_name=type_name)
    encounter = encounters[id]
    encounter.setDate_of_visit(obj.start())

encounter.append_visit(obj.UID())
encounter.reindexObject()

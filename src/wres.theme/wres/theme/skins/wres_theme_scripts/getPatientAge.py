## Script (Python) "getPatientAge"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=birthdate=None
##title=
##
def getDiferenceYears(today, bd):
    return (today.year()-bd.year())

def getAge(age, today, bd):
    today = DateTime(today.dayOfYear())
    bd = DateTime(bd.dayOfYear())
    if today.lessThan(bd):
        return (age - 1)
    return age

def calculeAge(today, birthdate):
    if birthdate:
        if same_type(DateTime(), birthdate):
            bd = birthdate
        else:
            bd = DateTime(birthdate)
        return getAge(getDiferenceYears(today, bd), today, bd)
    return ''

today = DateTime()
return calculeAge(today, birthdate)
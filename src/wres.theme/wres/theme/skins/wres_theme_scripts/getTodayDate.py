## Script (Python) "getTodayDate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=date_str=''
##title=
##

from DateTime import DateTime

# get date: today if passed date is invalid
try:
    return DateTime(str(date_str))
except:
    return DateTime()
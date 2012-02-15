from Products.CMFCore.utils import getToolByName
from wres.policy.utils.utils import getWresSite
from DateTime import DateTime

vt = getToolByName(context,"vocabulary_tool")
DEF_list = vt.get_vocabulary("DEF")
return DEF_list

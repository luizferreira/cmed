from Products.CMFCore.utils import getToolByName
from wres.policy.utils.utils import getWresSite
from DateTime import DateTime

vt = getToolByName(context,"vocabulary_tool")
CID_list = vt.get_vocabulary("CID_code")
return CID_list

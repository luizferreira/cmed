from Products.CMFCore.utils import getToolByName
vt = getToolByName(context, 'vocabulary_tool')
backup = vt.get_vocabulary('cmed_backup')

try:
	return backup[0]
except:
	return ""

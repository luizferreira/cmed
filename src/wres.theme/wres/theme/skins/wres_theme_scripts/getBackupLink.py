from Products.CMFCore.utils import getToolByName
vt = getToolByName(context, 'vocabulary_tool')
backup = vt.get_vocabulary('cmed_backup')
return backup[0]

## Script (Python) "lstDDD"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=value='',part='complete'
##title=
##

value = str(value)
tmpReturn = ''

if not value:
    return tmpReturn
    
isSpecialPhone = value.startswith('0')

displayFmt = (isSpecialPhone and '%s%s%s') or '(%s)%s-%s'

tmpDDD = (isSpecialPhone and value[:4]) or value[:2]
tmpPhone = (isSpecialPhone and value[4:]) or value[2:]
tmpPhone1 = tmpPhone[:-4]
tmpPhone2 = tmpPhone[-4:]

if part == 'complete':
    tmpReturn = displayFmt % (tmpDDD,tmpPhone1,tmpPhone2)
elif part == 'ddd':
    tmpReturn = tmpDDD
else:
    tmpReturn = tmpPhone

return tmpReturn
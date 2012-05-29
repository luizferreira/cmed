##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=list
##

to_return = []

for item in list:
    if item.getName() == 'lastName' or item.getName() == 'birthDate':
        to_return.append (item)

return to_return
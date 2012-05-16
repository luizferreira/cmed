## Script (Python) "verifyRole"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=roles=[]
##title=
##

# Attributes
request = container.REQUEST
response =  request.RESPONSE
session  = request.SESSION
form = request.form
cookies = request.cookies

# Obtem o objeto portal
portal = context.portal_url.getPortalObject()

userRoles = portal.portal_membership.getAuthenticatedMember().getRoles()
verify = 0

for role in roles:
 if role in userRoles:
   verify = 1

return verify

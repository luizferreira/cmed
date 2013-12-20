## coding=utf-8

response = {}

auth_user = context.portal_membership.getAuthenticatedMember()
user_roles = auth_user.getRoles()

cmed = context.restrictedTraverse(context.portal_url.getPortalPath())
base = cmed.absolute_url()

response['links'] = {}
response['links']['configuration'] = base + '/configuration'
response['links']['doctorfolder'] = base + '/Doctors'
response['links']['secretaryfolder'] = base + '/Secretaries'

if 'Doctor' in user_roles or 'Manager' in user_roles:
    response['links']['clinic'] = base + '/Clinic'
else:
    response['links']['clinic'] = ''

if 'Doctor' in user_roles:
    response['links']['mydata'] = base + '/Doctors/' + auth_user.getId()
elif 'Secretary' in user_roles:
    response['links']['mydata'] = base + '/Secretaries/' + auth_user.getId()
else:
    response['links']['mydata'] = None


# este atributo indica qual link deve estar como current (destacado) no portlet
response['current'] = ''
if context.getId() == auth_user.getId():
    response['current'] = 'mydata'
elif context.portal_type == 'Doctor' or context.portal_type == 'DoctorFolder':
        response['current'] = 'doctorfolder'
elif context.portal_type == 'Clinic':
    response['current'] = 'clinic'
elif context.portal_type == 'Secretary' or context.portal_type == 'SecretaryFolder':
        response['current'] = 'secretaryfolder'

return response

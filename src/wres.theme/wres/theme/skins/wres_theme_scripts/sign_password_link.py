#from wres.policy.utils.utils import get_related_user_object

#member = context.portal_membership.getAuthenticatedMember()
#obj = get_related_user_object(context, member)
return context.absolute_url() + '/change_sign_password'

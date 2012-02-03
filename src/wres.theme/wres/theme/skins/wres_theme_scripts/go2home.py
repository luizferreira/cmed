from wres.policy.utils.utils import getWresSite
from Products.CMFCore.utils import getToolByName

portal = getWresSite()
mt = getToolByName(portal, 'portal_membership')
if mt.isAnonymousUser():
    container.REQUEST.RESPONSE.redirect(context.portal_url() + '/logged_out')
else:
    member = mt.getAuthenticatedMember()
    username = member.getUserName()
    if username == 'admin':
        container.REQUEST.RESPONSE.redirect(context.portal_url() + '/view')
        return

acl = getToolByName(portal, 'acl_users')
user = acl.getUserById(username)
home_url = user.getProperty('home_url')

container.REQUEST.RESPONSE.redirect(home_url)

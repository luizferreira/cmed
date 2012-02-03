##Controller Python Script "logged_in"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Initial post-login actions
##

from Products.CMFPlone import PloneMessageFactory as _
REQUEST=context.REQUEST

# if we weren't called from something that set 'came_from' or if HTTP_REFERER
# is the 'logged_out' page, return the default 'login_success' form
login_success = None
came_from = REQUEST.get('came_from')
if came_from is None or \
   came_from.endswith('logged_out') or \
   came_from.endswith('mail_password') or \
   came_from.endswith('member_search_results') or \
   came_from.endswith('login_form'):
    login_success = '%s/%s' % (context.portal_url(), 'login_success')

# If someone has something on their clipboard, expire it.
if REQUEST.get('__cp', None) is not None:
    REQUEST.RESPONSE.expireCookie('__cp', path='/')

membership_tool=context.portal_membership
if membership_tool.isAnonymousUser():
    REQUEST.RESPONSE.expireCookie('__ac', path='/')
    context.plone_utils.addPortalMessage(_(u'Login failed'))
    return state.set(status='failure')

member = membership_tool.getAuthenticatedMember()

# i have to change here to get the initial page for a user
REFERER=REQUEST.get('HTTP_REFERER')
if login_success:
    URL=login_success
else:
    URL=REQUEST.get('came_from', REFERER)

URL=member.getProperty('home_url',URL)
state.set(redirect=URL)

login_time = member.getProperty('login_time', '2000/01/01')
initial_login = int(str(login_time) == '2000/01/01')
state.set(initial_login=initial_login)

must_change_password = member.getProperty('must_change_password', 0)
state.set(must_change_password=must_change_password)

if initial_login:
    state.set(status='initial_login')
elif must_change_password:
    state.set(status='change_password')

membership_tool.setLoginTimes()
membership_tool.createMemberArea()

return state

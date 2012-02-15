# coding=utf-8

from wres.policy.utils.utils import getWresSite
from Products.CMFCore.utils import getToolByName

# este script pressupõe que apenas um médico o chamará,
# essa pressuposição será sempre correta, já que apenas
# médicos podem ver o link Calendário (que chama esse
# script)

portal = getWresSite()
mt = getToolByName(portal, 'portal_membership')
member = mt.getAuthenticatedMember()
username = member.getUserName()
container.REQUEST.RESPONSE.redirect(context.portal_url() + '/Appointments/'  + username)
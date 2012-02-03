#from wres.policy.utils.utils import setDenyInformation
#from DateTime import DateTime
from Products.CMFPlone import PloneMessageFactory as _

request = context.REQUEST
deny_notes = request.get('other_deny_reason')
#date = DateTime()
#date_str = date.strftime('%d/%m/%Y - %I:%M %p')

#member = context.portal_membership.getAuthenticatedMember()
#doctor = getattr(context.Doctors, member.id)

#signature = doctor.getSignature()
#if not signature:
#    signature = "Dr. %s %s" % (doctor.getFirstName(), doctor.getLastName())

#deny_information = {'denied': True,
#                    'deny_reason': request.get('deny_reason'),
#                    'other_deny_reason': request.get('other_deny_reason'),
#                    'actor': signature,
#                    'date': date_str,
#}

#setDenyInformation(deny_information)

context.portal_workflow.doActionFor(context, 'really_deny', comment=deny_notes)
context.plone_utils.addPortalMessage(_('Documento Negado.'))

return state

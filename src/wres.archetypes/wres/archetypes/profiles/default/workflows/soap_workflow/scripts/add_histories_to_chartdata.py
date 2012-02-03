## Script (Python) "add_histories_to_chartdata"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state_change
##title=
##

#from DateTime import DateTime
obj = state_change.object

if hasattr(obj, 'distributeDataInChart'):
    obj.distributeDataInChart()
#date = DateTime()
#date_str = date.strftime('%d/%m/%Y - %I:%M %p')
#member = context.portal_membership.getAuthenticatedMember()
#doctor = getattr(context.Doctors, member.id)
#signature = doctor.getSignature()
#if not signature:
#    signature = "Dr. %s %s" % (doctor.getFirstName(), doctor.getLastName())
#sign_information = {'signed': True,
#                    'signature': signature,
#                    'date_str': date_str,
#                    }
#obj.setSignInformation(sign_information)

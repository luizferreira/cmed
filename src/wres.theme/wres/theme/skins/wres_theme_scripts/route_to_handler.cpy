##parameters=routable
from Products.CMFPlone import PloneMessageFactory as _

title = ''
#brains = context.uid_catalog.search({'UID': routable})
review_notes = context.REQUEST.get('review_notes')
#user = brains[0].getObject()
#if user.getProfessional().lower() == 'provider':
#    context.setDoctor(routable)
#    doctor = context.getDoctor()
#    title = 'Dr. %s %s' % (doctor.getFirstName(), doctor.getLastName())
#elif user.getProfessional().lower() == 'transcriptionist':
#    title = 'Transcriptionist %s %s' % (user.getFirstName(), user.getLastName())
#context.setReview_notes(review_notes) ---> Precisamos de campos review notes nos tipos
context.portal_workflow.doActionFor(context, 'really_review', comment=review_notes)
context.plone_utils.addPortalMessage(_('Documento enviado para revisao.'))
return state

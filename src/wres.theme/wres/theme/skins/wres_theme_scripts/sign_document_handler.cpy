##syntaxe on
from wres.policy.utils.utils import get_related_user_object, canSignPn
from Products.CMFPlone import PloneMessageFactory as _

request = context.REQUEST
button = request.get('button', 'sign')
if button == 'cancel':
    state.set(portal_status_message='Canceled Signing')
    return state
entered_passwd = request.get('passwd', '')
    
member = context.portal_membership.getAuthenticatedMember()
doctor = get_related_user_object(context, member)
if not canSignPn(context, doctor, entered_passwd):
    context.plone_utils.addPortalMessage(_('Senha incorreta. Tente novamente.'))
    state.setStatus('failure')
    return state
else:
    context.portal_workflow.doActionFor(context, 'really_sign')
    context.plone_utils.addPortalMessage(_('Documento Assinado.'))
return state

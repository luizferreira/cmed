##syntaxe on
from wres.policy.utils.utils import get_related_user_object
from Products.CMFPlone import PloneMessageFactory as _

request = context.REQUEST
    
member = context.portal_membership.getAuthenticatedMember()
doctor = get_related_user_object(context, member)

if doctor.getSignPassword() == request.get('act'):
    if request.get('new') == request.get('conf'):
        doctor.setSignPassword(request.get('new'))
        context.plone_utils.addPortalMessage(_('Senha de assinatura alterada com sucesso.'))
        return state
    else:
        context.plone_utils.addPortalMessage(_('As novas senhas digitadas nao conferem.'))
        state.setStatus('failure')
        return state
else: 
    context.plone_utils.addPortalMessage(_('A senha atual nao confere.'))
    state.setStatus('failure')
    return state

#if not canSignPn(context, doctor, entered_passwd):
#    context.plone_utils.addPortalMessage(_('Senha incorreta. Tente novamente.'))
#    state.setStatus('failure')
#    return state
#else:
#    context.portal_workflow.doActionFor(context, 'really_sign')
#    context.plone_utils.addPortalMessage(_('Documento Assinado.'))
#return state

# Esse script eh chamado por um js em footer_cstat.pt. Ele constroi a URL
# do cstat que sera chamada para registrar a requisicao.

from Products.CMFCore.utils import getToolByName

prefix = 'cmed_'
site = "http://cstat.communi.com.br/cmed_stat"

mt = getToolByName(context, 'portal_membership')
member = mt.getAuthenticatedMember()
username = member.getUserName()

params = {}
params[prefix + 'url'] = context.REQUEST.URL
params[prefix + 'user'] = username
params[prefix + 'roles'] = '__'.join(member.getRoles())

url = site + '?'
for param in params:
    url += '%s=%s&' % (param, params[param])

# exemplo de url retornada
# http://cstat.communi.com.br/cmed_stat?cmed_user=admin&cmed_url=http://localhost:8010/wres6/doctor_presentation&cmed_roles=Manager__Authenticated& 

return url
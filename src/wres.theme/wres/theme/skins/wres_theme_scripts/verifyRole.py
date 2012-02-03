## Script (Python) "verifyRole"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=roles=[]
##title=
##
# Nomes validos:
#
# request   : objeto request. Somente consulta ou insere dados
#                         Ex:  x = request['nome']
#                                  request.set('nome','valor')
#                                  request.has_key('chave')
#
# response  : objeto response. Ex:  response.redirect('pagina')
#                                   response.setCookie('nome','valor')
#                                   response.appendCookie('nome','valor')
#                                   response.expireCookie('nome')
#                                   response.write('<b>negrito</b>')
#                                   response.setHeader('Content-Type', 'text/html')
#
# session   : objeto sessao (dicionario). Ex:  x = session['pagina']
#                                 session['pagina'] = {'chave':'valor'}
#                                 session.has_key('chave')
#                                 session.delete('chave')
#
# form      : dicionario que guarda os itens do formulario. Somente consulta ou insere dados
# cookies   : objeto que guarda os itens do cookie. Lomente leitura !! -->Manipulado pelo response.
# ------------------------------------------------------------------------------------------------
# METHODOS IMPORTANTES
#
# Adicionando uma instancia de ZClass
# instance = container.nomeDoProduto.createInObjectManager(request['id'], request)
#
# ------------------------------------------------------------------------------------------------
# Adicionando uma instancia de uma ZClass closed box no dir container
# try:
#   try:
#     container.manage_addProduct['PythonScripts'].manage_addPythonScript(id,titulo)
#     container.manage_addProduct['OFSP'].manage_addDTMLDocument(id,titulo)
#   finally:
#     getattr(container,id).ZPythonScript_edit(tit,valBody)
# except:
#   pass
# -------------------------------------------------------
#
# container : diretorio pai
# context   : objeto sobre o qual este script eh chamado
# namespace : espaco de nomes
# script    : este script
# printed   : varivel que contem o contedo impresso pela funo print

# Atribuies.
request = container.REQUEST
response =  request.RESPONSE
session  = request.SESSION
form = request.form
cookies = request.cookies

# Obtem o objeto portal
portal = context.portal_url.getPortalObject()

userRoles = portal.portal_membership.getAuthenticatedMember().getRoles()
verify = 0

for role in roles:
 if role in userRoles:
   verify = 1

return verify

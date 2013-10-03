# coding=utf-8

__author__  = '''Communi'''
__docformat__ = 'plaintext'

"""
Este arquivo contem validadores para os campos Archetypes.
utilize a classe CurrentPasswordValidator como modelo para 
criar novos validadores.
"""

from Products.validation.config import validation
from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements

listValidators = []

class CurrentPasswordValidator:
    """
    Valida a senha inserida no campo de senha atual.
    """
    
    implements(IValidator)
    
    def __init__(self, name, title='', description=''):
        """
        Chamado na instanciacao do objeto CurrentPasswordValidator
        (no listValidators.append)
        """
        self.name = name
        self.title = title or name
        self.description = description
    
    def __call__(self, value, *args, **kw):
        """
        essa eh o metodo chamado no momento da validacao.
        value contem o valor colocado no campo a ser validado. Ex:
        value = ea5c871e-f8d2-4c7a-a32d-fe7891993130
        args eh uma tupla com todos os parametros.
        kw contem informacoes do campo, do objeto, da requisicao, etc. Ex:
        kw = {'field': <Field patient(reference:rw)>, 
              'errors': {}, 
              'REQUEST': <HTTPRequest, URL=http://localhost:8080/wres3/Appointments/dteste/visittemp.2012-02-15.6261846328/SFValidate_integrity>, 
              'instance': <VisitTemp at /wres3/Appointments/dteste/visittemp.2012-02-15.6261846328>}
        """
        
        passwd = value
        instance = kw['instance']
        pm = instance.portal_membership
        if pm.testCurrentPassword(passwd):
            return True
        else:
            return 'Senha incorreta.'

listValidators.append(CurrentPasswordValidator('isCurrentPassword', title='Validador de senhas', description=''))

for validador in listValidators:
    validation.register(validador)

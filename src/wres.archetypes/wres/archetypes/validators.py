# TODO: DELETAR ARQUIVO
# # coding=utf-8

# __author__  = '''Communi'''
# __docformat__ = 'plaintext'

# # esse arquivo contem validadores para os campos Archetypes.
# # utilize a classe ValidadorBuildingBLocks como modelo para 
# # criar novos validadores.

# from Products.validation.interfaces import ivalidator

# from Products.validation.config import validation
# from Products.validation.interfaces.IValidator import IValidator
# from zope.interface import implements

# from zope.i18nmessageid import MessageFactory, Message
# _ = MessageFactory("cmfuemr")

# import re

# listValidators = []

# class ValidadorBuildingBlocks:
#     """
#     Valida a referencia a paciente na criacao da visita.
#     """
    
#     implements(IValidator)
    
#     def __init__(self, name, title='', description=''):
#         # chamado na instanciacao do objeto ValidadorBuildingBlocks
#         # (no listValidators.append)
#         self.name = name
#         self.title = title or name
#         self.description = description
    
#     def __call__(self, value, *args, **kw):
#         # essa eh o metodo chamado no momento da validacao.
#         # value contem o valor colocado no campo a ser validado. Ex:
#         # value = ea5c871e-f8d2-4c7a-a32d-fe7891993130
#         # args eh uma tupla com todos os parametros.
#         # kw contem informacoes do campo, do objeto, da requisicao, etc. Ex:
#         # kw = {'field': <Field patient(reference:rw)>, 
#         #       'errors': {}, 
#         #       'REQUEST': <HTTPRequest, URL=http://localhost:8080/wres3/Appointments/dteste/visittemp.2012-02-15.6261846328/SFValidate_integrity>, 
#         #       'instance': <VisitTemp at /wres3/Appointments/dteste/visittemp.2012-02-15.6261846328>}
        
#         if value == ['no_patient']:
#             return _(u"Você precisa escolher um paciente.")
        
#         return True
    

# listValidators.append(ValidadorBuildingBlocks('isValidReference', title=_(u'Validator de Referencias'), description=''))

# for validador in listValidators:
#     validation.register(validador)

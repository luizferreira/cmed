# coding=utf-8

__author__  = '''Simples Consultoria'''
__docformat__ = 'plaintext'

from Products.validation.interfaces import ivalidator

from Products.validation.config import validation
from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements

from wres.brfields import MessageFactory as _

import re

listValidators = []

class ValidadorCPF:
    """
    Validador para verificar se o CPF informado e valido
    Baseado em http://www.pythonbrasil.com.br/moin.cgi/VerificadorDeCPF .
    """
    
    #__implements__ = IValidator # Padrão P3
    implements(IValidator)
    
    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description
    
    
    def __call__(self, value, *args, **kw):
        cpf = value
        cpf = ''.join([c for c in value if c.isdigit()])
        
        if len(cpf) != 11:
            return _(u"CPF precisa ter 11 dígitos.")
        elif len(cpf)==11:
            vtemp = [int(cpf[:1]) for i in list(cpf)] 
            cpf2 = [int(i) for i in list(cpf)]
            if cpf2 == vtemp:
                return _(u"CPF inválido.")
            
            tmp = cpf[:9] 
            ltmp = [int(i) for i in list(tmp)]               
            
            while len(ltmp) < 11:
                R = sum(map(lambda(i,v):(len(ltmp)+1-i)*v,enumerate(ltmp))) % 11
                
                if R > 1:
                    f = 11 - R
                else:
                    f = 0
                ltmp.append(f)
            
            if cpf2 != ltmp:
                return _(u"O dígito verificador do CPF não confere.")
        return True
    

listValidators.append(ValidadorCPF('isCPF', title=_(u'Validator de CPF'), description=''))

class ValidadorCNPJ:
    """
    Validador para verificar se o CNPJ informado e valido.
    Baseado em http://www.pythonbrasil.com.br/moin.cgi/VerificadorDeCnpj
    """
    
    #__implements__ = IValidator # Padrão P3
    implements(IValidator)
    
    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description
    
    
    def __call__(self, value, *args, **kw):
        cnpj = value
        cnpj = ''.join([c for c in value if c.isdigit()])
        if len(cnpj) != 14:
            return _(u"O CNPJ deve ter 14 dígitos.")
        elif len(cnpj) == 14:
            vtemp = [int(cnpj[:1]) for i in list(cnpj[:8])] 
            cnpj2 = [int(i) for i in list(cnpj[:8])]
            
            if cnpj2 == vtemp:
               return _(u"O CNPJ informado é inválido.")
            
            tmp = cnpj[:12]
            ltmp = [int(i) for i in list(tmp)]
            temp = [int(i) for i in list(cnpj)]
            prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            
            while len(ltmp) < 14:
                R = sum([x*y for (x, y) in zip(ltmp, prod)])%11
                if R >= 2:
                    f = 11 - R
                else:
                    f = 0
                ltmp.append(f)
                prod.insert(0,6)
            if temp != ltmp:
                return _(u"O CNPJ informado é inválido.")
        return True
    

listValidators.append(ValidadorCNPJ('isCNPJ', title='', description=''))

class ValidadorCEP:
    """
    Validador para informar se o CEP informado is valido. Sao aceitos codigos 
    de enderecamento postal em duas formas:Oito digitos consecutivos ou cinco 
    digitos, hifen, tres digitos, ou seja, XXXXXXXX ou XXXXX-XXX, onde cada X 
    pode ser qualquer digito entre 0 e 9.
    """
    
    #__implements__ = IValidator # Padrão P3
    implements(IValidator)
    
    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description
    
    
    def __call__(self, value, *args, **kw):
        cep = ''.join([c for c in value if c.isdigit()])
        
        if not(len(cep)==8):
            return _(u"O cep informado é inválido.")
        return True

listValidators.append(ValidadorCEP('isCEP', title='CEP Validator', description=''))

class ValidadorBrPhone:
    """
    Validador para telefones brasileiros. Suportando os formatos:
        XXXXXXXXXXX (DD123456789) - Algumas regiões já adotam cel com 9 dígitos
        XXXXXXXXXX (1155553211) - Novos telefones
        XXXXXXXXX  (115552133) - Antigos telefones
        0n00XXXXXXX (n sendo 3 ou 8)
        0n00XXXXXX (n sendo 3 ou 8)
    """
    
    #__implements__ = IValidator # Padrão P3
    implements(IValidator)
    
    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description
    
    def __call__(self, value, *args, **kw):
        
        phone = ''.join([c for c in value if c.isdigit()])
        status = True

        if phone.startswith('0'):
            if not((len(phone) in [10,11,12]) and phone.isdigit()):
                status = False
        elif not(len(phone) in [9,10,11] and phone.isdigit()):
            status = False
        
        return status or _(u"Telefone inválido")
    

listValidators.append(ValidadorBrPhone('isBrPhone', title='Brazilian Phone Validator', description=''))

for validador in listValidators:
    validation.register(validador)

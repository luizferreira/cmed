from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import StringWidget
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Field import StringField

from wres.brfields import MessageFactory as _

class CPFWidget(StringWidget):
    security = ClassSecurityInfo()
    
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro': 'BrCPF',
        'helper_js': ('BrFieldsAndWidgets.js',),
        })
    


class CPFField(StringField):
    security  = ClassSecurityInfo()    
    _properties = StringField._properties.copy()
    _properties.update({
        'widget': CPFWidget,
        'validators': ('isCPF',),
        })
    


class CEPWidget(StringWidget):
    security = ClassSecurityInfo()
    
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro': 'BrCEP',
        'helper_js': ('BrFieldsAndWidgets.js',),
        })
    


class CEPField(StringField):
    security  = ClassSecurityInfo()    
    _properties = StringField._properties.copy()
    _properties.update({
        'widget': CEPWidget,
        'validators': ('isCEP',),
        })
    


class CNPJWidget(StringWidget):
    security = ClassSecurityInfo()
    
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro': 'BrCNPJ',
        'helper_js': ('BrFieldsAndWidgets.js',),
        })
    


class CNPJField(StringField):
    security  = ClassSecurityInfo()    
    _properties = StringField._properties.copy()
    _properties.update({
        'widget': CNPJWidget,
        'validators': ('isCNPJ',),
        })
    


class BrPhoneWidget(StringWidget):
    security = ClassSecurityInfo()
    
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro': 'BrPhone',
        'helper_js': ('BrFieldsAndWidgets.js',),
        })
    


class BrPhoneField(StringField):
    security  = ClassSecurityInfo()    
    _properties = StringField._properties.copy()
    _properties.update({
        'widget': BrPhoneWidget,
        'validators': ('isBrPhone',),
        })
    


class BrTimeWidget(StringWidget):
    security = ClassSecurityInfo()
    
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro': 'BrTime',
        'helper_js': ('BrFieldsAndWidgets.js',),
        })


registerWidget(CPFWidget,
               title='CPF',
               description="CPF widget.",
               used_for=('Products.Archetypes.public.StringField',)
               )

registerWidget(CEPWidget,
               title='CEP',
               description="CEP widget.",
               used_for=('Products.Archetypes.public.StringField',)
               )

registerWidget(CNPJWidget,
               title='CNPJ',
               description="CNPJ widget.",
               used_for=('Products.Archetypes.public.StringField',)
               )

registerWidget(BrPhoneWidget,
               title='BrPhone',
               description="BrPhone widget.",
               used_for=('Products.Archetypes.public.StringField',)
               )

registerWidget(BrTimeWidget,
               title='BrTimeWidget',
               description="BrTime widget.",
               used_for=('Products.Archetypes.public.StringField',)
               )
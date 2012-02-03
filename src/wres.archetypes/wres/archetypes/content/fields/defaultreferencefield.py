
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import ReferenceField
from Products.Archetypes.interfaces import IObjectField
from Products.Archetypes.config import REFERENCE_CATALOG

# o DefaultReferenField e' um ReferenceField com suporte a default_method
class DefaultReferenceField(ReferenceField):

    implements(IObjectField)
    security = ClassSecurityInfo()
    
    security.declarePrivate('getRaw')
    def getRaw(self, instance, aslist=False, **kwargs):
        """Return the list of UIDs referenced under this fields
        relationship.
        
        During creation look for a default value. This will only work for
        user edited forms, not programmatically generated content.
        """
        if instance._at_creation_flag:
            return self.getDefault(instance)
        else:
            return ReferenceField.getRaw(self, instance, aslist, **kwargs)
# Python
# from sets import Set
# from DateTime import DateTime

# Zope
# import Globals
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo

# CMF
# from Products.CMFCore.utils import getToolByName
# from Products.CMFCore import permissions as CMFCorePermissions

# Other Products
from OFS.PropertyManager import PropertyManager

# herdando de PropertyManager permite que a tool possua atributos.
class NewVocabTool(SimpleItem, PropertyManager):
    """ Manage persistent dynamic vocabularies. """

    # General properties
    security = ClassSecurityInfo()
    plone_tool = 1
    id = 'new_vocab_tool'
    meta_type = 'NewVocabTool'
    
    # Vocabulary portal property
    property_prefix = 'vocab'

    manage_options = (
        {'action': 'manage_propertiesForm', 'label': 'Properties'},
    )

    def teste(self):
        import ipdb; ipdb.set_trace()

    def __get_property_name(self, prefix, suffix):
        """ Returns the property name following a convention. """
        return prefix + '_' + suffix

    def _persist_vocabulary_manager(self, property_name, vocab_list):
        to_persist = vocab_list
        if self.hasProperty(property_name):
            self.manage_changeProperties(**{property_name: to_persist})
        else:
            self.manage_addProperty(property_name, [], 'lines')
            self.manage_changeProperties(**{property_name: to_persist})        

    security.declarePublic('add_vocabulary')
    def add_vocab(self, new_vocab_name, new_vocab_content):
        """ Adds a vocabulary. new_vocab_content is a list of strings """
        property_name = self.__get_property_name(self.property_prefix, new_vocab_name)
        self._persist_vocabulary_manager(property_name, new_vocab_content)

    security.declarePublic('get_vocabulary')
    def get_vocabulary(self, vocab_name):
        """ Gets a vocabulary. A vocabulary is represented by a list of strings."""
        property_name = self.__get_property_name(self.property_prefix, vocab_name)
        vocab_list = list(self.getProperty(property_name, []))
        return vocab_list

    def add2vocabulary(self, vocab_name, new_vocabule):
        current_vocab = self.get_vocabulary(vocab_name)
        if new_vocabule not in current_vocab:
            current_vocab.append(new_vocabule)
            property_name = self.__get_property_name(self.property_prefix, vocab_name)
            self._persist_vocabulary_manager(property_name, current_vocab)

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
class VocabularyTool(SimpleItem, PropertyManager):
    """ Manage persistent dynamic vocabularies. """

    # General properties
    security = ClassSecurityInfo()
    plone_tool = 1
    id = 'vocabulary_tool'
    meta_type = 'VocabularyTool'
    
    # Vocabulary portal property
    property_prefix = 'vocab'

    manage_options = (
        {'action': 'manage_propertiesForm', 'label': 'Properties'},
    )

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
    def get_vocabulary(self, vocab_name, get_type=0):
        """ Gets a vocabulary. A vocabulary is represented by a list of strings.
        get_type refers to the way the words will be presented.
        get_type = 0: Strings will be presented the same way that is persisted in the vocab.
        get_type = 1: First letter of the strings will be upper cased.
        get_type = 2: First leters of the words will be upper cased.
        """
        property_name = self.__get_property_name(self.property_prefix, vocab_name)
        vocab_list = list(self.getProperty(property_name, []))
        if not get_type:
            return vocab_list
        new_vocab_list = []
        if get_type == 1:
            for vocab in vocab_list:
                new_vocab = vocab[0].upper() + vocab[1:]
                new_vocab_list.append(new_vocab)
        else: # get_type = 2
            for vocab in vocab_list:
                vocab_sp = vocab.split(' ')
                new_vocab_sp = []
                for v in vocab_sp:
                    if len(v) > 2:
                        v = v[0].upper() + v[1:]
                    new_vocab_sp.append(v)
                new_vocab = str.join(' ', new_vocab_sp)
                new_vocab_list.append(new_vocab)
        return new_vocab_list

    def add2vocabulary(self, vocab_name, new_vocabule, add_type=0):
        """ add_type refers to the way the words will be saved in the vocab.
        0 = words saved the exact way the word came.
        1 = words saved lower cased.
        """
        if add_type:
            new_vocabule = new_vocabule.lower()
        current_vocab = self.get_vocabulary(vocab_name)
        if new_vocabule not in current_vocab:
            current_vocab.append(new_vocabule)
            property_name = self.__get_property_name(self.property_prefix, vocab_name)
            self._persist_vocabulary_manager(property_name, current_vocab)

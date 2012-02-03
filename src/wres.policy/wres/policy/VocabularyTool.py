# Python
from sets import Set
from DateTime import DateTime

# Zope
import Globals
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo

# CMF
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions as CMFCorePermissions

#================================================================================#
# Peter Thorun - prthorun@gmail.com                                              #
#                                                                                #
# VocabularyTool trabalha com uma lista (vocab_list) dicionarios 'vocabulos'.    #
# Cada dicionario 'vocabulo' = {'sentence': String, 'use': Int}                  #
# onde sentence eh uma frase. As sentencas sao classificadas e buscadas de       #
# acordo com sua ultima utilizacao representada por um inteiro.                  #
# A politica de insercao e remocao e o MRU (Most Recently Used)                  #
#                                                                                # 
#================================================================================#

class VocabularyTool(SimpleItem):
    """ Manage persistent dynamic vocabularies. """
    
    # General properties
    security = ClassSecurityInfo()
    plone_tool = 1
    id = 'vocabulary_tool'
    meta_type = 'VocabularyTool'
    
    # Vocabulary portal property
    property_prefix = 'vocab'
    vocab_size = 30 #tamanho do cache de vocabularios
    ignored_fields = ['family_diseases', 'gineco_mamo',] #lista dos nomes dos campos que ignoram vocabulario
    dg_ignored_subfields = ['reaction', 'start', 'desc', 'code'] #lista dos nomes de subcampos DataGrid a serem ignorados
    
    security.declarePrivate('__get_property_name')
    def __get_property_name(self, prefix, suffix):
        """ Returns the property name following a convention. """
        return prefix + '_' + suffix

    security.declarePublic('add_vocabulary')
    def add_vocabulary(self, vocab_name, new_vocab):
        """ Adds a vocabulary. new_vocab is a list of strings """
        property = self.__get_property_name(self.property_prefix, vocab_name)
        if hasattr(self, property):
            vocab_list = self.update_vocabulary(vocab_name, property, new_vocab)
        else:
            vocab_list = [{'sentence': '', 'rank': 0}]
            for sentence in new_vocab:  
                vocab_list = [{'sentence': self.sub_numeros(sentence), 'rank': 0}]
        if vocab_name not in self.ignored_fields:
            vocab_list = self.update_mru(vocab_list)
            self._persist_vocabulary_manager(property, vocab_list)

    security.declarePublic('update_vocabulary')
    def update_vocabulary(self, vocab_name, property, new_vocab):
        """ Updates a given vocab_list with the list of new vocabules."""
        current_list = list(self.getProperty(property, []))
        for sentence in new_vocab:
            current_list = self.apply_filters(sentence, current_list, vocab_name)
        return current_list

    def apply_filters(self, sentence, current_list, vocab_name):
        flag = 0 #marca que sentenca nao esta no vocabulario
        if sentence: #exclui sentencas vazias
            for vocabule in current_list: #checa se sentence ja esta no vocabulario
                sentence = self.sub_numeros(sentence) # troca numeros por ?
                if self.limpa_sentenca(sentence) == self.limpa_sentenca(vocabule['sentence']):#se ja estiver no vocabulario...
                    maximo = self.get_max_rank(current_list)
                    vocabule['rank'] = maximo+1 #atualiza o rank
                    flag = 1 #marca que ja esta no vocabulario
                    break #se ja esta no vocabulario break
            if flag == 0: #se nao esta no vocabulario entao insere
                current_list = self.add_mru(sentence, current_list) #inserindo
        return current_list

    def _persist_vocabulary_manager(self, property, vocab_list):
        to_persist = vocab_list
        if hasattr(self, property):
            self.manage_changeProperties(**{property: to_persist})
        else:
            self.manage_addProperty(property, [], 'lines')
            self.manage_changeProperties(**{property: to_persist})

    def add_mru (self, sentence, current_list):
        maximo = self.get_max_rank(current_list)
        maximo = maximo+1
        if len(current_list) == self.vocab_size:
            current_list.pop()
            new_dict = {'sentence': sentence, 'rank': maximo}
        else:
            new_dict = {'sentence': sentence, 'rank': maximo}
        current_list.insert(0, new_dict) 
        return current_list

    def update_mru (self, current_list):
        current_list = sorted(current_list, reverse=True)
        maximo = self.get_max_rank(current_list)
        if maximo > 30000:
            for i in range(len(current_list)):
                current_list[len(current_list)-1 - i]['rank'] = i
        return current_list

    def get_max_rank(self, current_list):
        maximo = 0
        for vocabule in current_list:
            if vocabule['rank'] > maximo:
                maximo = vocabule['rank']
        return maximo
        
    security.declarePublic('clear_vocabulary')
    def clear_vocabulary(self, vocab):
        """ Remove empty strings from vocabulary. """
        vocab = [v for v in vocab if v]
        return vocab

    def sub_numeros(self, sentence):
        for x in ['0','1','2','3','4','5','6','7','8','9']:
            sentence = sentence.replace(x, '?') #substitui numeros por ?
        return sentence

    def limpa_sentenca(self, sentence):
        return sentence.lower().replace(' ', '').replace('?', '').replace('.', '')
    
    security.declarePublic('get_vocabulary')
    def get_vocabulary(self, vocab_name):
        """ Gets a vocabulary. A vocabulary is represented by a list of strings."""
        property = self.__get_property_name(self.property_prefix, vocab_name)
        vocab_list = list(self.getProperty(property, []))
        sentence_list = []
        for vocabule in vocab_list:
            sentence_list.append(vocabule['sentence'])
        return sentence_list

    security.declarePublic('del_vocabulary')
    def del_vocabulary(self, vocab_name):
        """ Removes a vocabulary. """
        property = self.__get_property_name(self.property_prefix, vocab_name)
        # update property
        if hasattr(self, property):
            self.manage_delProperties((property,))

    #================================================================================
    # Metodo chamado no at_post_create_script de todo archetype que usa autocomplete
    #================================================================================
    security.declarePublic('extractFieldValues')
    def extractFieldValues(self, document):
        schema = document.schema
        default_names = ['main', 'default', 'categorization', 'dates', 'ownership', 'settings']
        schemata_names = schema.getSchemataNames()
        for name in default_names:
            schemata_names.remove(name)
        for name in schemata_names:
            fields = schema.getSchemataFields(name)
            for field in fields:
                if field.widget.getName() == 'StringWidget' or field.widget.getName() == 'TextAreaWidget':
                    self.saveStringsVocabulary(field, document)
                if field.widget.getName() == 'DataGridWidget':
                    self.saveDataGridVocabulary(field, document)
                 
    def saveStringsVocabulary(self, field, document):
        field_name = field.getName()
        field_value = []
        field_value.append(field.get(document))
        self.add_vocabulary(field_name, field_value)
        
    def saveDataGridVocabulary(self, field, document):
        linhas = field.get(document)
        for linha in linhas:
            for key in linha:
                subfield_name = "dg_"+key
                subfield_value = []
                subfield_value.append(linha[key])
                if key not in self.dg_ignored_subfields:
                    self.add_vocabulary(subfield_name, subfield_value)
        

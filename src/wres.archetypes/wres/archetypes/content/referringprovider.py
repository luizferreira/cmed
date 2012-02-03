# coding=utf-8
"""Definition of the ReferringProvider content type
"""

from zope.interface import implements
from zope.app.component.hooks import getSite
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

from wres.archetypes.interfaces import IReferringProvider
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.schemas.referringprovider import ReferringProviderSchema

def create_base_of_id(first_name, last_name):
    """ Essa função cria o id do usuário com base
    no seu nome e sobrenome
    Chamada por create_id()
    """
    import re
    pattern = re.compile('[a-z\d]')
    filter_func = lambda c: re.match(pattern, c)
    fname_filtered = filter(filter_func, first_name.lower())
    lname_filtered = filter(filter_func, last_name.lower())
    return fname_filtered[:1] + lname_filtered


def create_id(portal_registration, first_name, last_name):
    """ Essa função testa se o id já está em uso e caso
    afirmativo concatena um número ao id para desambiguação
    Chamada por generateNewId()
    """
    portal = getSite()
    resolvido = False
    base = create_base_of_id(first_name, last_name)
    new_id = base
    num = 0
    pr = portal_registration
    rp_folder = portal['Referring Providers']
    while not resolvido:
        try:
            tentativa = rp_folder[new_id]
            num += 1
            new_id = "%s%s" % (base, num)        
        except:
            resolvido = True;
    while not pr.isMemberIdAllowed(new_id):
        num += 1
        new_id = "%s%s" % (base, num)
    return new_id
    

class ReferringProvider(folder.ATFolder):
    """Type Referring Provider for WRES website"""
    implements(IReferringProvider)

    meta_type = "ReferringProvider"
    schema = ReferringProviderSchema

    def getFullName(self):
        return self.Title()

    def at_post_create_script(self):
        self.setId(self.generateNewId())

    def generateNewId(self):
        """ Create an id based on the last name of an user.
        """
        lname = self.getLastName()
        fname = self.getFirstName()
        old_id = self.getId()
        pm = getToolByName(self, 'portal_membership')
        if not pm.getMemberById(old_id):
            pr = getToolByName(self, 'portal_registration')
            return create_id(pr, fname, lname)
        else:
            return old_id

    def getParsedLastName(self):
        """
        Utilizado para indexar o parsedLastName do tipo
        """
        from wres.policy.utils.utils import do_transformation
        return do_transformation(self.getLastName())     

atapi.registerType(ReferringProvider, PROJECTNAME)

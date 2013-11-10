## coding=utf-8

import transaction
from Products.CMFPlone.utils import _createObjectByType
from AccessControl import Unauthorized
from wres.policy.utils.roles import *

def getOrCreateType(portal, atobj, newid, newtypeid):
    """
    Gets the object specified by newid if it already exists under
    atobj or creates it there with the id given in newtypeid
    """
    try:
        newobj = getattr(atobj,newid) #get it if it already exists
    except AttributeError:  #newobj doesn't already exist
        try:
            _ = atobj.invokeFactory(id=newid,type_name=newtypeid)
        except ValueError:
            _createObjectByType(newtypeid, atobj, newid)
        except Unauthorized:
            _createObjectByType(newtypeid, atobj, newid)
        newobj = getattr(atobj,newid)
    return newobj

def create_configuration_folder(context):
    """ Cria a pasta de configuracao """
    portal = context.getParentNode()
    print '*** Criando pasta de configuracao...'
    configuration_folder = getOrCreateType(portal, portal, 'configuration', 'CmedConfiguration')
    configuration_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE], acquire = False)
    configuration_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE], acquire = False)
    configuration_folder.setTitle('Configurações')
    configuration_folder.setExcludeFromNav(True)
    configuration_folder.reindexObject()
    print '*** Criando pasta de configuracao...... OK'

    transaction.commit()
    print "..."
    print "Pronto!\n"

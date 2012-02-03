from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.Archetypes.public import process_types, listTypes
from Products.Archetypes.atapi import *
from Products.validation.config import validation

from config import *

registerDirectory(SKINS_DIR, GLOBALS)

from zope.i18nmessageid import MessageFactory as BaseMessageFactory
MessageFactory = BaseMessageFactory('wres.brfields')

from wres.brfields import validators

def initialize(context):
    
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)
    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
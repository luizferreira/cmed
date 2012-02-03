# coding=utf-8

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.CMFCore.utils import getToolByName

from wres.archetypes.interfaces import IReviewOfSystems
from wres.archetypes.config import PROJECTNAME

from wres.archetypes.content.schemas.reviewofsystems import ReviewOfSystemsSchema

class ReviewOfSystems(base.ATCTContent):

    implements(IReviewOfSystems)

    meta_type = "ReviewOfSystems"
    schema = ReviewOfSystemsSchema
    
    def at_post_create_script(self):
        self.setTitle('Revisão dos Sistemas')
        vt = getToolByName(self, 'vocabulary_tool')
        vt.extractFieldValues(self)

atapi.registerType(ReviewOfSystems, PROJECTNAME)

# coding=utf-8

"""Definition of the Encounter content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from wres.archetypes.interfaces import IEncounter
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.schemas.encounter import EncounterSchema

schemata.finalizeATCTSchema(
    EncounterSchema,
    folderish=True,
    moveDiscussion=False
)


class Encounter(folder.ATFolder):
    """Description of the Example Type"""
    implements(IEncounter)

    meta_type = "Encounter"
    schema = EncounterSchema

#    title = atapi.ATFieldProperty('title')
#    description = atapi.ATFieldProperty('description')

#    def Title(self):
#        date_of_visit = self.getDate_of_visit()
#        if date_of_visit is not None:
#            return date_of_visit.strftime('%d/%m/%Y')#alterado para o formato brasileiro
#        else:
#            date_of_visit = self.Date()
#            return self.setDate_of_visit(date_of_visit)

#    def saveNote(self, note):
#        self.note = note

#    def getNote(self):
#        if not hasattr(self, 'note'):
#            self.saveNote('')
#        return self.note
    
#    def saveStatus(self, status):
#        self.status = status

#    def getStatus(self):
#        if not getattr(self, 'status', False):
#            self.saveStatus('pending')
#        return self.status

#    def parent_address(self):
#        return self.aq_parent.absolute_url()

#    def _append_uid_to_field(self, field, uid):
#        field = self.Schema().getField(field)
#        relationship = field.relationship
#        rc = self.reference_catalog
#        rc.addReference(self, uid, relationship, referenceClass=Reference)

#    def append_visit(self, uid):
#        self._append_uid_to_field('visit', uid)

#    def append_related_document(self, uid):
#        self._append_uid_to_field('related_documents', uid)
##        field = self.Schema().getField('related_documents')
##        relationship = field.relationship
##        rc = self.reference_catalog
##        rc.addReference(self, uid, relationship, referenceClass=Reference)

#    def patient_visits(self):
#        chart = self.getChart()
#        pc = self.schedule_catalog
#        query = {'meta_type': 'Visit', 'getChart': chart,
#                 'review_state': ['concluded', 'running',] }
#        brains = pc.search(query, sort_index='start')
#        def title(brain):
#            date = brain.start
#            return date.strftime('%d/%m/%Y - %I:%M %p')#alterado para o formato brasileiro
#        return [(b.UID, title(b)) for b in brains]

atapi.registerType(Encounter, PROJECTNAME)

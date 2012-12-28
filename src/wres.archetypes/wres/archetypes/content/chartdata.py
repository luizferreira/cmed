##coding=utf-8

from Persistence import Persistent
from BTrees.OOBTree import OOBTree
from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

class EventBrain:
    """
    persisted in event_catalog.
    """
    def __init__(self, event):
        self.event = event
        for metadata in event.metadata:
            setattr(self, metadata, getattr(event, metadata))
        self.review_state = ''

    def getObject(self):
        '''
        search catalog for Patient with id self.patient_id
        events = patient.get_events()
        return events[self.id]

        '''
        return self.event

class Event:
    '''
    cmed event, similar to encounter concept.
    '''
    __allow_access_to_unprotected_subobjects__ = 1
    '''
    EVENT TYPES
    '''
    # EVENT TYPES
    CREATION = 1000

    # set as attributes for EventBrain instances.
    metadata = ['date_year', 'date_month', 'date_day', 'related_object_id',
                'path', 'patient_id', 'id', 'event_type', 'meta_type']

    def __init__(self, patient, ev_type, date, related_obj, author=None):
        '''
        author param is used only in migration of ChartItemEventWrapper's
        '''
        self.portal = getSite()
        self.cct = getToolByName(self.portal, 'cmed_catalog_tool')
        self.patient_id = patient.getId()
        self.date = date
        self.related_obj = related_obj
        # author input keyword param is seted only when importing ChartDataItemWrapper's
        if author:
            self.author = author
        else:
            self.author = related_obj.getOwner().getId()

        self.type = ev_type

        # indexes and metadata
        # self.event_text = self.eprint() # commenting: this is problemetic when migrating, since the object isnt in catalog yet. (ATBlob early creation)
        self.date_year = date.year()
        self.date_month = date.month()
        self.date_day = date.day()
        self.path = self.event_url()
        self.event_type = self.type
        self.meta_type = self.related_obj.meta_type
        self.related_object_id = self.related_obj.getId()

        # this attributes gonna replace self.related_obj soon.
        # we gonna do this cause a reference for an object is not the right thing to do, in many
        # cases can lead to bugs difficult to debug. ro = related_object.
        # self.ro_id = self.related_obj.getId()
        # self.ro_uid = self.related_obj.UID()
        # self.ro_meta_type = self.related_obj.meta_type

        self.catalog_me()

    def catalog_me(self):
        '''
        index an event (through an EventBrain) in event_catalog.
        '''
        self.id = self.cct.event_catalog_map.new_docid()
        self.cct.event_catalog_map.add(EventBrain(self), self.id)
        self.cct.event_catalog.index_doc(self.id, self)

    def get_contextualized_object(self):
        '''
        Used to workaround the problem of objects that getPhysicalPath doesnt work
        properly. Returns a catalog brain object.
        '''
        uid = self.related_obj.UID()
        portal_catalog = self.portal.portal_catalog
        return portal_catalog.search(dict(UID=uid))[0]

    def event_url(self):
        '''
        used to solve a problem in some urls with absolute_url_path().
        '''
        portal_url = '/'.join(self.portal.getPhysicalPath())
        patient_url = portal_url + '/Patients/' + self.patient_id
        chart_url = patient_url + '/chartFolder_hidden'

        if self.related_obj.meta_type == 'ChartItemEventWrapper':
            return chart_url + self.related_obj.url_sufix
        else:
            return self.get_contextualized_object().getPath()

    def eprint(self):
        '''
        returns html to be printed in screen
        '''
        if self.related_obj.meta_type == 'Visit':
            related_obj = "<a target=\"_blank\" href=\"" + self.event_url() + "\" >" + self.related_obj.getVisit_type() + "</a>"
        else:
            related_obj = "<a target=\"_blank\" href=\"" + self.event_url() + "\" >" + self.related_obj.Title() + "</a>"
        return self.prefix() + related_obj + self.posfix()

    def prefix(self):
        '''
        called by eprint.
        '''
        # necessary to be here (and not in the header), since medicaldocument import chartdata too.
        from wres.archetypes.content.medicaldocument import MedicalDocument
        if self.type == Event.CREATION:
            if self.related_obj.meta_type == 'Visit':
                return ''
            elif self.related_obj.meta_type == 'Patient':
                return 'Paciente '
            elif isinstance(self.related_obj, ChartItemEventWrapper):
                return self.related_obj.prefix
            elif isinstance(self.related_obj, MedicalDocument):
                return 'Documento '
            elif self.related_obj.portal_type == 'Image':
                return 'Imagem '
            elif self.related_obj.portal_type == 'File':
                return 'Arquivo '
        return ''

    def posfix(self):
        '''
        called by eprint
        '''
        if self.type == Event.CREATION:
            if self.related_obj.meta_type == 'Visit':
                return self._visit_review_state()
            else:
                return ' adicionado.'

    def getAuthor(self):
        '''
        If not admin, return the related object of the self.author.
        '''
        # admin doesnt have a member neither a related_object.
        if self.author == 'admin':
            return 'admin'
        mt = getToolByName(self.portal, 'portal_membership')
        member = mt.getMemberById(self.author)
        return self.portal.unrestrictedTraverse(member.getProperty('related_object'))

    def _visit_review_state(self):
        '''
        used only for visits.
        '''
        pw = getToolByName(self.portal, 'portal_workflow')
        wf = getattr(pw, 'appointment_workflow')
        pc = getToolByName(self.portal, 'portal_catalog')
        brains = pc.search({'id':self.related_obj.getId()})
        if len(brains) > 1:
            raise Exception('I found more than 1 visit with the same id.')
        brain = brains[0]
        state = getattr(wf.states, brain.review_state)
        return ' (' + state.title_or_id().lower() + ').'

    def _event_cmp(ev1, ev2):
        '''
        used for sorting events in patient.py
        '''
        if ev1.date < ev2.date:
            return -1
        if ev1.date == ev2.date:
            return 0
        else:
            return 1

    def export_dict(self):
        '''
        function that transform an event instance in a dictionary to be exported.
        '''
        if isinstance(self.related_obj, ChartItemEventWrapper):
            return {'type': self.type, 'date': self.date, 'author': self.author, 'related_obj' : self.related_obj.meta_type,
                    'mapping_name' : self.related_obj.mapping_name,  'prefix' : self.related_obj.prefix,
                    'title' : self.related_obj.title, 'url_sufix' : self.related_obj.url_sufix,}
        else:
            return {'type': self.type, 'date': self.date, 'author': self.author, 'related_obj' : self.related_obj.getId()}


class ChartItemEventWrapper:
    '''
    wrapper for creating chart_data events.
    '''
    meta_type = 'ChartItemEventWrapper'
    def __init__(self, mapping_name, patient, **object):
        if mapping_name == 'medications':
            self.prefix = 'Medicamento '
            self.title = object['medication']
            self.url_sufix = '/show_medications'
        elif mapping_name == 'problems':
            self.prefix = 'Diagnóstico '
            self.title = object['problem']
            self.url_sufix = '/show_problem_list'
        elif mapping_name == 'allergies':
            self.prefix = 'Alergia '
            self.title = object['allergy']
            self.url_sufix = '/show_allergies'
        elif mapping_name == 'laboratory':
            self.prefix = 'Exame '
            self.title = object['exam']
            self.url_sufix = '/show_exams'
        elif mapping_name == 'prescriptions':
            self.prefix = ''
            self.title = 'Prescrição'
            self.url_sufix = '/show_medications'
        self.mapping_name = mapping_name
        self.patient = patient
        self.id = self.patient.getId() + '_' + mapping_name + '_' + self.title

    def getId(self):
        return self.id

    def getOwner(self):
        portal = getSite()
        return getToolByName(portal, 'portal_membership').getAuthenticatedMember()

    def Title(self):
        return self.title

    # TODO: Remover a partir de 01/04/2013
    # def absolute_url_path(self):
    #     chart_folder = self.patient.chartFolder
    #     return chart_folder.absolute_url_path() + self.url_sufix

class ChartData(Persistent):
    __allow_access_to_unprotected_subobjects__ = 1
    #TODO alguns atributos nao estao sendo usados. Limpar posteriormente.
    mapping = {
               'allergies': OOBTree,
               'not_signed_allergies': OOBTree,
               'medications': OOBTree,
               'review_of_systems': OOBTree,
               'problems': OOBTree,
               'prescriptions': OOBTree,
               'events': OOBTree,
               'laboratory': OOBTree,
              }

    security = ClassSecurityInfo()
    def __init__(self):
        self.clean_chart()

    def clean_chart(self):
        mapping = self.mapping
        for key, value in mapping.items():
            setattr(self, key, value())

    def update_chart(self):
        mapping = self.mapping
        for key, value in mapping.items():
            if not hasattr(self, key):
                setattr(self, key, value())

    def raise_event(self, context, mapping_name, type, **object):
        '''
        type 1 == creation
        type 2 == edition (not implemented yet)
        '''
        # related_obj is a wrapper for the event related with the chart_data.
        related_obj = ChartItemEventWrapper(mapping_name, context, **object)
        context.create_event(Event.CREATION, DateTime(), related_obj)


    def save_entry(self, context, mapping_name, **object):
        '''
        save the entry in the mapping attribute of chart_data.
        '''
        # parameter 1 means that is a creation. context is usually a patient.
        self.raise_event(context, mapping_name, 1, **object)
        mappings = getattr(self, mapping_name)
        entry = {'date': DateTime(), 'came_from': 'template'}
        id = context.generateUniqueId(mapping_name)
        object['id'] = id
        entry['id'] = id
        entry['data'] = object
        mappings[id] = entry
        return id

    #Edita um item do atributo mappings do chart_data
    def edit_entry(self, id, mapping_name, **data):
        mappings = getattr(self, mapping_name)
        object = mappings[id]
        for key, value in data.items():
            object[key] = value
        mappings[id] = object

    #Pega um atributo completo do mappings em chart_data
    def get_entry(self, mapping_name):
        return dict(getattr(self, mapping_name))

    #Pega um item do atributo mappings do chart_data
    def get_entry_item(self, id, mapping_name):
        mappings = getattr(self, mapping_name)
        return mappings[id]

InitializeClass(ChartData)

# coding=utf-8

from DateTime import DateTime
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from zope.app.component.hooks import getSite
from Products.Archetypes import PloneMessageFactory as _

from BTrees.Length import Length

from Products.Archetypes.utils import DisplayList
from Products.Archetypes.Registry import setSecurity
from Products.Archetypes.interfaces.vocabulary import IVocabulary

import unicodedata
import logging

#===============================================================================
# Esse método é necessário para contornar o validador que define que startDate precisa
# ser menor que endDate.
# Luiz
#===============================================================================
def endDateDefaultMethod():
    return DateTime(2100, 1, 1)

#===============================================================================
# Essa função foi criada para remover campos desnecessários do schema de classes
# derivadas da BaseFolder. Através dela, conseguimos evitar a exibição dos
# schematas default e metadata do BaseFolderSchema. Recebe como parâmetro o
# schema base, de onde serão tirados os campos desnecessários. Obs. Essa função
# foi criada para ser utilizada com schemas do baseados no ATFolderSchema, que
# é o caso do WRESUserSchema.
# non_eclude_schematas: lista de schematas dentre os default que nao eh para
#   retirar.
# non exclude_fields: lista de fields dentro dos schematas default que nao eh
#   para retirar.
# Luiz
#===============================================================================
def finalizeSchema(baseSchema, type='None', non_exclude_schematas=[], non_exclude_fields=[]):
    newSchema = baseSchema
    newSchema['id'].required = 1
    #olhar essa questao da permissao posteriormente
    #newSchema['id'].read_permission = VIEW_PATIENT
    #newSchema['id'].write_permission = EDIT_PATIENT
    newSchema['id'].schemata = 'main'
    newSchema['id'].widget=IdWidget(label='User Id',
                                    label_msgid='cmfuemr_label_user_id',
                                    i18n_domain='cmfuemr',
                                    visible={'edit':'invisible',
                                             'view':'invisible'})


    newSchema['description'].widget = TextAreaWidget(
                                                    label=_(u'label_description', default=u'Description'),
                                                    description=_(u'help_description',
                                                        default=u'Used in item listings and search results.'),
                                                    rows='2',
                                                    )


    #- Esconde os fields dos schematas default, categorization, dates, ownership
    #---------------------------------------------------------------- e settings

    # Esconde os fields dos schematas default, categorization, date, ownership
    # e settings.

    if type == 'Visit':
        fields = newSchema.getSchemataFields('default')
        for field in fields:
            field_name = field.getName()
            if field_name is not 'startDate' and field_name is not 'endDate':
                field.widget.visible = {'edit': 'invisible', 'view': 'invisible'}
            else:
                if field_name is 'startDate':
                    field.widget.label = u'Início da Consulta'
                else:
                    field.required = False
                    field.widget.label = u'Final da Consulta'
                    field.default_method = endDateDefaultMethod
                    field.widget.visible = {'edit': 'visible', 'view': 'visible'}
    else:
        if 'default' not in non_exclude_schematas:

            newSchema['title'].required = 0
#            newSchema['title'].searchable = 0
#            newSchema['title'].schemata = 'main'
#            newSchema['title'].widget = StringWidget(visible={'edit':'invisible',
#                                                              'view':'invisible'},
#                                                     label='title',
#                                                     label_msgid='cmfuemr_label_title',
#                                                     i18n_domain='cmfuemr')
            #newSchema['description'].searchable = 0


            fields = newSchema.getSchemataFields('default')
            for field in fields:
                if field not in non_exclude_fields:
                    field.widget.visible = {'edit': 'invisible', 'view': 'invisible'}

    if 'categorization' not in non_exclude_schematas:
        fields = newSchema.getSchemataFields('categorization')
        for field in fields:
            if field not in non_exclude_fields:
                field.widget.visible = {'edit': 'invisible', 'view': 'invisible'}

    if 'dates' not in non_exclude_schematas:
        fields = newSchema.getSchemataFields('dates')
        if field not in non_exclude_fields:
            for field in fields:
                field.widget.visible = {'edit': 'invisible', 'view': 'invisible'}

    if 'ownership' not in non_exclude_schematas:
        fields = newSchema.getSchemataFields('ownership')
        if field not in non_exclude_fields:
            for field in fields:
                field.widget.visible = {'edit': 'invisible', 'view': 'invisible'}

    if 'settings' not in non_exclude_schematas:
        fields = newSchema.getSchemataFields('settings')
        if field not in non_exclude_fields:
            for field in fields:
                field.widget.visible = {'edit': 'invisible', 'view': 'invisible'}

    return newSchema

#===============================================================================
# Essa função retorna o plone site (root). Foi criada para contornar o
# problema de asserção de segurança levantada pelo getSite().
# Luiz
#===============================================================================
def getWresSite():
    return getSite()

#===============================================================================
# Essa função é utilizada no processo de 'Quick Register'
# Luiz
#===============================================================================
def createVisitObject(context, id):
    from wres.archetypes.content.visit import Visit
    visit = Visit(id)
    return visit.__of__(context)

def asc2Filter(string):
    '''
    transform a string to asc2. Ex:
    if string = 'jassumção', returns jassumpcao.
    '''
    char_map = {'á':'a', 'â':'a', 'ã':'a', 'é':'e', 'ê':'e', 'í':'i', 'ó':'o', 'ô':'o', 'ú':'u', 'ç':'c'}
    new_string = ''
    i = 0
    while i < len(string):
        if ord(string[i]) == 195: #identifies a non asc2 character
            try:
                character = string[i:i+2]
            except:
                raise Exception('Sorry, I supposed char ord=195 always preceds another char')
            if character in char_map:
                new_string += char_map[character]
            else:
                logging.warn("'Pegue o pombo!' Special character passed (not in char_map)!")
            i += 1 # used to jump 2, since special chars have lenght 2.
        else:
            new_string += string[i]
        i += 1

    # verifying
    try:
        new_string.decode('ascii')
    except UnicodeDecodeError:
        logging.warn("Sorry, seems to me that some non asc2 char passed, this will cause problmes later!")
    return new_string

def create_base_of_id(first_name, last_name):
    """ Essa função cria o id do usuário com base
    no seu nome e sobrenome
    Chamada por create_id()
    """
    first_name, last_name = (asc2Filter(first_name.lower()), asc2Filter(last_name.lower()))
    import re
    pattern = re.compile('[a-z\d]')
    filter_func = lambda c: re.match(pattern, c)
    fname_filtered = filter(filter_func, first_name)
    lname_filtered = filter(filter_func, last_name)
    return fname_filtered[:1] + lname_filtered

def create_valid_user_id(portal_registration, first_name, last_name):
    """ Essa função testa se o id já está em uso e caso
    afirmativo concatena um número ao id para desambiguação
    Chamada por generateNewId()
    """
    base = create_base_of_id(first_name, last_name)
    new_id = base
    num = 0
    pr = portal_registration
    while not pr.isMemberIdAllowed(new_id):
        num += 1
        new_id = "%s%s" % (base, num)
    return new_id

def changeFlag(object, value):
    if not hasattr(object, 'flag_change'):
        object.flag_change = Length()
    object.flag_change.set(value)

def set_schemata_properties(schemata_obj, **kwargs):
    for field in schemata_obj.fields():
        for id, value in kwargs.items():
            setattr(field, id, value)

def formatPath(tuple_path):
    string_path = ''
    for part in tuple_path:
        if part != '/':
            string_path = string_path + '/' + part
    return string_path

def get_related_user_object(context, member):
    role_folder = {'Patient': 'Patients',
                   'Secretary': 'Secretaries',
                   'Doctor': 'Doctors',
                   }
    for role, folder_id in role_folder.items():
        if member.has_role(role):
            folder = getattr(context, folder_id)
    member_id = member.id
    return getattr(folder, member_id)

def do_transformation(undone):
    import string
    new_value = [c for c in undone if c in string.letters]
    return ''.join(new_value)

def getDefaultPhotoUrl():
    return getSite().portal_skins.wres_theme_images.__getitem__('nophoto.jpeg').absolute_url()

def strip_accents(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

class LogoWrapper:
    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        request = self.REQUEST
        response = request.RESPONSE
        return self.obj.index_html(request, response)

    def __getattr__(self, attr):
        r = getattr(self.obj, attr)
        return r

class uemr_datetime:
    def __init__(self, date):
        self.__date = date
    def __getattr__(self, name):
        return getattr(self.__date, name)
    def strftime(self, format):
        return self.__date.strftime(format)

def convertDateTime2datetime(date):
    year, month, day, hour, minute, second, tz = date.parts()
    micro = 0
    second = int(second)
    dt = datetime(year, month, day, hour, minute, second, micro, None)
    return uemr_datetime(dt)

def subtractMonths(date, num_months):
    year, month, day, hour, minute, second, timezone = date.parts()
    delta_months = month - num_months
    if delta_months <= 0:
        new_year = year - 1
        new_month = 12 + delta_months
    else:
        new_year = year
        new_month = delta_months
    #the while below is a hack to handle cases like: date=31/12/2006,
    #num_months=1, that would give as result 31/11/2006, an invalid date
    while True:
        try:
            result = DateTime(new_year, new_month, day, hour, minute, second,
                              timezone)
            break
        except DateTime.DateError:
            day = day - 1
    return result

def getObjWorkflowStatus(portal_workflow, obj):
    review_state = portal_workflow.getInfoFor(obj, 'review_state', '')
    portal_type = obj.portal_type
    workflow_id = portal_workflow.getChainForPortalType(portal_type)[0]
    return getWorkflowStatus(portal_workflow, workflow_id, review_state)

def getWorkflowStatus(portal_workflow, workflow_id, review_state):
    workflow_state = getWorkflowStateObject(portal_workflow, workflow_id,
                                            review_state)
    return workflow_state.title_or_id()

class FakeWorkflowState:
    def title_or_id(self):
        return ''

def getWorkflowStateObject(portal_workflow, workflow_id, state_id):
    if workflow_id and state_id:
        return portal_workflow[workflow_id].states[state_id]
    else:
        return FakeWorkflowState()

def getPortalObject(obj):
    return getToolByName(obj, 'portal_url').getPortalObject()

def event_between(event, start, end):
    eventstart = DateTime(str(event.start))
    #eventstart >= start && eventstart <= end
    return eventstart.greaterThanEqualTo(start) and \
           eventstart.lessThanEqualTo(end)

def filter_events_between(events, start, end):
    return filter(lambda x: event_between(x, start, end), events)

def event_before(event, slot):
    eventstart = DateTime(str(event.start))
    eventend = DateTime(str(event.end))
    #eventstart < slot && eventend > slot
    return eventstart.lessThan(slot) and \
           eventend.greaterThan(slot)

def filter_events_before(events, start):
    return filter(lambda x: event_before(x, start), events)

def getHourEvents(day_events, hour):
    str_ymdh = "%s/%s/%s %s" % (hour.year(), hour.month(), hour.day(),\
                                hour.hour())
    hour_start = DateTime(str_ymdh + ":00:00")
    hour_end = DateTime(str_ymdh + ":59:59")
    events_before = filter_events_before(day_events, hour_start)
    events_between = filter_events_between(day_events, hour_start, hour_end)
    return events_before + events_between

def getSlotEvents(hour_events, hour, minute, slot_size):
    str_ymdh = "%s/%s/%s %s" % (hour.year(), hour.month(), hour.day(),\
                                hour.hour())
    slot_start = DateTime(str_ymdh + ":%s:00" % mk2d(minute))
    slot_end = DateTime(str_ymdh + ":%s:59" % mk2d(minute + slot_size - 1))
    events_before = filter_events_before(hour_events, slot_start)
    events_between = filter_events_between(hour_events, slot_start, slot_end)
    return events_before + events_between

def mk2d(num):
    str_num = str(num)
    if len(str_num) == 1:
        return '0%s' % num
    else:
        return str_num

def getFieldVocabularyValue(obj, field_id):
    field = obj.getField(field_id)
    accessor_id = field.accessor
    accessor = obj[accessor_id]
    vocabulary = field.Vocabulary(obj)
    return vocabulary.getValue(accessor())

# Retorna um nome pre-definido associado ao vocabulario;
# Se o usuario define um outro nome, esse valor e retornado do field
def getFieldVocabularyName(obj, field_id):
    vocabulary_value = getFieldVocabularyValue(obj, field_id)
    if not vocabulary_value:
        vocabulary_value = obj[obj.getField(field_id).accessor]()
    return vocabulary_value

""" Retorna um valor associado a uma chave do vocabuario de um subfield """
def getRecordSubfieldDisplayValue(obj, field_id, subfield_id, key, default=None):
    field = obj.getField(field_id)
    vocabulary = field.getVocabularyFor(subfield_id, instance=obj)
    value = vocabulary.getValue(key)
    if value is None:
        return default
    else:
        return value

def canSignPn(self, doctor, entered_passwd):
    error = doctor.validateSignPassword(entered_passwd)
    return error == None

class DayInformation:
    def __init__(self, date_inf):
        self._date_inf = date_inf
        self._start = 24
        self._end = 0
        self._hours = {}

    def getDateTimeInformation(self):
        return self._date_inf

    def Title(self):
        return self._date_inf.strftime("%a %m/%d")

    def getStart(self):
        return self._start

    def getEnd(self):
        return self._end

    def getSlotInformation(self, str_time):
        dt_time = DateTime(str_time)
        hour_inf = self.getHourInformation(dt_time.hour())
        return hour_inf.getSlotInformation(dt_time.minute())

    def getHourInformation(self, hour):
        if self._hours.has_key(hour):
            return self._hours[hour]
        else:
            return HourInformation(hour)

    def addHourInformation(self, hour_inf):
        dt_hour = hour_inf.getDateTimeHour()
        int_hour = dt_hour.hour()
        if self._start > int_hour:
            self._start = int_hour
        if self._end < int_hour + 1:
            self._end = int_hour + 1
        hour_inf.setParent(self)
        self._hours[int_hour] = hour_inf

class HourInformation:
    def __init__(self, hour):
        self._hour = hour
        self._slots = []
        self._parent = None

    def setParent(self, day_inf):
        self._parent = day_inf

    def getParent(self):
        return self._parent

    def getDateTimeHour(self):
        return self._hour

    def getSlots(self):
        return self._slots

    def getSlotInformation(self, minute):
        current = SlotInformation(minute)
        for slot in self._slots:
            if slot.getMinute() > minute:
                break
            elif slot.getMinute() < minute:
                current = slot
            else:
                return slot
        return current

    def addSlotInformation(self, slot_inf):
        """ """
        slot_inf.setParent(self)
        self._slots.append(slot_inf)

class SlotInformation:
    def __init__(self, minute, filled=False, activity='', activity_name=''):
        self._title = mk2d(minute)
        self._minute = minute
        self._filled = filled
        self._activity_name = activity_name
        self._activity = activity
        self._parent = None
        self._events = []

    def Title(self):
        return self._title

    def getMinute(self):
        return self._minute

    def setEvents(self, events):
        self._events = events

    def getEvents(self):
        return self._events

    def isFilled(self):
        return (self._events != [])

    def setActivityName(self, activity_name):
        self._activity_name = activity_name

    def getActivityName(self):
        return self._activity_name

    def setActivity(self, activity):
        self._activity = activity

    def getActivity(self):
        return self._activity

    def allowedActivity(self):
        return self.getActivity()

    def setParent(self, hour_inf):
        self._parent = hour_inf

    def getParent(self):
        return self._parent

##['slot_information', 'end', 'class', 'events_to_show', 'label', 'start',
##'appointment_time', 'has_events', 'events_before', 'events']

def getTypesOfDocument(self):
    mapping = {}

    def addEntry(specialty, key, value, display):
        if not 'neutro' in mapping:
            mapping['neutro'] = {}
        if not specialty in mapping:
            mapping[specialty] = {}
        if not key in mapping['neutro']:
            mapping['neutro'][key] = []
        if not key in mapping[specialty]:
            mapping[specialty][key] = []
        mapping[specialty][key].append({'value': value, 'display': display})
        mapping['neutro'][key].append({'value': value, 'display': display})

    """ PLASTICA """
    addEntry('plastic','progressNotes', 'ivp', 'Initial Visit Plastic Surgery')
    addEntry('plastic','consultation_folder_hidden', 'cn', 'Consultation')
    addEntry('plastic','consultation_folder', 'cn', 'Consultation')

    """ ALERGIA """
    addEntry('allergy','progressNotes', 'iv', 'Initial Visit')
    addEntry('allergy','consultation_folder_hidden', 'cn', 'Consultation')
    addEntry('allergy','consultation_folder', 'cn', 'Consultation')

    specialty= 'neutro'
    pm = getToolByName(self, 'portal_membership')
    member = pm.getAuthenticatedMember()
    if member.has_role('Doctor'):
        user_obj = get_related_user_object(self, member)
        specialty = user_obj.getSpecialty()

    obj_id =  self.aq_parent.id
    #obj_id = 'progressNotes'
    types_by_specialty = mapping.get(specialty,{})
    types_of_document = types_by_specialty.get(obj_id, [])

    return types_of_document

#==========================================================================================================
#A função abaixo é uma aproximação da real idade da pessoa, mas não conta com tratamento para anos bisextos
#Nao pode ser usada para validações
#Matheus
#==========================================================================================================
def getPatientAge(BirthDate):
    a = datetime.strptime(BirthDate.strftime("%Y/%m/%d"),"%Y/%m/%d")
    b = datetime.now()
    c = b - a
    return c.days/365

#Custom DisplayList usada em MultipleCheckboxWidget
class MyDisplayList:

    __implements__ = (IVocabulary,)

    def __init__(self, tuples):
        self.tuples = tuples

    def __getitem__(self, item):
        return self.tuples[item]

    def getDisplayList(self, instance):
        retval = [item for item in self.tuples]
        return DisplayList(retval)

    def getThirdElement(self, id):
        retval = [elem[2] for elem in self.tuples if elem[0] == id]
        if len(retval) == 0:
            return None
        return retval[0]

    def __contains__(self, id):
        retval = [elem[2] for elem in self.tuples if elem[0] == id or elem[2] == id]
        return (len(retval) != 0)

    def getTuples(self):
        return self.tuples

    def keys(self):
        return []

setSecurity(MyDisplayList, defaultAccess='allow')

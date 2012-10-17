# coding=utf-8
"""Definition of the Doctor content type
"""

from zope.app.component.hooks import getSite
from Products.CMFPlone.utils import _createObjectByType
from zope.interface import implements
from AccessControl import ClassSecurityInfo, AuthEncoding

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Solgema.fullcalendar.interfaces import ISolgemaFullcalendarProperties

from wres.archetypes.content import wresuser
from wres.archetypes.interfaces import IDoctor
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.schemas.doctor import DoctorSchema
from wres.policy.utils.roles import DOCTOR_GROUP
from wres.policy.utils.utils import asc2Filter

schemata.finalizeATCTSchema(
    DoctorSchema,
    folderish=True,
    moveDiscussion=False
)

COURSE_TYPES = atapi.DisplayList((
   ('college','Ensino Superior.'),
   ('specialization','Especialização'),
))

specialty_mapping = {
    'Não Selecionada': '',
    'Alergia e Imunologia': 'allergy',
    'Anestesiologia': 'anesthesiology',
    'Atendimento de emergência': 'emergency',
    'Cardiologia': 'cardiology',
    'Cirurgia': 'surgery',
    'Cirurgia Neurológica': 'neurological',
    'Cirurgia Plástica': 'plastic',
    'Clínica geral': 'general',
    'Dermatologia': 'dermatology',
    'Doença infecciosa': 'infectious',
    'Endocrinologia, Diabetes e Metabolismo': 'endocrinology',
    'Gastroenterologia': 'gastroenterology',
    'Geriatria': 'geriatrics',
    'Medicina familiar': 'family',
    'Medicina Física e Reabilitação': 'physical',
    'Medicina Genética': 'medical',
    'Medicina Interna': 'internal',
    'Medicina Preventiva': 'preventive',
    'Nefrologia': 'nephrology',
    'Neurologia': 'neurology',
    'Obstetrícia e Ginecologia': 'obstetrics',
    'OftalmologiaOftalmologia': 'ophthalmology',
    'Oncologia (Câncer)': 'oncology',
    'Ortopedia': 'orthopedics',
    'Otorrinolaringologia': 'otolaryngology',
    'Outro': 'other',
    'Patologia': 'pathology',
    'Pediatria': 'pediatrics',
    'Psiquiatria': 'psychiatry',
    'Radiologia': 'radiology',
    'Urologia': 'urology'
}

class Doctor(wresuser.WRESUser):
    """Doctor type for WRES website"""
    implements(IDoctor)

    meta_type = "Doctor"
    schema = DoctorSchema

    security = ClassSecurityInfo()

    security.declarePublic('add_visits_folder')
    def add_visits_folder(self):
        ''' adiciona a pasta onde serao colocadas as consultas do medico e tambem a colecao onde sera
        colocado o calendario '''
        user_id = self.getId()

        portal = getSite()

        # cria a pasta de visitas e coloca permissao 'Add portal content' (checada pelo solgema antes
        # de adicionar uma visita no calendário) apenas para Secretary, Manager e Owner. Logo depois,
        # muda-se o owner da pasta doctor_visits para o médico reponsável para que o mesmo possa
        # adicionar visitas no seu calendário.
        doctor_visits = _createObjectByType('VisitFolder', portal.Appointments, user_id)
        doctor_visits.setTitle('Dr(a) ' + self.getFullName())
        # apenas o medico correspondente (Owner) pode adicionar consulta em sua pasta de consultas.
        doctor_visits.manage_permission('Add portal content', ['Secretary', 'Manager', 'Owner'])
        doctor_visits.manage_permission('Copy or Move', ['Secretary', 'Manager', 'Owner'])
        doctor_visits.manage_permission('Delete objects', ['Manager'])

        doctor_visits.setConstrainTypesMode(1)
        portal.plone_utils.changeOwnershipOf(doctor_visits, user_id)
        collection = _createObjectByType('Topic', doctor_visits, 'Agenda')

        # configura slot padrao para 15 minutos e o intervalo de horas mostrado para 6:00-20:00.
        cal = ISolgemaFullcalendarProperties(collection)
        cal.slotMinutes = 15
        cal.minTime = '6'
        cal.maxTime = '20'

        collection.setTitle('Calendário do(a) Dr(a) ' + self.Title())
        collection.setLayout('solgemafullcalendar_view')
        # medicos e secretarias nao veem 'Edicao' e 'Criterio' na colecao.
        collection.manage_permission('Change portal topics', ['Manager'], False)
        # ninguem pode copiar, colar, recortar ou deletar um calendario.
        collection.manage_permission('Copy or Move', roles=[], acquire=False)
        collection.manage_permission('Delete objects', roles=[], acquire=False)
        criteria = collection.addCriterion('Type','ATPortalTypeCriterion')
        criteria.setValue('Visit')
        # (Maio/2012) TODO: Limpar
        # criteria2 = collection.addCriterion('Subject', 'ATSimpleStringCriterion')
        # criteria2.setValue(user_id)
        criteria2 = collection.addCriterion('path', 'ATRelativePathCriterion')
        criteria2.relativePath = '..'
        criteria3 = collection.addCriterion('Subject', 'ATSelectionCriterion')
        criteria3.setValue('CalendarShow')
        # (Maio/2012) TODO: Limpar
        # doctor_visits.setLayout('Agenda')

    def at_post_create_script(self, migration=False):
        wresuser.WRESUser.at_post_create_script(self)

        # Anonymous need to have View permission here in order to see the initial page (doctor_presentation).
        # remember that depending in what was done in setuphandlers, the anonymous will not be able to see neither.
        # This is controlled by the field 'Quero meu site profissional' in registration form.
        self.manage_permission('View', ['Manager', 'UemrAdmin', 'Doctor', 'Secretary', 'Transcriptionist', 'Patient', 'Anonymous'], acquire=False)

        self.add_visits_folder()
        if not migration:
            self.setSignPassword('senha1') #TODO gerar uma assinatura padrao randomica

    def at_post_edit_script(self):
        wresuser.WRESUser.at_post_edit_script(self)

    def getGroup(self):
        return DOCTOR_GROUP

    security.declarePublic('Title')
    def Title(self):
        """ """
        return '%s %s' %(self.getFirstName(), self.getLastName())

    security.declarePublic('asc2title')
    def asc2title(self):
        """
        Returns an forced asc2 title. Used as metadata.
        Ex input:
            title = 'Lúcio Gama'
        Ex output:
            return 'Lucio Gama'
        """
        return asc2Filter(self.Title())

    def get_home_url(self):
        portal = getSite()
        return '/'.join(portal.getPhysicalPath()) + '/Appointments/sec_desk'

    def getAppointmentsURL(self):
        portal = getSite()
        return portal.absolute_url_path() + '/Appointments/' + self.getId() + '/Agenda'

    def validateSignPassword(self, typed_pass):
        sign_password = self.getSignPassword()
        password_matches = AuthEncoding.pw_validate(sign_password, typed_pass)

        if password_matches:
            return

        return "Password doesn't match"

    def getCourseTypes(self):
        """
        Used by specialty1 and specialty2 fields.
        """
        return COURSE_TYPES

    def getSchemaFields(self):
        '''
        Used in doctor_presentaion (doctor_presentaion.py) to pass throgh an unauthorized.
        '''
        return self.schema.fields()

    def fillFirstDoctorInfo(self, info):
        '''
        Used to fill information about the first system doctor. That information is collected
        by setup_handlers in firstdoctor_info.txt file.
        '''
        full_name = info['Nome Completo'].split(' ')
        firstname = full_name[0]
        lastname = full_name[-1]
        self.setFirstName(firstname)
        self.setLastName(lastname)
        self.setSsn(info['CRM'])
        self.setPhone(info['Telefone de Contato'])
        if info['Confirmação do e-mail'] != info['Seu endereço de e-mail']:
            raise Exception("The two e-mail are different.")
        else:
            self.setEmail(info['Seu endereço de e-mail'])
        self.setSpecialty1(specialty_mapping[info['Especialidade 1']])
        self.setSpecialty2(specialty_mapping[info['Especialidade 2']])
        self.at_post_create_script()

atapi.registerType(Doctor, PROJECTNAME)

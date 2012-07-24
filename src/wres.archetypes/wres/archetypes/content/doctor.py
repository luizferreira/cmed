# coding=utf-8
"""Definition of the Doctor content type
"""

from zope.app.component.hooks import getSite
from Products.CMFPlone.utils import _createObjectByType
from zope.interface import implements
from AccessControl import ClassSecurityInfo, AuthEncoding
import logging

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Solgema.fullcalendar.interfaces import ISolgemaFullcalendarProperties

from wres.archetypes.content import wresuser
from wres.archetypes.interfaces import IDoctor
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.schemas.doctor import DoctorSchema
from wres.policy.utils.roles import DOCTOR_GROUP


schemata.finalizeATCTSchema(
    DoctorSchema,
    folderish=True,
    moveDiscussion=False
)


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
            title = Lúcio Gama
        Ex output:
            return 'Lucio Gama'
        """
        title = self.Title()
        # maybe char_map will have to be incremented in future. 
        char_map = {'á':'a', 'â':'a', 'ã':'a', 'é':'e', 'ê':'e', 'í':'i', 'ó':'o', 'ô':'o', 'ú':'u'}
        new_title = ''
        i = 0
        while i < len(title):
            if ord(title[i]) == 195: #identifies a non asc2 character
                try:
                    character = title[i:i+2]
                except:
                    raise Exception('Sorry, I supposed char ord=195 always preceds another char')
                if character in char_map:
                    new_title += char_map[character]
                else:
                    logging.warn("'Pegue o pombo!' Special character passed (not in char_map)!")
                i += 1 # used to jump 2, since special chars have lenght 2.
            else:
                new_title += title[i]
            i += 1

        # verifying
        try: 
            new_title.decode('ascii')
        except UnicodeDecodeError:
            logging.warn("Sorry, seems to me that some non asc2 char passed, this will cause problmes later!")
        return new_title        
    
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
    

atapi.registerType(Doctor, PROJECTNAME)

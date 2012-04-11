# coding=utf-8
"""Definition of the Doctor content type
"""

from zope.app.component.hooks import getSite
from Products.CMFPlone.utils import _createObjectByType
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from AccessControl import ClassSecurityInfo, AuthEncoding

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
        user_id = self.getId()
        
        portal = getSite()
        
        # cria a pasta de visitas e coloca permissao 'Add portal content' (checada pelo solgema antes 
        # de adicionar uma visita no calendário) apenas para Secretary, Manager e Owner. Logo depois,
        # muda-se o owner da pasta doctor_visits para o médico reponsável para que o mesmo possa
        # adicionar visitas no seu calendário.
        doctor_visits = _createObjectByType('VisitFolder', portal.Appointments, user_id)
        doctor_visits.setTitle('Dr(a) ' + self.getFullName())
        doctor_visits.manage_permission('Add portal content', ['Secretary', 'Manager', 'Owner'])
        doctor_visits.setConstrainTypesMode(1)
        portal.plone_utils.changeOwnershipOf(doctor_visits, user_id)
        collection = _createObjectByType('Topic', doctor_visits, 'Agenda')
        collection.setTitle('Calendário do(a) Dr(a) ' + self.Title())
        collection.setLayout('solgemafullcalendar_view')
        criteria = collection.addCriterion('Type','ATPortalTypeCriterion')
        criteria.setValue('VisitTemp')
        # criteria2 = collection.addCriterion('Subject', 'ATSimpleStringCriterion')
        # criteria2.setValue(user_id)
        criteria2 = collection.addCriterion('path', 'ATRelativePathCriterion')
        criteria2.relativePath = '..'
        criteria3 = collection.addCriterion('Subject', 'ATSelectionCriterion')       
        criteria3.setValue('CalendarShow')
        doctor_visits.setLayout('Agenda')
        self.setSignPassword('senha1') #TODO gerar uma assinatura padrao randomica        

    def at_post_create_script(self):
        wresuser.WRESUser.at_post_create_script(self)
        self.add_visits_folder()

    def getGroup(self):
        return DOCTOR_GROUP
    
    security.declarePublic('Title')
    def Title(self):
        """ """
        return '%s %s' %(self.getFirstName(), self.getLastName())
    
    def get_home_url(self):
        portal = getSite()
        return portal.absolute_url_path() + '/Appointments/sec_desk'

    def getAppointmentsURL(self):
        portal = getSite()
        return portal.absolute_url_path() + '/Appointments/' + self.getId()
    
    def validateSignPassword(self, typed_pass):
        sign_password = self.getSignPassword()
        password_matches = AuthEncoding.pw_validate(sign_password, typed_pass)

        if password_matches:
            return

        return "Password doesn't match"
    

atapi.registerType(Doctor, PROJECTNAME)

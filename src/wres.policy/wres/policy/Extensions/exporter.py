# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
import codecs

import os
import shutil
import tempfile

handlers = dict()  # model => {portal_type: handler}

def registerHandler(handler):
    '''
    register a handler for a content type.
    '''
    portal_types = handler.portal_types
    if isinstance(portal_types, str):
        portal_types = [portal_types]
    for pt in portal_types:
        handlers[pt] = handler

def export_members(plone, export_dir, verbose):
    '''
    exports portal members.
    '''

    print 'Exporting Members'
    fp = file(os.path.join(export_dir, 'members.ini'), 'w')

    acl_users = plone.acl_users
    pm = plone.portal_membership

    passwords = plone.acl_users.source_users._user_passwords

    # write data for each user registered in portal_membership
    for username in acl_users.getUserNames():
        if verbose:
            print '-> %s' % username
        user = acl_users.getUserById(username)
        member = pm.getMemberById(username)
        if member is None:
            continue
        print >>fp, '[member-%s]' % username
        print >>fp, 'username = %s' % username
        print >>fp, 'password = %s' % passwords.get(username)
        print >>fp, 'fullname = %s' % member.getProperty('fullname')
        print >>fp, 'email = %s' % member.getProperty('email')
        print >>fp, 'related_object = %s' % member.getProperty('related_object')
        print >>fp
    fp.close()

class Validation(object):

    def __init__(self, export_dir):
        self.export_dir = export_dir
        self.counters = []
        for handler in handlers.values():
            counter_name = handler.ident + '_counter' 
            setattr(self, counter_name, 0)
            if counter_name not in self.counters:
                self.counters.append(counter_name)

        fname = os.path.join(self.export_dir, 'validation' + '.ini')
        if not os.path.exists(os.path.dirname(fname)):
            os.makedirs(os.path.dirname(fname))
        self.fp = file(fname, 'a')                

    def count(self, ident):
        '''
        increment portal_type counter
        '''
        setattr(self, ident+'_counter', getattr(self, ident+'_counter')+1)

    def write(self):
        print '\n' + '-'*80
        print ' '*30 + 'VALIDATION DATA'
        for attr in dir(self):
            if attr.endswith('_validator'):
                func = getattr(self, attr)
                func()
        self.fp.close()
        print '-'*80

    def counters_validator(self):
        self.vprint('[counters_validator]')
        for attr in dir(self):
            if attr.endswith('_counter'):
                self.vprint("%s = %d" % (attr, getattr(self, attr)))
        self.vprint('\n')

    def vprint(self, string):
        print >>self.fp, string
        print string

class BaseHandler(object):

    portal_types = ()
    ident = None
    initialized = False

    def __init__(self, plone, validation, export_dir='exports', verbose=False):
        self.plone = plone
        self.portal_id = plone.getId()
        self.portal_path = plone.absolute_url(1)
        self.validation = validation
        self.export_dir = export_dir
        self.verbose = verbose
        fname = os.path.join(export_dir, self.ident + '.ini')

        # this lines will be executed once for content type, in order to create the out file.
        if not self.initialized:        
            if not os.path.exists(os.path.dirname(fname)):
                os.makedirs(os.path.dirname(fname))
            self.fp = file(fname, 'a')
            self.initialized = True        

    def __del__(self):
        self.fp.close()

    def _get_objects(self, portal_type):
        brains = self.plone.portal_catalog(portal_type=portal_type, show_all=1, show_inactive=1)
        for brain in brains:
            try:
                obj = self.plone.unrestrictedTraverse(brain.getPath())
            except:
                print '***OCORREU UM ERRO***'
                print brain.getPath()
                pass
            obj_path = brain.getPath()
            folder_path = obj_path.replace(self.portal_path, '')[1:]
            yield obj, obj_path, folder_path

    def write_common(self, obj, folder_path, raw_data=False):
        ''' 
        write common fields like title, id, path, etc.
        '''
        def fix_oneline(s):
            '''
            clean possible windows shit
            '''
            s = s.replace('\r\n', ' ')
            s = s.replace('\n', ' ')
            return s

        from Products.CMFCore.WorkflowCore import WorkflowException

        # get workflow state.
        wf_tool = obj.portal_workflow
        try:
            review_state = wf_tool.getInfoFor(obj, 'review_state')
        except WorkflowException:
            review_state = ''

        description = obj.Description()

        # write the fields in .ini format
        print >>self.fp, '[%s-%s]' % (self.ident, obj.absolute_url(1))
        print >>self.fp, 'path = %s' % folder_path.lstrip('/')
        print >>self.fp, 'id = %s' % obj.getId()
        print >>self.fp, 'UID = %s' % obj.UID()
        print >>self.fp, 'title = %s' % fix_oneline(obj.Title())
        print >>self.fp, 'Description = %s' % fix_oneline(description)
        print >>self.fp, 'owner = %s' % obj.getOwner()
        print >>self.fp, 'review-state = %s' % review_state
        print >>self.fp, 'created = %f' % obj.created().timeTime()
        print >>self.fp, 'effective = %f' % obj.effective().timeTime()
        print >>self.fp, 'expires = %f' % obj.expires().timeTime()
        print >>self.fp, 'subjects = %s' % ','.join(obj.Subject())

        text_format = None
        if hasattr(obj, 'text_format'):
            text_format = obj.text_format
            self.write('text-format', text_format)

        # content-type:
        ct = None
        try:
            ct = obj.getContentType()
        except AttributeError:
            ct = obj.content_type()
        if ct is not None: 
            if text_format in ('html', 'structured-text'):
                ct = 'text/html'
            self.write('content-type', ct)

        # optional raw_data exporter. None of this is currently used (but maybe in the future)
        if raw_data:
            schema = obj.Schema()
            for field in schema.fields():
                field_class = field.__class__.__name__
                if 'ImageField' in field_class or 'FileField' in field_class:
                    continue
                accessor = field.accessor
                try:
                    value = getattr(obj, accessor)()
                except:
                    continue
                print >>self.fp, 'raw_%s = %s' % (field.getName(), value)

    def write_leadout(self):
        '''
        sections separator. 
        '''
        print >>self.fp

    def write_binary(self, data, suffix='', key='filename'):
        '''
        used to export raw things, like images, files, body text, etc.
        '''
        dirpath = os.path.join(self.export_dir, self.ident)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        tempf = tempfile.mktemp(dir=dirpath) + suffix
        open(tempf, 'wb').write(str(data))
        self.write(key, os.path.abspath(tempf))


    def write(self, key, value):
        '''
        wrapper to the print function
        '''
        print >>self.fp, '%s = %s' % (key, value)

    def export(self, portal_type):
        '''
        function called right after the initialization to perform
        the exportation de facto.
        '''

        print 'Exporting %s' % portal_type

        for obj, obj_path, folder_path in self._get_objects(portal_type):
            if self.verbose:
                print '-> %s' % obj_path

            if getattr(self, 'folderish', False):
                self.write_common(obj, '/'.join(folder_path.split('/')[:-1]))
            else:
                self.write_common(obj, folder_path)

            # calls the type especific import step.
            if hasattr(self, 'export2'):
                self.export2(obj)
            self.write_leadout()

            # increment validation counter
            self.validation.count(self.ident)

class ClinicHandler(BaseHandler):
    portal_types = ('Clinic')
    ident = 'clinic'
    folderish = False

    def export2(self, obj):
        ''' especific Secretary fields'''
        self.write('name ', obj.getName())
        self.write('endereco ', obj.getEndereco())
        self.write('phone ', obj.getPhone())
        self.write('fax ', obj.getFax())
        self.write('email ', obj.getEmail())

registerHandler(ClinicHandler)

class PatientHandler(BaseHandler):
    portal_types = ('Patient')
    ident = 'patient'
    folderish = True

    def export2(self, obj):
        ''' especific Patient fields'''
        self.write('firstName ', obj.getFirstName())
        self.write('lastName ', obj.getLastName())
        self.write('birthDate ', obj.getBirthDate())
        self.write('email ', obj.getEmail())
        self.write('homePhone ', obj.getHomePhone())
        self.write('mobile ', obj.getMobile())
        self.write('contactPhone ', obj.getContactPhone())
        self.write('sex ', obj.getSex())
        self.write('address1 ', obj.getAddress1())
        self.write('address2 ', obj.getAddress2())
        self.write('city ', obj.getCity())
        self.write('state ', obj.getState())
        self.write('chart ', obj.getChart())
        doctor = obj.getDoctor()
        if doctor is not None:
            self.write('doctor ', doctor.getId())
        else:
            self.write('doctor ', '')
        self.write('socialSecurity ', obj.getSocialSecurity())
        self.write('identidade ', obj.getIdentidade())
        self.write('orgaoEmissor ', obj.getOrgaoEmissor())
        self.write('zipcode ', obj.getZipcode())
        self.write('pis_pasep ', obj.getPis_pasep())
        self.write('CTPS ', obj.getCTPS())
        self.write('tituloEleitor ', obj.getTituloEleitor())
        self.write('tipo ', obj.getTipo())
        self.write('convenio ', obj.getConvenio())
        self.write('matricula ', obj.getMatricula())
        self.write('titular ', obj.getTitular())
        self.write('cartaoNacionalDeSaude ', obj.getCartaoNacionalDeSaude())
        self.write('nomeDoPai ', obj.getNomeDoPai())
        self.write('nomeDaMae ', obj.getNomeDaMae())
        self.write('nacionalidade ', obj.getNacionalidade())
        self.write('race ', obj.getRace())
        self.write('maritalStatus ', obj.getMaritalStatus())
        self.write('educationCompleted ', obj.getEducationCompleted())
        self.write('employerName ', obj.getEmployerName())
        self.write('industry ', obj.getIndustry())
        self.write('occupationTitle ', obj.getOccupationTitle())
        self.write('status ', obj.getStatus())
        self.write('workPhone ', obj.getWorkPhone())
        self.write('extension ', obj.getExtension())
        self.write('fax ', obj.getFax())
        self.write('retirementdate ', obj.getRetirementdate())
        image = obj.getPhoto()
        if image != '':
            self.write_binary(str(image.data))
        chart_summary = obj.chart_data_summary()
        self.write('chartdata ', chart_summary)

registerHandler(PatientHandler)

class SecretaryHandler(BaseHandler):
    portal_types = ('Secretary')
    ident = 'secretary'
    folderish = True

    def export2(self, obj):
        ''' especific Secretary fields'''
        self.write('isTranscriptionist ', obj.getIsTranscriptionist())
        self.write('firstName ', obj.getFirstName())
        self.write('lastName ', obj.getLastName())
        self.write('ssn ', obj.getSsn())
        self.write('email ', obj.getEmail())
        self.write('address1 ', obj.getAddress1())
        self.write('city ', obj.getCity())
        self.write('state ', obj.getState())
        self.write('phone ', obj.getPhone())
        self.write('cel ', obj.getCel())

registerHandler(SecretaryHandler)

class DoctorHandler(BaseHandler):
    portal_types = ('Doctor')
    ident = 'doctor'
    folderish = True

    def export2(self, obj):
        ''' especific Doctor fields'''
        self.write('professional ', obj.getProfessional())
        self.write('ssn ', obj.getSsn())
        self.write('firstName ', obj.getFirstName())
        self.write('lastName ', obj.getLastName())
        self.write('street1 ', obj.getStreet1())
        self.write('street2 ', obj.getStreet2())
        self.write('city ', obj.getCity())
        self.write('state ', obj.getState())
        self.write('zipcode ', obj.getZipcode())
        self.write('website ', obj.getWebsite())
        self.write('phone ', obj.getPhone())
        self.write('cel ', obj.getCel())
        self.write('fax ', obj.getFax())
        self.write('email ', obj.getEmail())
        self.write('initial ', obj.getInitial())
        self.write('signature ', obj.getSignature())
        self.write('credentials ', obj.getCredentials())
        self.write('specialty ', obj.getSpecialty())
        self.write('signPassword ', obj.getSignPassword())

registerHandler(DoctorHandler)

class VisitHandler(BaseHandler):
    portal_types = ('Visit')
    ident = 'visit'
    folderish = False

    def export2(self, obj):
        ''' especific Visit fields'''
        patient = obj.getPatient()
        if patient != None:
            self.write('patient ', patient.getId())
        else:
            self.write('patient ', '')
        self.write('start-date ', obj.start().timeTime())
        self.write('end-date ', obj.end().timeTime())
        self.write('duration ', obj.getDuration())
        self.write('contactPhone ', obj.getContactPhone())
        self.write('visit_type ', obj.getVisit_type())
        self.write('visit_reason ', obj.getVisit_reason())

registerHandler(VisitHandler)

class TemplateHandler(BaseHandler):
    portal_types = ('Template')
    ident = 'template'
    folderish = False

    def export2(self, obj):
        ''' especific Template fields'''
        try:
            self.write_binary(obj.getTemplate_body())
        except:
            self.write_binary(obj.getRawTemplate_body())        

registerHandler(TemplateHandler)

class ImpressoHandler(BaseHandler):
    portal_types = ('Impresso')
    ident = 'impresso'
    folderish = True

    def export2(self, obj):
        ''' especific Impresso fields'''
        self.write('date ', obj.getDate())
        doctor = obj.getDoctor()
        self.write('doctor ', doctor.getId())
        self.write('dateOfVisit ', obj.getDateOfVisit())
        self.write('medicalNote ', obj.getMedicalNote())
        self.write('document_type ', obj.getDocument_type())
        try:
            self.write_binary(obj.getGdocument_body())
        except:
            self.write_binary(obj.getRawGdocument_body())     

registerHandler(ImpressoHandler)


class GenericDocumentHandler(BaseHandler):
    portal_types = ('GenericDocument')
    ident = 'genericdocument'
    folderish = True

    def export2(self, obj):
        ''' especific GenericDocument fields'''
        self.write('date ', obj.getDate())
        doctor = obj.getDoctor()
        self.write('doctor ', doctor.getId())
        self.write('dateOfVisit ', obj.getDateOfVisit())
        self.write('medicalNote ', obj.getMedicalNote())
        self.write('document_type ', obj.getDocument_type())
        try:
            self.write_binary(obj.getGdocument_body())
        except:
            self.write_binary(obj.getRawGdocument_body())        

registerHandler(GenericDocumentHandler)

class ImageHandler(BaseHandler):
    portal_types = ('Image', 'ATImage','Photo')
    ident = 'image'

    def export2(self, obj):
        self.write_binary(str(obj.data))

registerHandler(ImageHandler)

class FileHandler(ImageHandler):
    portal_types = ('File', 'ATFile')
    ident = 'files'

registerHandler(FileHandler)

def main(self, version='0_0_0'):
    ''' function called by Zope '''

    from optparse import OptionParser
    from AccessControl.SecurityManagement import newSecurityManager

    username = 'admin' # must be an user with admin priviligies in Zope.
    verbose = True

    app = self.getParentNode()

    plone = self
    plone_id = plone.getId() 

    # verify if a instance in the same version already exist.
    for obj in app.values():
        if obj.getId() == plone_id + '__' + version.replace('.', '_'):
            raise Exception('A %s instance in the version %s already exist!' % (plone_id, version))

    export_dir = 'export-%s' % plone.getId()
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir, ignore_errors=True)
    os.makedirs(export_dir)

    validation = Validation(export_dir) # validation object, store validation data.

    print '-'*80    
    print 'Exporting Plone site: %s' % plone_id
    print 'Export directory:  %s' % os.path.abspath(export_dir)
    print '-'*80    

    # get the admin user and defines a new security manager
    uf = app.acl_users
    user = uf.getUser(username)
    if user is None:
        raise ValueError('Unknown user: %s' % username)
    newSecurityManager(None, user.__of__(uf))

    export_members(plone, export_dir, verbose)

    # call exporters for each handler previusly registered.
    for portal_type in handlers:
        handler = handlers[portal_type]
        exporter = handler(plone, validation, export_dir, True)
        exporter.export(portal_type)

    validation.write()

    return export_dir

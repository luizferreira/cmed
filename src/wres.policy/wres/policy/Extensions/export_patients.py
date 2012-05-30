# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
import codecs

import os
import shutil
import tempfile

handlers = dict()  # portal_type -> handler

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

    print 'Exporting Members'
    fp = file(os.path.join(export_dir, 'members.ini'), 'w')

    acl_users = plone.acl_users
    pm = plone.portal_membership

    try:
        # Plone 2.5
        passwords = plone.acl_users.source_users._user_passwords
    except:
        # Plone 2.1
        passwords = None

    for username in acl_users.getUserNames():

        # if not username in members.objectIds():
        #     continue

        if verbose:
            print '-> %s' % username
        user = acl_users.getUserById(username)
        member = pm.getMemberById(username)
        if member is None:
            continue
        print >>fp, '[member-%s]' % username
        print >>fp, 'username = %s' % username
        if passwords:
            print >>fp, 'password = %s' % passwords.get(username)
        else:
            try:
                print >>fp, 'password = %s' % user.__
            except AttributeError:
                print >>fp, 'password = %s' % 'n/a'

        print >>fp, 'fullname = %s' % member.getProperty('fullname')
        print >>fp, 'email = %s' % member.getProperty('email')
        print >>fp, 'related_object = %s' % member.getProperty('related_object')
        print >>fp
    fp.close()

class BaseHandler(object):

    portal_types = ()
    ident = None
    initialized = False

    def __init__(self, plone, export_dir='exports', verbose=False):
        self.plone = plone
        self.portal_id = plone.getId()
        self.portal_path = plone.absolute_url(1)
        self.export_dir = export_dir
        self.verbose = verbose
        fname = os.path.join(export_dir, self.ident + '.ini')
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

    def write_common(self, obj, folder_path):

        def fix_oneline(s):
            s = s.replace('\r\n', ' ')
            s = s.replace('\n', ' ')
            return s

        from Products.CMFCore.WorkflowCore import WorkflowException

        wf_tool = obj.portal_workflow
        try:
            review_state = wf_tool.getInfoFor(obj, 'review_state')
        except WorkflowException:

            review_state = ''

        description = obj.Description()

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

        # raw data
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
#            print >>self.fp, 'raw_%s = %s' % (field.getName(), value)

    def write_leadout(self):
        print >>self.fp

    def write_binary(self, data, suffix='', key='filename'):
            dirpath = os.path.join(self.export_dir, self.ident)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            tempf = tempfile.mktemp(dir=dirpath) + suffix
            open(tempf, 'wb').write(str(data))
            self.write(key, os.path.abspath(tempf))


    def write(self, key, value):
        print >>self.fp, '%s = %s' % (key, value)

    def export(self, portal_type):

        print 'Exporting %s' % portal_type

        for obj, obj_path, folder_path in self._get_objects(portal_type):
            if self.verbose:
                print '-> %s' % obj_path

            if getattr(self, 'folderish', False):
                self.write_common(obj, '/'.join(folder_path.split('/')[:-1]))
            else:
                self.write_common(obj, folder_path)
            if hasattr(self, 'export2'):
                self.export2(obj)
            self.write_leadout()

class PatientHandler(BaseHandler):
    portal_types = ('Patient')
    ident = 'patient'
    folderish = True

    def export2(self, obj):
        ''' especific Doctor fields'''
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
            self.write('doctor ', doctor.UID())
        else:
            self.write('doctor ', '')
        self.write('socialSecurity ', obj.getSocialSecurity())
        self.write('identidade ', obj.getIdentidade())
        self.write('orgaoEmissor ', obj.getOrgaoEmissor())
        self.write('zipcode ', obj.getZipcode())
        self.write('pis_pasep ', obj.getPis_pasep())
        self.write('CTPS ', obj.getCTPS())
        self.write('tituloEleitor ', obj.getTituloEleitor())
        insurance = obj.getInsurance()
        if insurance is not None:
            self.write('insurance ', insurance.UID())
        else:
            self.write('insurance ', '')        
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
        # self.write('photo ', obj.getPhoto())
        self.write('employerName ', obj.getEmployerName())
        self.write('industry ', obj.getIndustry())
        self.write('occupationTitle ', obj.getOccupationTitle())
        self.write('status ', obj.getStatus())
        self.write('workPhone ', obj.getWorkPhone())
        self.write('extension ', obj.getExtension())
        self.write('fax ', obj.getFax())
        self.write('retirementdate ', obj.getRetirementdate())
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

class ImpressoHandler(BaseHandler):
    portal_types = ('Impresso')
    ident = 'impresso'
    folderish = True

    def export2(self, obj):
        ''' especific Impresso fields'''
        self.write('date ', obj.getDate())
        doctor = obj.getDoctor()
        self.write('doctor ', doctor.UID())
        self.write('dateOfVisit ', obj.getDateOfVisit())
        self.write('medicalNote ', obj.getMedicalNote())
        self.write('document_type ', obj.getDocument_type())
        try:
            self.write_binary(obj.getGdocument_body(), key='gdocument_body')
        except:
            self.write_binary(obj.getRawGdocument_body(), key='gdocument_body')        

registerHandler(ImpressoHandler)

class GenericDocumentHandler(BaseHandler):
    portal_types = ('GenericDocument')
    ident = 'genericdocument'
    folderish = True

    def export2(self, obj):
        ''' especific GenericDocument fields'''
        self.write('date ', obj.getDate())
        doctor = obj.getDoctor()
        self.write('doctor ', doctor.UID())
        self.write('dateOfVisit ', obj.getDateOfVisit())
        self.write('medicalNote ', obj.getMedicalNote())
        self.write('document_type ', obj.getDocument_type())
        try:
            self.write_binary(obj.getGdocument_body(), key='gdocument_body')
        except:
            self.write_binary(obj.getRawGdocument_body(), key='gdocument_body')        

registerHandler(GenericDocumentHandler)

class ImageHandler(BaseHandler):
    portal_types = ('Image', 'ATImage','Photo')
    ident = 'image'

    def export2(self, obj):
        self.write_binary(str(obj.data))

class FileHandler(ImageHandler):
    portal_types = ('File', 'ATFile')
    ident = 'files'

registerHandler(FileHandler)

registerHandler(ImageHandler)

def main(self):
    from optparse import OptionParser
    from AccessControl.SecurityManagement import newSecurityManager
    # import Zope

    parser = OptionParser()
    parser.add_option('-u', '--user', dest='username', default='admin')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      default=False)
    
#    import pdb; pdb.set_trace()

#    options, args = parser.parse_args()

    username = 'admin'

    # app = Zope.app()
    app = self.getParentNode()


    # plone = app.restrictedTraverse(path)
    plone = self
    path = plone.getId() 
    group = ''           
    export_dir = 'export-%s' % plone.getId()
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir, ignore_errors=True)
    os.makedirs(export_dir)

    print '-'*80    
    print 'Exporting Plone site: %s' % path
    print 'Export directory:  %s' % os.path.abspath(export_dir)
    print '-'*80    

    # app = Zope.app()

    uf = app.acl_users
#        user = uf.getUser(options.username)
    user = uf.getUser(username)
    if user is None:
#            raise ValueError('Unknown user: %s' % options.username)
        raise ValueError('Unknown user: %s' % username)
    newSecurityManager(None, user.__of__(uf))

#    export_members(plone, export_dir, options.verbose)
    export_members(plone, export_dir, True)

    for portal_type in handlers:
        handler = handlers[portal_type]
#            exporter = handler(plone, export_dir, options.verbose)
        exporter = handler(plone, export_dir, True)
        exporter.export(portal_type)

    print "\n****FIM****\n"
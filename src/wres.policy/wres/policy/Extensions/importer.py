# -*- coding: utf-8 -*-

import os
import transaction
from ConfigParser import ConfigParser, NoOptionError
from Products.CMFPlone.utils import _createObjectByType
from wres.archetypes.content.chartdata import ChartItemEventWrapper
from zope.app.component.hooks import getSite
from Testing.makerequest import makerequest
from zExceptions import BadRequest
from DateTime import DateTime


default_products = ['wres.policy']

extension_profiles = ('plonetheme.classic:default', 'plonetheme.sunburst:default')

handlers = []

relations2build = []

def registerHandler(handler):
    handlers.append(handler)


def setup_plone(app, import_dir, version, products, ext_profiles=()):
    '''
    create cmed instance
    '''

    app = makerequest(app)

    # derivate the instance id
    instance_name = import_dir[import_dir.rfind('/export-')+8:]
    instance_name = instance_name.split('__')[0] # exclude version from instance_name, if exist
    version = str(version).replace('.', '_')
    plone_id = instance_name + '__' + version

    # add plone site
    from Products.CMFPlone.factory import addPloneSite
    try:
        plone = addPloneSite(app, plone_id, extension_ids=ext_profiles)
    except BadRequest:
        # increment sub_version (plone site id) and then create plone site.
        instance_list = []
        for obj in app.values():
            if instance_name in obj.getId():
                instance_list.append(obj.getId())
        instance_list.sort()
        last = instance_list[-1]
        if last.count('_') == 3: # second migration in some version (eg unica__0_8)
            new_site_id =  last + '_1'
        else: # and so on (eg unica__0_8_2)
            to_increment = int(last[-1]) + 1
            new_site_id = last[:-1] + str(to_increment)
        plone = addPloneSite(app, new_site_id, extension_ids=ext_profiles)


    qit = plone.portal_quickinstaller

    # installs wres.policy
    ids = [ x['id'] for x in qit.listInstallableProducts(skipInstalled=1) ]
    for product in products:
        if product in ids:
            qit.installProduct(product)

    return plone


def import_members(plone, import_dir, verbose):

    print 'Importing members'

    pr = plone.portal_registration
    pm = plone.portal_membership


    members_ini = os.path.join(import_dir, 'members.ini')

    CP = ConfigParser()
    CP.read([members_ini])
    get = CP.get

    for section in CP.sections():
        username = get(section, 'username')
        if verbose:
            print '-> %s' % username

        try:
            pr.addMember(username, get(section, 'password'))
        except:
            print '-> ERROR: omitting %s' % username
            continue
        member = pm.getMemberById(username)
        pm.createMemberArea(username)
        member.setMemberProperties(dict(email=get(section, 'email'),
                                        fullname=get(section, 'fullname'),
                                  ))

def import_vocabulary(plone, import_dir):

    print 'Importing vocabularies'

    vt = plone.vocabulary_tool

    vocab_ini = os.path.join(import_dir, 'vocabulary.ini')

    CP = ConfigParser()
    CP.read([vocab_ini])
    get = CP.get
    for section in CP.sections():
        name = get(section, 'name')
        words = eval(get(section, 'words'))
        vt._persist_vocabulary_manager('vocab_'+name, words)

def search_catalog_by_id(id):
    portal = getSite()
    catalog = portal.portal_catalog
    brains = catalog.search({'id': id})
    try:
        return brains[0].getObject()
    except:
        print 'Object not in catalog.'


class Relation:
    def __init__(self, obj, set_method_str, referenced_obj_type, referenced_obj_id):
        self.obj = obj
        self.str_method = set_method_str
        self.type_name = referenced_obj_type
        self.referenced_obj_id = referenced_obj_id

    def build_relation(self, portal):
        '''
        build the relations between objects. The relations is in the list relations2build following
        the schema (obj, set_method_str_name, type_of_referenced_obj, referenced_obj_id)
        '''
        print 'Building relation: %s -> %s (method: %s)' % (self.obj.getId(), self.referenced_obj_id, self.str_method)
        catalog = portal.portal_catalog
        obj = self.obj
        brains = catalog.search({'portal_type': self.type_name, 'id':self.referenced_obj_id})
        if len(brains) > 1:
            raise Exception('The search returned more than one object, this is wrong bro!')
        ref_obj = brains[0].getObject()
        set_method = getattr(obj, self.str_method)
        set_method(ref_obj)
        obj.reindexObject()

class Validation(object):
    '''
    handle the validation of data imported.
    '''

    def __init__(self, plone, import_dir):
        self.verrors = []
        self.plone = plone
        fname = import_dir + '/validation.ini'
        self.cfg = ConfigParser()
        self.cfg.read(fname)

        print '\n' + '-'*80
        print ' '*30 + 'VALIDATING DATA'

        # call validation functions
        for section in self.cfg.sections():
            func = getattr(self, section)
            func(section)
        print '-'*80 + '\n'

    def counters_validator(self, section):
        '''
        validate the number of objects of each content type.
        '''
        clinic_counter = self.cfg.get(section, 'clinic_counter')
        doctor_counter = self.cfg.get(section, 'doctor_counter')
        files_counter = self.cfg.get(section, 'files_counter')
        genericdocument_counter = self.cfg.get(section, 'genericdocument_counter')
        image_counter = self.cfg.get(section, 'image_counter')
        impresso_counter = self.cfg.get(section, 'impresso_counter')
        patient_counter = self.cfg.get(section, 'patient_counter')
        secretary_counter = self.cfg.get(section, 'secretary_counter')
        template_counter = self.cfg.get(section, 'template_counter')
        visit_counter = self.cfg.get(section, 'visit_counter')

        tuples = [
        ('Clinic', clinic_counter),
        ('Doctor', doctor_counter),
        ('File', files_counter),
        ('GenericDocument', genericdocument_counter),
        ('Image', image_counter),
        ('Impresso', impresso_counter),
        ('Patient', patient_counter),
        ('Secretary', secretary_counter),
        ('Template', template_counter),
        ('Visit', visit_counter),
        ]

        for t in tuples:
            portal_type, counter = t
            brains = self.plone.portal_catalog(portal_type=portal_type, show_all=1, show_inactive=1)
            str_exp = '%d == %s' % (len(brains), counter)
            self.vprint('number of %s' % portal_type, str_exp)

    def vprint(self, validator_string, str_exp, verror='Erro'):
        '''
        wrapper to the print function
        '''
        print 'Validating ' + validator_string + '...',
        if eval(str_exp):
            print ' ok (%s)' % str_exp
        else:
            print ' VALIDATION ERROR*** (%s)' % str_exp
            self.verrors.append(verror)

class BaseHandler(object):

    portal_types = ()
    ident = None
    initialized = False

    def __init__(self, plone, import_dir, cfgfile, verbose=False):
        self.plone = plone
        self.portal_id = plone.getId()
        self.portal_path = plone.absolute_url(1)
        self.import_dir = import_dir
        self.verbose = verbose
        self.cfg = ConfigParser()
        self.cfg.read(cfgfile)

    def changeOwner(self, context, owner):
        try:
            context.plone_utils.changeOwnershipOf(context, owner)
        except:
            try:
                context.plone_utils.changeOwnershipOf(context, 'raetsch')
            except:
                if not 'admin' in context.portal_membership.listMemberIds():
                    context.portal_registration.addMember('admin', '"&§%/!')
                context.plone_utils.changeOwnershipOf(context, 'admin')

    def folder_create(self, root, dirname):
        '''
        create 'Folders' to fetch the object being imported
        '''
        current = root
        for c in dirname.split('/'):
            if not c: continue
            if not c in current.objectIds():
                _createObjectByType('Folder', current, id=c)
            current = getattr(current, c)

        return current

    def set_data(self, obj, section):
        '''
        import common fields like title, id, path, etc.
        '''

        CP = self.cfg

        if CP.has_option(section, 'description'):
            obj.setDescription(CP.get(section, 'description'))

        if CP.has_option(section, 'title'):
            obj.setTitle(CP.get(section, 'title'))

        if CP.has_option(section, 'expires'):
            obj.setExpirationDate(CP.getfloat(section, 'expires'))

        if CP.has_option(section, 'effective'):
            obj.setEffectiveDate(CP.getfloat(section, 'effective'))

        if CP.has_option(section, 'created'):
            obj.setCreationDate(CP.getfloat(section, 'created'))

        if CP.has_option(section, 'content-type'):
            obj.setContentType(CP.get(section, 'content-type'))

        if CP.has_option(section, 'text-format'):
            format = CP.get(section, 'text-format')
            if format == 'structured-text':
                format = 'text/structured'
            elif format == 'html':
                format = 'text/html'
            obj.format = format
            obj.setFormat(format)
            obj.__format = format

        if CP.has_option(section, 'subjects'):
            subjects = [s.strip() for s in CP.get(section, 'subjects').split(',')]
            obj.setSubject(subjects)

        if CP.has_option(section, 'owner'):
            owner = CP.get(section, 'owner')
            self.changeOwner(obj, owner)
            obj.setCreators([owner])

        if CP.has_option(section, 'review-state'):
            state = CP.get(section, 'review-state')
            if state == 'published':
                wf_tool = obj.portal_workflow
                try:
                    wf_tool.doActionFor(obj, 'publish')
                except:
                    pass

    def get_binary(self, section, key='filename'):
        '''
        used to import raw things, like images, files, body text, etc.
        '''
        return file(self.cfg.get(section, key)).read()

    def __call__(self, *args, **kw):
        '''
        function called right after the initialization to perform
        the importation de facto.
        '''
        portal_type = getattr(self, 'portal_type', None)
        if portal_type is None:
            print 'Omitting %s' % self.__class__.__name__
            return

        print 'Importing %s' % portal_type

        get = self.cfg.get

        for section in self.cfg.sections():
            path = get(section, 'path')
            id = get(section, 'id')

            # dirname == path if object is folderish.
            if getattr(self, 'folderish', False):
                dirname = path
            else:
                dirname = '/'.join(path.split('/')[:-1])

            folder = self.folder_create(self.plone, dirname) # create 'Folders' to fetch the object path.

            if self.verbose:
                print 'Creating %s: %s' % (portal_type, path+'/'+id)

            if id in folder.objectIds():
                obj = folder
            else:
                _createObjectByType(portal_type, folder, id)
            obj = getattr(folder, id)
            self.set_data(obj, section)

            # calls the type especific import step.
            if hasattr(self, 'import2'):
                self.import2(obj, section)

class ClinicHandler(BaseHandler):
    ident = 'clinic'
    folderish = False
    portal_type = 'Clinic'

    def import2(self, obj, section):
        ''' especific Clinic fields'''
        obj.setName(self.cfg.get(section, 'name'))
        obj.setStreet(self.cfg.get(section, 'street'))
        obj.setComplemento(self.cfg.get(section, 'complemento'))
        obj.setBairro(self.cfg.get(section, 'bairro'))
        obj.setCity(self.cfg.get(section, 'city'))
        obj.setState(self.cfg.get(section, 'state'))
        obj.setPhone(self.cfg.get(section, 'phone'))
        obj.setFax(self.cfg.get(section, 'fax'))
        obj.setEmail(self.cfg.get(section, 'email'))
        obj.reindexObject()

registerHandler(ClinicHandler)

class DoctorHandler(BaseHandler):
    ident = 'doctor'
    folderish = True
    portal_type = 'Doctor'

    def import2(self, obj, section):
        ''' especific Doctor fields'''
        obj.setProfessional(self.cfg.get(section, 'professional'))
        obj.setSsn(self.cfg.get(section, 'ssn'))
        obj.setFirstName(self.cfg.get(section, 'firstName'))
        obj.setLastName(self.cfg.get(section, 'lastName'))
        obj.setStreet1(self.cfg.get(section, 'street1'))
        obj.setStreet2(self.cfg.get(section, 'street2'))
        obj.setCity(self.cfg.get(section, 'city'))
        obj.setState(self.cfg.get(section, 'state'))
        obj.setZipcode(self.cfg.get(section, 'zipcode'))
        obj.setWebsite(self.cfg.get(section, 'website'))
        obj.setPhone(self.cfg.get(section, 'phone'))
        obj.setCel(self.cfg.get(section, 'cel'))
        obj.setFax(self.cfg.get(section, 'fax'))
        obj.setEmail(self.cfg.get(section, 'email'))
        obj.setInitial(self.cfg.get(section, 'initial'))
        obj.setSignature(self.cfg.get(section, 'signature'))
        obj.setCredentials(self.cfg.get(section, 'credentials'))
        obj.setSpecialty1(self.cfg.get(section, 'specialty1'))
        obj.setSpecialty2(self.cfg.get(section, 'specialty2'))
        obj.setSignPassword(self.cfg.get(section, 'signPassword'))
        obj.add_visits_folder()
        obj.at_post_create_script(migration=True)
        obj.reindexObject()

registerHandler(DoctorHandler)

class SecretaryHandler(BaseHandler):
    ident = 'secretary'
    folderish = True
    portal_type = 'Secretary'

    def import2(self, obj, section):
        ''' especific Secretary fields'''
        obj.setIsTranscriptionist(self.cfg.get(section, 'isTranscriptionist'))
        obj.setFirstName(self.cfg.get(section, 'firstName'))
        obj.setLastName(self.cfg.get(section, 'lastName'))
        obj.setSsn(self.cfg.get(section, 'ssn'))
        obj.setEmail(self.cfg.get(section, 'email'))
        obj.setAddress1(self.cfg.get(section, 'address1'))
        obj.setCity(self.cfg.get(section, 'city'))
        obj.setState(self.cfg.get(section, 'state'))
        obj.setPhone(self.cfg.get(section, 'phone'))
        obj.setCel(self.cfg.get(section, 'cel'))
        obj.reindexObject()
        obj.at_post_create_script()

registerHandler(SecretaryHandler)

class PatientHandler(BaseHandler):
    ident = 'patient'
    folderish = True
    portal_type = 'Patient'

    def import2(self, obj, section):
        ''' especific Patient fields'''
        obj.chartFolder # create chart
        obj.setFirstName(self.cfg.get(section, 'firstName'))
        obj.setLastName(self.cfg.get(section, 'lastName'))
        obj.setBirthDate(self.cfg.get(section, 'birthDate'))
        obj.setEmail(self.cfg.get(section, 'email'))
        obj.setHomePhone(self.cfg.get(section, 'homePhone'))
        obj.setMobile(self.cfg.get(section, 'mobile'))
        obj.setContactPhone(self.cfg.get(section, 'contactPhone'))
        obj.setSex(self.cfg.get(section, 'sex'))
        obj.setAddress1(self.cfg.get(section, 'address1'))
        obj.setAddress2(self.cfg.get(section, 'address2'))
        obj.setCity(self.cfg.get(section, 'city'))
        obj.setState(self.cfg.get(section, 'state'))
        obj.setChart(self.cfg.get(section, 'chart'))
        doctor_id = self.cfg.get(section, 'doctor')
        if doctor_id:
            relations2build.append((Relation(obj, 'setDoctor', 'Doctor', doctor_id)))
        else:
            obj.setDoctor(None)
        obj.setSocialSecurity(self.cfg.get(section, 'socialSecurity'))
        obj.setIdentidade(self.cfg.get(section, 'identidade'))
        obj.setOrgaoEmissor(self.cfg.get(section, 'orgaoEmissor'))
        obj.setZipcode(self.cfg.get(section, 'zipcode'))
        obj.setPis_pasep(self.cfg.get(section, 'pis_pasep'))
        obj.setCTPS(self.cfg.get(section, 'CTPS'))
        obj.setTituloEleitor(self.cfg.get(section, 'tituloEleitor'))
        obj.setNomeDoPai(self.cfg.get(section, 'nomeDoPai'))
        obj.setNomeDaMae(self.cfg.get(section, 'nomeDaMae'))
        obj.setNacionalidade(self.cfg.get(section, 'nacionalidade'))
        obj.setRace(self.cfg.get(section, 'race'))
        obj.setMaritalStatus(self.cfg.get(section, 'maritalStatus'))
        obj.setEducationCompleted(self.cfg.get(section, 'educationCompleted'))
        obj.setEmployerName(self.cfg.get(section, 'employerName'))
        obj.setIndustry(self.cfg.get(section, 'industry'))
        obj.setOccupationTitle(self.cfg.get(section, 'occupationTitle'))
        obj.setStatus(self.cfg.get(section, 'status'))
        obj.setWorkPhone(self.cfg.get(section, 'workPhone'))
        obj.setExtension(self.cfg.get(section, 'extension'))
        obj.setFax(self.cfg.get(section, 'fax'))
        obj.setRetirementdate(self.cfg.get(section, 'retirementdate'))
        try:
            obj.setPhoto(self.get_binary(section))
        except NoOptionError:
            pass # patient photo is the default photo.
        chart_dic = eval( self.cfg.get(section, 'chartdata') )
        obj.import_chartdata(chart_dic) # there is a method in Patient to handle the chartdata import
        obj.at_post_create_script()
        obj.reindexObject()

registerHandler(PatientHandler)

class VisitHandler(BaseHandler):
    ident = 'visit'
    folderish = False
    portal_type = 'Visit'

    def import2(self, obj, section):
        ''' especific Visit fields'''
        patient_id = self.cfg.get(section, 'patient')
        if patient_id:
            relations2build.append((Relation(obj, 'setPatient', 'Patient', patient_id)))
        else:
            obj.setPatient(None)
        obj.setStartDate(DateTime(float(self.cfg.get(section, 'start-date'))))
        obj.setEndDate(DateTime(float(self.cfg.get(section, 'end-date'))))
        obj.setDuration(self.cfg.get(section, 'duration'))
        obj.setContactPhone(self.cfg.get(section, 'contactPhone'))
        obj.setVisit_type(self.cfg.get(section, 'visit_type'))
        obj.setVisit_reason(self.cfg.get(section, 'visit_reason'))
        obj.setSubject(obj.getVisit_type())
        obj.reindexObject()

registerHandler(VisitHandler)


class ImpressoHandler(BaseHandler):
    ident = 'impresso'
    folderish = True
    portal_type = 'Impresso'

    def import2(self, obj, section):
        ''' especific Impresso fields'''
        obj.setDate(self.cfg.get(section, 'date'))
        doctor_id = self.cfg.get(section, 'doctor')
        if doctor_id:
            relations2build.append((Relation(obj, 'setDoctor', 'Doctor', doctor_id)))
        else:
            obj.setDoctor(None)
        obj.setDateOfVisit(self.cfg.get(section, 'dateOfVisit'))
        obj.setMedicalNote(self.cfg.get(section, 'medicalNote'))
        obj.setDocument_type(self.cfg.get(section, 'document_type'))
        obj.reindexObject()

registerHandler(ImpressoHandler)

class GenericDocumentHandler(BaseHandler):
    ident = 'genericdocument'
    folderish = True
    portal_type = 'GenericDocument'

    def import2(self, obj, section):
        ''' especific Impresso fields'''
        obj.setDate(self.cfg.get(section, 'date'))
        doctor_id = self.cfg.get(section, 'doctor')
        if doctor_id:
            relations2build.append((Relation(obj, 'setDoctor', 'Doctor', doctor_id)))
        else:
            obj.setDoctor(None)
        obj.setDateOfVisit(self.cfg.get(section, 'dateOfVisit'))
        obj.setMedicalNote(self.cfg.get(section, 'medicalNote'))
        obj.setDocument_type(self.cfg.get(section, 'document_type'))
        obj.reindexObject()

registerHandler(GenericDocumentHandler)

class TemplateHandler(BaseHandler):
    ident = 'template'
    folderish = False
    portal_type = 'Template'

    def import2(self, obj, section):
        ''' especific Template fields'''
        obj.setTemplate_body(self.get_binary(section))
        obj.reindexObject()

registerHandler(TemplateHandler)

class ImageHandler(BaseHandler):
    ident = 'image'
    portal_type = 'Image'

    def import2(self, obj, section):
        obj.setImage(self.get_binary(section))

registerHandler(ImageHandler)

class FileHandler(BaseHandler):
    ident = 'files'
    portal_type = 'File'

    def import2(self, obj, section):
        obj.setFile(self.get_binary(section))

registerHandler(FileHandler)

def import_events(import_dir):

    print 'Importing events'

    events_file = os.path.join(import_dir, 'patients.ini')

    CP = ConfigParser()
    CP.read([events_file])
    get = CP.get
    for section in CP.sections():
        ev_list = eval(get(section, 'events'))
        for event in ev_list:
            if event['related_obj'] is 'ChartItemEventWrapper':
                dummy = {}
                dummy['medication'] = dummy['problem'] = dummy['allergy'] = dummy['exam'] = event['title']
                wrapper = ChartItemEventWrapper(event['mapping_name'], patient, **dummy)
                patient.create_event(event['type'], DateTime(event['date']), wrapper)
            else:
                patient.create_event(event['type'], DateTime(event['date']), search_catalog_by_id(event['related_obj']))

def import_plone(self, import_dir, version, verbose=False):
    '''
    makes the importation de factory
    '''

    print '-'*80
    print 'Importing Plone site from %s ' % import_dir
    print '-'*80

    products = default_products
    profiles = []

    # create a cmed instance.
    plone = setup_plone(self, import_dir, version, products, extension_profiles)
    transaction.commit()
    print '\nSite created: %s' % plone.getId()
    print 'Products: %s' % ','.join(products)
    print 'Profiles: %s' % profiles

    import_vocabulary(plone, import_dir)
    import_members(plone, import_dir, verbose)
    transaction.commit()

    # run each importer handler.
    for handler in handlers:
        ident = handler.ident
        fname = import_dir + '/' + ident + '.ini'
        if fname.endswith('members.ini'): continue # jump members.
        handler = handler(plone, import_dir, fname, verbose) # init handler
        handler() # run it
        transaction.commit()

    import_events(import_dir)

    # fixup(plone)
    print 'Building relations'
    for relation in relations2build:
        relation.build_relation(plone)
    transaction.commit()

    return plone

def main(self, import_dir=None, version=None):
    from AccessControl.SecurityManagement import newSecurityManager

    if import_dir == None or version == None:
        raise Exception("The import step must be called inside 'upgrade'.")

    username = 'admin'
    verbose = True

    # get the admin user and defines a new security manager
    app = self.getParentNode()
    uf = app.acl_users
    user = uf.getUser(username)
    if user is None:
        raise ValueError('Unknown user: %s' % username)
    newSecurityManager(None, user.__of__(uf))

    plone = import_plone(app, import_dir, version, verbose)
    print 'Committing...'
    transaction.commit()
    print 'Upgrade done'

    Validation(plone, import_dir)

    print plone.absolute_url()

    return 'Importing Complete'

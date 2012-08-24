# coding=utf-8

import os

from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.CatalogTool import CatalogTool
from wres.policy.utils.setup_utils import add_types_to_portal_factory,\
     install_dependencies, create_metadatas, add_index, add_layer
from AccessControl import Unauthorized


from AccessControl.Permissions import *
from Products.Sessions.SessionPermissions import *
from Products.CMFCore.permissions import *

# WRES imports
from wres.policy.utils.roles import *
from wres.policy.utils.permissions import *
from wres.policy.utils.config import *

def getInstancePath():
    home = os.environ['INSTANCE_HOME']
    home = home.split('parts')
    home = home[0]
    return home

def getOrCreateType(portal, atobj, newid, newtypeid):
    """
    Gets the object specified by newid if it already exists under
    atobj or creates it there with the id given in newtypeid
    """
    try:
        newobj = getattr(atobj,newid) #get it if it already exists
    except AttributeError:  #newobj doesn't already exist
        try:            
            _ = atobj.invokeFactory(id=newid,type_name=newtypeid)            
        except ValueError:
            _createObjectByType(newtypeid, atobj, newid)
        except Unauthorized:
            _createObjectByType(newtypeid, atobj, newid)
        newobj = getattr(atobj,newid)
    return newobj

def createClinic(portal):
    """ Cria o objeto clinica """
    print '*** Criando objeto clinica...'
    clinic = getOrCreateType(portal, portal, 'Clinic', 'Clinic')
    # Anonymous need the permission view, so he can view that information in "Contato"
    clinic.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE, ANONYMOUS_ROLE], acquire = False)
    clinic.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE], acquire = False)
    clinic.setTitle('Clínica')
    clinic.setExcludeFromNav(True)
    clinic.reindexObject()
    """ Cria objetos dentro de clinica """
    #TODO: Atualmente os relatorios sao um template acessado de dentro do obj clinica (18/06/2012). Discutir a necessidade deste ReportsFolder.
    #createReportsFolder(portal, clinic) 
    print '*** Criando objeto clinica...... OK'

def createAdminFolder(portal):
    """ Cria a pasta de admins """
    print '*** Criando pasta de admins...'
    admin_folder = getOrCreateType(portal, portal, 'Admins', 'AdminFolder')
    admin_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE], acquire = False)
    admin_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE], acquire = False)
    admin_folder.setTitle('Administradores')
    admin_folder.reindexObject()
    print '*** Criando pasta de admins...... OK'

def createTemplateFolder(portal):
    """ Cria a pasta de templates """
    print '*** Criando pasta de templates...'
    template_folder = getOrCreateType(portal, portal, 'Templates', 'Folder')
    consultas_folder = getOrCreateType(portal, template_folder, 'Consultas', 'TemplateFolder')
    impressos_folder = getOrCreateType(portal, template_folder, 'Impressos', 'TemplateFolder')

    # a permissao Modify portal content eh necessaria pra se poder adicionar objetos dentro da pasta.
    consultas_folder.manage_permission('Modify portal content', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE], acquire = False)
    impressos_folder.manage_permission('Modify portal content', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE], acquire = False)
    template_folder.manage_permission('Modify portal content', [MANAGER_ROLE], acquire = False)
    template_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE], acquire = False)
    template_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE], acquire = False)
    # adds
    template_folder.manage_permission('ATContentTypes: Add File', [], acquire = False)
    template_folder.manage_permission('Add portal topics', [], acquire = False)
    template_folder.manage_permission('ATContentTypes: Add Event', [], acquire = False)
    template_folder.manage_permission('ATContentTypes: Add Image', [], acquire = False)
    template_folder.manage_permission('ATContentTypes: Add Link', [], acquire = False)
    template_folder.manage_permission('ATContentTypes: Add News Item', [], acquire = False)
    template_folder.manage_permission('ATContentTypes: Add Folder', [], acquire = False)
    template_folder.manage_permission('ATContentTypes: Add Document', [], acquire = False)
    template_folder.manage_permission('ATContentTypes: Add File', [], acquire = False)
    template_folder.setTitle('Modelos')
    template_folder.reindexObject()
    print '*** Criando pasta de templates...... OK'    

def createDoctorFolder(portal):
    """ Cria a pasta de medicos """
    print '*** Criando pasta de medicos...'
    doctor_folder = getOrCreateType(portal, portal, 'Doctors', 'DoctorFolder')
    doctor_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE], acquire = False)
    # its important that Anonymous have 'Acess cont..' permission, so he can call the method list_doctors.
    doctor_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE, ANONYMOUS_ROLE], acquire = False)
    doctor_folder.setTitle('Médicos')
    doctor_folder.reindexObject()
    print '*** Criando pasta de medicos...... OK'

def createContactPage(portal):
    ''' Create contact page (visible just for anonymous) '''
    contact = getOrCreateType(portal, portal, 'Contato', 'Document')
    contact.setLayout('clinic_contact')
    contact.manage_permission('View', [MANAGER_ROLE, ANONYMOUS_ROLE], acquire=False)
    contact.manage_permission('Access contents information', [MANAGER_ROLE, ANONYMOUS_ROLE], acquire = False)
    contact.setExcludeFromNav(True)
    contact.reindexObject()

def createReferringProviderFolder(portal):
    """ Cria a pasta de medicos indicantes """
    print '*** Criando pasta de medicos indicantes...'
    refprovider_folder = getOrCreateType(portal, portal, 'Referring Providers', 'ReferringProviderFolder')
    refprovider_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    refprovider_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    refprovider_folder.setTitle('Médicos Indicantes')
    refprovider_folder.reindexObject()
    print '*** Criando pasta de medicos indicantes...... OK'
    
def createPatientFolder(portal):
    """ Cria a pasta de pacientes """
    print '*** Criando pasta de pacientes...'
    patient_folder = getOrCreateType(portal, portal, 'Patients', 'PatientFolder')
    patient_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    patient_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)        
    patient_folder.setTitle('Pacientes')
    patient_folder.reindexObject()
    print '*** Criando pasta de pacientes...... OK'
    
def createSecretaryFolder(portal):
    """ Cria a pasta de secretarias """
    print '*** Criando pasta de secretarias...'
    secretary_folder = getOrCreateType(portal, portal, 'Secretaries', 'SecretaryFolder')
    secretary_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE], acquire = False)
    secretary_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE], acquire = False)
    secretary_folder.setTitle('Secretárias')
    secretary_folder.reindexObject()
    print '*** Criando pasta de secretarias...... OK'    
    
def createTranscriptionistFolder(portal):
    """ Cria a pasta de transcritores """
    print '*** Criando pasta de transcritores...'
    transcriptionist_folder = getOrCreateType(portal, portal, 'Transcriptionists', 'TranscriptionistFolder')
    transcriptionist_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    transcriptionist_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    transcriptionist_folder.setTitle('Transcritores')
    transcriptionist_folder.reindexObject()
    print '*** Criando pasta de transcritores...... OK'
    
def createVisitFolder(portal):
    """ Cria a pasta de visitas """
    print '*** Criando pasta de visitas...'
    visit_folder = getOrCreateType(portal, portal, 'Appointments', 'VisitFolder')
    visit_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE], acquire = False)
    visit_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE], acquire = False)    
    visit_folder.setTitle('Agenda')
    visit_folder.setLayout('sec_desk')
    visit_folder.setExcludeFromNav(True)
    visit_folder.setLocallyAllowedTypes([])
    visit_folder.setImmediatelyAddableTypes([])
    visit_folder.setConstrainTypesMode(1)
    visit_folder.reindexObject() 
    print '*** Criando pasta de visitas...... OK'

#TODO: Remover comentarios referente ao insurance folder posteriormente
#def createInsuranceFolder(portal):
    #""" Cria a pasta de planos de saude """
    #print '*** Criando pasta de planos de saude...'
    #insurance_folder = getOrCreateType(portal, portal, 'Insurances', 'InsuranceFolder')
    #insurance_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    #insurance_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    #insurance_folder.setTitle('Planos de Saúde')
    #insurance_folder.reindexObject()
    #print '*** Criando pasta de planos de saude...... OK'                  
    
def createReportsFolder(portal, clinic):
    """ Cria a pasta de relatórios """
    print '*** Criando pasta de relatórios...'
    reports_folder = getOrCreateType(portal, clinic, 'Reports', 'Folder')
    reports_folder.manage_permission('Modify portal content', [MANAGER_ROLE], acquire = False)
    reports_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    reports_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    reports_folder.manage_addProperty('layout','reports_folder_view','string')
    reports_folder.setTitle('Relatórios')
    reports_folder.setExcludeFromNav(True)
    reports_folder.setLocallyAllowedTypes([])
    reports_folder.setImmediatelyAddableTypes([])
    reports_folder.setConstrainTypesMode(1)
    reports_folder.reindexObject()
    print '*** Criando pasta de relatórios...... OK'       

def deleteDefaultObjects(portal):
    """ Deleta objetos de um plone site out-of-the-box """
    try:
        portal.manage_delObjects('Members')
        print "Deleted %s folder" % 'members'
    except AttributeError:
        print "No %s folder detected. Hmm... strange. Continuing..." % 'members'
    
    try:
        portal.manage_delObjects('news')
        print "Deleted %s folder" % 'news'
    except AttributeError:
        print "No %s folder detected. Hmm... strange. Continuing..." % 'news'

    try:
        portal.manage_delObjects('events')
        print "Deleted Events folder"
    except AttributeError:
        print "No %s folder detected. Hmm... strange. Continuing..." % 'events'

    try:
        portal.manage_delObjects('front-page')
        print "Deleted Front page"
    except AttributeError:
        print "No %s detected. Hmm... strange. Continuing..." % 'page'        

def createGroups(portal):
    """ Funcao que cria os grupos e atribui papeis aos mesmos. As constantes aqui
    utilizadas estao definidas no arquivo wres.policy.utils.roles """
    
    print "Create Groups..."
    print "Creating Groups..."

    portal_groups = getToolByName(portal, 'portal_groups')
    acl_users = getToolByName(portal, 'acl_users')
     
    if not acl_users.searchGroups(id=DOCTOR_GROUP):    
        portal_groups.addGroup(DOCTOR_GROUP, roles = [DOCTOR_ROLE, MEMBER_ROLE, CONTRIBUTOR_ROLE, REVIEWER_ROLE])
    
    if not acl_users.searchGroups(id=SECRETARY_GROUP):        
        portal_groups.addGroup(SECRETARY_GROUP, roles = [SECRETARY_ROLE, MEMBER_ROLE, CONTRIBUTOR_ROLE])
        
    if not acl_users.searchGroups(id=PATIENT_GROUP):    
        portal_groups.addGroup(PATIENT_GROUP, roles = [PATIENT_ROLE, MEMBER_ROLE])
    
    if not acl_users.searchGroups(id=TRANSCRIPTIONIST_GROUP):
        portal_groups.addGroup(TRANSCRIPTIONIST_GROUP, roles = [TRANSCRIPTIONIST_ROLE, MEMBER_ROLE, CONTRIBUTOR_ROLE])
    
    if not acl_users.searchGroups(id=UEMRADMIN_GROUP):
        portal_groups.addGroup(UEMRADMIN_GROUP, roles = [UEMRADMIN_ROLE, MEMBER_ROLE, OWNER_ROLE, MANAGER_ROLE])

#TODO: Remover posteriormente estes comentarios        
#def createTop10DefaultInsurance(portal):
    ##-------Bradesco Saúde------------------------------------------
    #print '*** Criando Plano Bradesco...'
    #insurance = getOrCreateType(portal, portal.Insurances, 'Bradesco', 'Insurance')
    #insurance.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    #insurance.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    #insurance.setTitle('Bradesco Saúde')
    #insurance.setName('Bradesco Saúde')
    #insurance.setPhoneNumber('0800 701 2700')
    #insurance.setWebPage('http://www.bradescosaude.com.br')
    #insurance.reindexObject()
    #print '*** Criando objeto Plano Bradesco...... OK'
    
    ##-------Amil Assistencia ------------------------------------------
    #print '*** Criando Amil Assitência...'
    #insurance = getOrCreateType(portal, portal.Insurances, 'Amil', 'Insurance')
    #insurance.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    #insurance.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    #insurance.setTitle('Amil Assitência')
    #insurance.setName('Amil Assitência')
    #insurance.setPhoneNumber('(31) 3316-1000')
    #insurance.setWebPage('http://www.amil.com.br/')
    #insurance.reindexObject()
    #print '*** Criando objeto Amil Assitência...... OK'
    
     ##-------Unimed BH------------------------------------------
    #print '*** Criando Unimed BH...'
    #insurance = getOrCreateType(portal, portal.Insurances, 'UnimedBH', 'Insurance')
    #insurance.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    #insurance.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    #insurance.setTitle('Unimed BH')
    #insurance.setName('Unimed BH')
    #insurance.setPhoneNumber('0800 30 30 03')
    #insurance.setWebPage('http://www.unimedbh.com.br/')
    #insurance.reindexObject()
    #print '*** Criando objeto Unimed BH...... OK'
    
     ##-------Intermédica------------------------------------------
    #print '*** Criando Intermédica...'
    #insurance = getOrCreateType(portal, portal.Insurances, 'Intermedica', 'Insurance')
    #insurance.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    #insurance.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    #insurance.setTitle('Intermédica')
    #insurance.setName('Intermédica')
    #insurance.setPhoneNumber('0800 770 084')
    #insurance.setWebPage('http://www.intermedica.com.br/')
    #insurance.reindexObject()
    #print '*** Criando objeto Intermédica...... OK'
    
     ##-------Medial------------------------------------------
    #print '*** Criando Medial...'
    #insurance = getOrCreateType(portal, portal.Insurances, 'Medial', 'Insurance')
    #insurance.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    #insurance.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    #insurance.setTitle('Medial')
    #insurance.setName('Medial')
    #insurance.setPhoneNumber('0800 724 1331')
    #insurance.setWebPage('http://www.medialsaude.com.br/')
    #insurance.reindexObject()
    #print '*** Criando objeto Medial...... OK'
    
    ##-------Sul América Saúde------------------------------------------
    #print '*** Criando Sul América Saúde...'
    #insurance = getOrCreateType(portal, portal.Insurances, 'Sulamerica', 'Insurance')
    #insurance.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    #insurance.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    #insurance.setTitle('Sul América Saúde')
    #insurance.setName('Sul América Saúde')
    #insurance.setPhoneNumber('0800 724 1331')
    #insurance.setWebPage('http://www.sulamericaweb.com.br/')
    #insurance.reindexObject()
    #print '*** Criando objeto Sul América Saúde...... OK'
    
    ##-------Golden Cross Saúde------------------------------------------
    #print '*** Criando Golden Cross...'
    #insurance = getOrCreateType(portal, portal.Insurances, 'Goldencross', 'Insurance')
    #insurance.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    #insurance.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    #insurance.setTitle('Golden Cross')
    #insurance.setName('Golden Cross')
    #insurance.setPhoneNumber('0800 728 2001')
    #insurance.setWebPage('http://www.goldencross.com.br/')
    #insurance.reindexObject()
    #print '*** Criando objeto Golden Cross...... OK'
   
   ##-------SóSaúde------------------------------------------
    #print '*** Criando SóSaúde...'
    #insurance = getOrCreateType(portal, portal.Insurances, 'Sosaude', 'Insurance')
    #insurance.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    #insurance.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    #insurance.setTitle('Só Saúde Assistência Medico Hospitalar')
    #insurance.setName('Só Saúde Assistência Medico Hospitalar')
    #insurance.setPhoneNumber('(31)3078-8000')
    #insurance.setWebPage('http://www.sosaude.com.br/')
    #insurance.reindexObject()
    #print '*** Criando objeto SóSaúde...... OK'
    
    ##-------Santa Casa Saúde------------------------------------------
    #print '*** Criando Santa Casa...'
    #insurance = getOrCreateType(portal, portal.Insurances, 'Santacasa', 'Insurance')
    #insurance.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)
    #insurance.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE], acquire = False)    
    #insurance.setTitle('Santa Casa Saúde')
    #insurance.setName('Santa Casa Saúde')
    #insurance.setPhoneNumber('(31)3271-1601')
    #insurance.setWebPage('http://www.santacasaplanos.com.br/')
    #insurance.reindexObject()
    #print '*** Criando objeto Santa Casa...... OK'
   
#===============================================================================
# Objeto Vazio        
#===============================================================================
class Empty: pass

#===============================================================================
# Adiciona Lexicos > Lexicon('Lexicon', '', HTMLWordSplitter(), CaseNormalizer(), StopWordRemover())  
# Peter  
#===============================================================================
def addLexicon(catalog, name, description, wordsplitter, case, stopwords):

    elem = []
    wordSplitter = Empty()
    wordSplitter.group = 'Word Splitter'
    wordSplitter.name = wordsplitter #'HTML aware splitter'

    caseNormalizer = Empty()
    caseNormalizer.group = 'Case Normalizer'
    caseNormalizer.name = case #'Case Normalizer'

    stopWords = Empty()
    stopWords.group = 'Stop Words'
    stopWords.name = stopwords #'Remove listed and single char words'

    elem.append(wordSplitter)
    elem.append(caseNormalizer)
    elem.append(stopWords)
    catalog.manage_addProduct['ZCTextIndex'].manage_addLexicon(name, description, elem)
    
#===============================================================================
# Cria o schedule_catalog
# Peter
#===============================================================================
def createScheduleCatalog(site):
    try:
        site.schedule_catalog
    except:
        site._setObject('schedule_catalog', CatalogTool())
        
    schedule_catalog = getToolByName(site, 'schedule_catalog')
    at = getToolByName(site, 'archetype_tool')
    at.setCatalogsByType(schedule_catalog.meta_type, ['portal_catalog', 'schedule_catalog'])
    at.setCatalogsByType('Visit', ['schedule_catalog'])
    
    #Adicionando Lexicos
    addLexicon(site.schedule_catalog, 'htmltext_lexicon', '', 'HTML aware splitter', 'Case Normalizer', 'Remove listed stop words only')
    addLexicon(site.schedule_catalog, 'plaintext_lexicon', '', 'Whitespace splitter', 'Case Normalizer', 'Remove listed stop words only')
    addLexicon(site.schedule_catalog, 'plone_lexicon', '', 'Whitespace splitter', 'Case Normalizer', 'Remove listed stop words only')
    
    #Declaracoes ZCTextIndex
    add_index(site, 'getParsedLastName', 'ZCTextIndex',
                catalog='schedule_catalog',
                extra={'lexicon_id': 'plone_lexicon',
                        'doc_attr': 'getParsedLastName',
                        'index_type': 'Okapi BM25 Rank',
                    }
                )
    add_index(site, 'Description', 'ZCTextIndex',
                catalog='schedule_catalog',
                extra={'lexicon_id': 'plaintext_lexicon',
                        'doc_attr': 'Description',
                        'index_type': 'Okapi BM25 Rank',
                    }
                )   
    add_index(site, 'SearchableText', 'ZCTextIndex',
                catalog='schedule_catalog',
                extra={'lexicon_id': 'htmltext_lexicon',
                        'doc_attr': 'SearchableText',
                        'index_type': 'Okapi BM25 Rank',
                    }
                )
    add_index(site, 'Title', 'ZCTextIndex', 
                catalog='schedule_catalog',
                extra={'lexicon_id': 'plaintext_lexicon',
                        'doc_attr': 'Title',
                        'index_type': 'Okapi BM25 Rank',
                    }
                )
    
    add_index(site, 'start', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'end', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'getLastName', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'getSocialSecurity', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'getChart', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'getProfessional', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'getProviderId', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'review_state', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'Type', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'Creator', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'Date', 'DateIndex', catalog='schedule_catalog')
    add_index(site, 'Subject', 'KeywordIndex', catalog='schedule_catalog')
    add_index(site, 'allowedRolesAndUsers', 'KeywordIndex', catalog='schedule_catalog')
    add_index(site, 'created', 'DateIndex', catalog='schedule_catalog')
    add_index(site, 'effective', 'DateIndex', catalog='schedule_catalog')
    add_index(site, 'expires', 'DateIndex', catalog='schedule_catalog')
    add_index(site, 'getId', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'in_reply_to', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'meta_type', 'FieldIndex', catalog='schedule_catalog')
    add_index(site, 'listCreators', 'KeywordIndex', catalog='schedule_catalog')
    add_index(site, 'portal_type', 'FieldIndex', catalog='schedule_catalog')
    
    ids = ['getPatientInfo', 'getReason', 'appointmentOrActivity',
            'getTypeOfLocationValue', 'UID', 'start', 'end',
            'getContactPhone', 'getRoomNumber', 'getDuration',
            'getLocationTitle', 'getSocialSecurity', 'getChart', 'getDoctor', 'Type',
            'CreationDate', 'Creator', 'Date', 'Description','EffectiveDate', 
            'ExpirationDate', 'ModificationDate', 'Subject', 'Title', 'getIcon', 'getId',
            'listCreators', 'modified', 'portal_type', 'created', 'effective', 'expires', 'review_state', ]
    create_metadatas(site, ids, catalog='schedule_catalog')
    
#===========================================================================
# Adiciona indices ao portal catalog e uid catalog
# Peter
#===========================================================================
def addOtherIndex(site):
    
    # TODO: Verificar a real necessidade dessas metadados, já que a quantidade
    # de metadados em um catalog impacta a velocidade do msm. (Luiz)
    ids = ['getPatientInfo', 'getReason', 'appointmentOrActivity',
           'getTypeOfLocationValue', 'UID']
    create_metadatas(site, ids)
    
    add_index(site, 'LTitle', 'FieldIndex',
              extra={'indexed_attrs': 'lower_title'})
    add_index(site, 'getProviderId', 'FieldIndex')
    add_index(site, 'idIncoherent', 'FieldIndex')
    add_index(site, 'getParsedLastName', 'ZCTextIndex',
              extra={'lexicon_id': 'plone_lexicon',
                     'doc_attr': 'getParsedLastName',
                     'index_type': 'Okapi BM25 Rank',
                     }
              )
    add_index(site, 'getDate_of_visit', 'DateIndex')
    add_index(site, 'getRouted_to', 'FieldIndex')
    add_index(site, 'getRouted_by', 'FieldIndex')
    add_index(site, 'getWorkflowStatus', 'FieldIndex')
    add_index(site, 'getStatus', 'FieldIndex')
    add_index(site, 'UID', 'FieldIndex', catalog='portal_catalog')
    add_index(site, 'getCode', 'FieldIndex', catalog='portal_catalog')
    add_index(site, 'getCodeType', 'FieldIndex', catalog='portal_catalog')
    
    add_index(site, 'getProfessional', 'FieldIndex',
          extra={'indexed_attrs': 'getProfessional'},
          catalog='uid_catalog')    

# o que isso esta fazendo?
def changePortalObjectsConfiguration(portal):

    # doctor_presentation as the default view
    portal.setDefaultPage(None)
    portal.setLayout('doctor_presentation')

    portal_membership = getToolByName(portal, 'portal_membership')
    #don't create a member folder
    portal_membership.memberareaCreationFlag = 1
    portal_memberdata = getToolByName(portal, 'portal_memberdata')
    portal_memberdata.manage_addProperty('home_url', './', 'string')
    portal_memberdata.manage_addProperty('related_object', '', 'string')
    portal_types = getToolByName(portal, 'portal_types')
    #Allow main types to be created in the portal root
    portal_types['Plone Site'].filter_content_types = True
    portal_types['Plone Site'].allowed_content_types = ['Document', 'File', 'Folder',
                                                        'Image', 'Link', 'Event', 'News Item', 'Topic',]

#===========================================================================
# Muda a lingua padrao do portal
# Peter
#===========================================================================
def changePortalLanguage(portal):
        portal.portal_languages.setDefaultLanguage('pt-br')
        
#===========================================================================
# Carrega o CID no Vocabulario do portal
# Peter
#===========================================================================
def loadCIDVocabulary(portal, context):
    print "Carregando CID do arquivo CID.txt ..."
    vt = getToolByName(portal, 'vocabulary_tool')
    CID_desc = context.readDataFile('../../CID_desc.txt')
    CID_code = context.readDataFile('../../CID_code.txt')
    print "Inserindo CID no Portal ..."
    vt.add_vocab('CID_desc', CID_desc)
    vt.add_vocab('CID_code', CID_code)


#===========================================================================
# Carrega o vocabulario de tipos insurance.
# Matheus
#===========================================================================
def loadInsuranceVocabulary(portal):
    vt = getToolByName(portal, 'vocabulary_tool')
    insurance = []
    insurance.append('particular')
    insurance.append('unimed')
    insurance.append('bradesco saude')
    vt.add_vocab('insurance', insurance)

#===========================================================================
# Carrega o vocabulario de tipos de documentos.
# Luiz
#===========================================================================
def loadDocumentTypesVocabulary(portal):
    vt = getToolByName(portal, 'vocabulary_tool')
    document_types = []
    document_types.append('primeira consulta')
    document_types.append('consulta')
    document_types.append('retorno')
    vt.add_vocab('document_types', document_types)

def loadImpressoTypesVocaburary(portal):
    ''' Carrega o vocabulario de tipo de impressos '''
    vt = getToolByName(portal, 'vocabulary_tool')
    types = []
    types.append('atestado')
    types.append('laudo')
    types.append('licença')
    types.append('pedido de exame')
    vt.add_vocab('impresso_types', types)

#===========================================================================
# Carrega o vocabulario de tipos e da razão das visitas.
# Luiz
#===========================================================================
def loadVisitVocabularies(portal):
    vt = getToolByName(portal, 'vocabulary_tool')
    visit_types = []
    visit_types.append('1a consulta')
    visit_types.append('consulta')
    visit_types.append('retorno')
    vt.add_vocab('visit_types', visit_types)   

    visit_reason = []
    visit_reason.append('acompanhamento')
    visit_reason.append('check up')
    vt.add_vocab('visit_reason', visit_reason)       


def loadDEFVocabulary(portal,context):
    #Dicionario de especialidades farmaceuticas
    vt = getToolByName(portal, 'vocabulary_tool')
    print "Carregando DEF do arquivo DEF.txt ..."
    DEF = context.readDataFile("../../DEF.txt")
    print "Inserindo DEF no Portal ..."
    vt.add_vocab('DEF', DEF)
	
def mailHostConfiguration(portal):
    '''Configura servidor de email (mesmos campos de Configuracao do Site -> E-mail)'''
    mail_host = portal.MailHost
    mail_host.smtp_host = 'localhost'
    mail_host.smtp_port = 25
    portal.email_from_name = 'Equipe de Desenvolvimento/Suporte'
    portal.email_from_address = 'desenvolvimento@communi.com.br'

def addUpgradeExternalMethods(portal):
    '''
    add upgrade external methods in site root.
    '''
    from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
    manage_addExternalMethod(portal, '0_upgrade', 'Upgrade (Export/Import) Cmed', 'wres.policy.upgrade', 'main')
    manage_addExternalMethod(portal, 'z_export', 'Export Cmed', 'wres.policy.exporter', 'main')
    manage_addExternalMethod(portal, 'z_import', 'Import Cmed', 'wres.policy.importer', 'main')


def createCmedCatalogs(portal):
    cct = getToolByName(portal, 'cmed_catalog_tool')
    from repoze.catalog.indexes.text import CatalogTextIndex
    from repoze.catalog.indexes.field import CatalogFieldIndex

    # event catalog
    event_catalog = cct.add_catalog('event_catalog')
    event_catalog['event_text'] = CatalogTextIndex('event_text')
    event_catalog['date'] = CatalogFieldIndex('date')
    event_catalog['date_year'] = CatalogFieldIndex('date_year')
    event_catalog['date_month'] = CatalogFieldIndex('date_month')
    event_catalog['date_day'] = CatalogFieldIndex('date_day')
    event_catalog['path'] = CatalogFieldIndex('path')
    event_catalog['event_type'] = CatalogFieldIndex('event_type')
    event_catalog['meta_type'] = CatalogFieldIndex('meta_type')
    event_catalog['related_object_id'] = CatalogFieldIndex('related_object_id')

def addExampleTemplate(portal):
    document_template = '<table class="plain"><tbody><tr><th colspan="2">QUEIXA E DURAÇÃO</th></tr><tr><td><br />\
    <br /></td></tr></tbody></table><table class="plain"><tbody><tr><th colspan="2">HISTÓRIA DA MOLÉSTIA ATUAL</th></tr><tr><td><br />\
    <br /></td></tr></tbody></table><table class="plain"><tbody><tr><th colspan="2">ANTECEDENTES PESSOAIS</th></tr><tr><td><br /><br />\
    </td></tr></tbody></table><table class="plain"><tbody><tr><th colspan="2">ANTECEDENTES PESSOAIS</th></tr><tr><td><br /><br /><br />\
    </td></tr></tbody></table><table class="plain"><tbody><tr><th>Hábitos</th> <th>Frequência</th></tr><tr><td>Tabagismo    (   )\
    </td><td><br /></td></tr><tr><td>Atividade Física (   )</td><td><br /></td></tr><tr><td>Etilismo (  )</td><td></td>\
    </tr><tr><td colspan="2">Alimentação:</td></tr><tr><td colspan="2">Sexuais:</td></tr></tbody></table><table class="plain">\
    <tbody><tr><th colspan="2">ANTENCENDENTES FAMILIARES</th></tr><tr><td>Doenças Cardiovasculares (  )</td><td>Diabetes ( )</td>\
    </tr><tr><td>Hipertenção Arterial (  )</td><td>Tuberculose ( )</td></tr><tr><th colspan="2"><strong>Participação familiar\
     na gênese do quadro atual</strong></th></tr><tr><td colspan="2" rowspan="3"><br /><br /></td></tr></tbody></table>\
     <table class="plain"><tbody><tr><th colspan="2">HISTÓRIA SOCIAL</th></tr><tr><td colspan="2"><br /><br /></td></tr></tbody>\
     </table><table class="plain"><tbody><tr><th colspan="2">REVISÃO DOS SISTEMAS</th></tr><tr><th>Geral (Febre, alterações\
      de peso, alteração no dinamismo)</th></tr><tr><td colspan="2"><br /><br /></td></tr><tr><th>Cabeça (Cefaléia, tontura)\
      </th></tr><tr><td colspan="2"><br /><br /></td></tr><tr><th>Cabeça (Cefaléia, tontura)</th></tr><tr><td colspan="2">\
      <br /><br /></td></tr><tr><th>Olhos(Acuidade visual, dor, campo visual)</th></tr><tr><td colspan="2"><br /><br /></td>\
      </tr><tr><th>Ouvido(Acuidade auditiva, zumbido, vertigem)</th></tr><tr><td colspan="2"><br /><br /></td></tr><tr>\
      <th>Nariz, garganta, boca( epistaxe, IVAS freqüentes, obstrução, dor de garganta freqüente, sinusite)</th></tr><tr>\
      <td colspan="2"><br /><br /></td></tr><tr><th>Tórax( Tosse, expectoração, dor, dispnéia, hemoptise, edemas, palpapitação)\
      </th></tr><tr><td colspan="2"><br /><br /></td></tr><tr><th>Gastrointestinal(Disfagia, azia, pirose, hábito intestinal,\
       sangramento, puxo, tenesmo, dia gástrico)</th></tr><tr><td colspan="2"><br /><br /></td></tr><tr><th>Gênito-urinário(Disúria,\
        poliúria, nictúria, nódulos de mama, Papanicolaou, mamografia)</th></tr><tr><td colspan="2"><br /><br /></td></tr><tr><th>\
        Pele e fâneros(Manchas, alopecia)</th></tr><tr><td colspan="2"><br /><br /></td></tr></tbody></table><table class="plain">\
        <tbody><tr><th colspan="2">EXAME FÍSICO</th></tr><tr><th colspan="2">Estado Nutricional</th></tr><tr><td>Caquético (  )</td>\
        <td>Emagrecido (  )</td></tr><tr><td>Obeso (  )</td><td>Descorado (  )</td></tr><tr><td>Desidratado (  )</td><td>Acianótico (  )\
        </td></tr><tr><td>Anictérico (  )</td><td>Febril (  )</td></tr><tr><td colspan="2">Outro:</td></tr><tr><th colspan="2">\
        Parâmetros vitais</th></tr><tr><td>PA(Pressão arterial)</td><td></td></tr><tr><td>FC(Freqüência cardíaca)</td><td></td>\
        </tr><tr><td>FR(Freqüência respiratória)</td><td></td></tr><tr><td>T(Temperatura)</td><td></td></tr><tr><td>Peso(Kg)</td>\
        <td></td></tr><tr><td>Altura(m)</td><td></td></tr><tr><td>Outros:</td><td></td></tr></tbody></table><table class="plain">\
        <tbody><tr><th colspan="2">HIPÓTESE DIAGNÓSTICA</th></tr><tr><td><br /><br /><br /></td></tr></tbody></table><table \
        class="plain"><tbody><tr><th colspan="2">CONDUTA E DISCUSSÃO</th></tr><tr><th colspan="2">Medicamentos</th></tr><tr><td>\
        <br /><br /></td></tr><tr><th colspan="2">Recomendações</th></tr><tr><td><br /><br /></td></tr></tbody></table>\
        <table class="plain"><tbody><tr><th colspan="2">DETALHES DE RETORNO</th></tr><tr><td>Data de Retorno:</td><td></td></tr>\
        <tr><th colspan="2">Observações para retorno:</th></tr><tr><td colspan="2"><br \><br \></td></tr></tbody></table>'
    import random
    print '*** Criando objeto Template...'
    templates = getattr(portal, "Templates")
    new_id = "Modelo-"+str(random.randint(0, 9999))
    consulta = getOrCreateType(portal, templates.Consultas, new_id, "Template")
    consulta.setTemplate_body(document_template)
    consulta.setTitle("[Exemplo]Primeira Consulta")
    consulta.reindexObject()
    
def parseFirstDoctorInputFile(infile):
    lines = infile.readlines()
    if len(lines) < 2:
        return None
    dic = {}
    for i in range(len(lines)):
        if i % 2 == 0:
            lines[i] = lines[i].replace('\n', '')
            lines[i+1] = lines[i+1].replace('\n', '')
            dic[lines[i]] = lines[i+1]
    return dic

def setupVarious(context):
    """ Funcao generica executada na instalacao do wres policy """


    # if context.readDataFile('wres.policy_various.txt') is None:
    #     return
    portal = getSite()

    # TODO:gambiarra (luiz)
    # a funcao setupVarious eh chamada varias vezes (toda vez que uma produto eh instalado),
    # mas ela deve ser executada apenas uma vez, que eh quando a expressao:
    # "context.readDataFile('wres.policy_various.txt') is not None" retorna True.
    # Por algum motivo a ordem de execucao esta errada no Plone 4.1.4, ocasionando erro.
    # a gambiarra feita aqui eh pra contornar isso. A maneira correta seria ter apenas o if
    # com a expressao "context.readDataFile ...".


    if context.readDataFile('wres.policy_various.txt') is not None:
        print '********************************ACHEI O TXT***********************************'   
        # read firstdoctor_info and create a doctor if there is information there.
        infile = context.openDataFile('firstdoctor_info.txt')
        doctor_info = parseFirstDoctorInputFile(infile)
        full_name = doctor_info['Nome Completo'].split(' ')
        firstname = full_name[0].lower(); lastname = full_name[-1].lower()
        doctor_id = firstname[0] + lastname

        if doctor_info is not None:
            doctor_folder = getattr(portal, 'Doctors')
            clinic = getattr(portal, 'Clinic')
            if not int(doctor_info['Quero o meu site profissional']):
                # removing permissions from anonymous, so he cant see initial page anymore.
                doctor_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE], acquire = False)
                clinic.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE, ANONYMOUS_ROLE], acquire = False)
                doctor_folder.reindexObject()
            doctor = getOrCreateType(portal, doctor_folder, doctor_id, 'Doctor')
            doctor.fillFirstDoctorInfo(doctor_info)
            clinic.fillClinicInformation(doctor_info)
            doctor.reindexObject()
            clinic.reindexObject()

        loadDocumentTypesVocabulary(portal)
        loadImpressoTypesVocaburary(portal)
        loadVisitVocabularies(portal)
        loadCIDVocabulary(portal, context)
        loadDEFVocabulary(portal,context)        
        loadInsuranceVocabulary(portal)

        createCmedCatalogs(portal)

    if not portal.portal_types.getTypeInfo('Visit'):
        print '********************************AINDA NÃO***********************************'
        return

    try:
        getattr(portal, 'Patients')
    except:

        deleteDefaultObjects(portal)
        
        #portal.setDefaultPage('Appointments')
        createVisitFolder(portal)
        createClinic(portal)
        createAdminFolder(portal)    
        createTemplateFolder(portal)
        createDoctorFolder(portal)
        createContactPage(portal)
        #TODO:Remover posteriormente
        #createInsuranceFolder(portal)
        #createTop10DefaultInsurance(portal)
        
        createPatientFolder(portal)
        createSecretaryFolder(portal)
        
        # conforme decidido na reuniao 21-10-2011 os medicos indicantes
        # serao removidos, fica aqui comentado caso decida-se voltar atras.
        # Os transcritores serao mantidos apenas na versao paga do CMed.
        # createReferringProviderFolder(portal)
        # createTranscriptionistFolder(portal)
        
        #createScheduleCatalog(portal)
        
        #addOtherIndex(portal)
        
        changePortalLanguage(portal)
        changePortalObjectsConfiguration(portal)
        mailHostConfiguration(portal)
        addUpgradeExternalMethods(portal)
        addExampleTemplate(portal)
        createGroups(portal)
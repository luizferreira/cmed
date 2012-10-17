# coding=utf-8

import os

from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
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
    template_folder.setLayout('templates_summary_view')
    template_folder.reindexObject()
    print '*** Criando pasta de templates...... OK'

def createAjudaFolder(portal):
    """ Create the Ajuda folder """
    print '*** Criando pasta de ajuda...'
    ajuda_folder = getOrCreateType(portal, portal, 'Ajuda', 'Folder')

    # a permissao Modify portal content eh necessaria pra se poder adicionar objetos dentro da pasta.
    ajuda_folder.manage_permission('Modify portal content', [MANAGER_ROLE], acquire=False)
    ajuda_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE], acquire=False)
    ajuda_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE], acquire=False)
    # adds
    ajuda_folder.manage_permission('ATContentTypes: Add File', [], acquire=False)
    ajuda_folder.manage_permission('Add portal topics', [], acquire=False)
    ajuda_folder.manage_permission('ATContentTypes: Add Event', [], acquire=False)
    ajuda_folder.manage_permission('ATContentTypes: Add Image', [], acquire=False)
    ajuda_folder.manage_permission('ATContentTypes: Add Link', [], acquire=False)
    ajuda_folder.manage_permission('ATContentTypes: Add News Item', [], acquire=False)
    ajuda_folder.manage_permission('ATContentTypes: Add Folder', [], acquire=False)
    ajuda_folder.manage_permission('ATContentTypes: Add Document', [], acquire=False)
    ajuda_folder.manage_permission('ATContentTypes: Add File', [], acquire=False)
    ajuda_folder.setTitle('Ajuda')
    ajuda_folder.setExcludeFromNav(True)
    ajuda_folder.setLayout('ajuda_view')
    ajuda_folder.reindexObject()
    print '*** Criando pasta de ajuda...... OK'

def createDoctorFolder(portal):
    """ Cria a pasta de medicos """
    print '*** Criando pasta de medicos...'
    doctor_folder = getOrCreateType(portal, portal, 'Doctors', 'DoctorFolder')
    doctor_folder.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE], acquire = False)
    # its important that Anonymous have 'Acess cont..' permission, so he can call the method list_doctors.
    doctor_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE, ANONYMOUS_ROLE], acquire = False)
    doctor_folder.setTitle('Médicos')
    doctor_folder.setExcludeFromNav(True)
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
    secretary_folder.setExcludeFromNav(True)
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

def changePortalLanguage(portal):
    '''
    Change portal default language.
    '''
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
    manage_addExternalMethod(portal, '0_generic_upgrade', 'Manual Upgrade Cmed', 'wres.policy.generic_upgrade', 'main')
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
    <br /></td></tr></tbody></table><table class="plain"><tbody><tr><th colspan="2">ANTECEDENTES PESSOAIS</th></tr><tr><td><br /><br /><br />\
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
    # if communimed site register form changes, this list will probably have to be updated.
    keys = ['Nome Completo', 'CRM', 'Telefone de Contato', 'Seu endereço de e-mail', 'Confirmação do e-mail', 'Especialidade 1', 'Especialidade 2', 'Quero o meu site profissional', 'Nome da Clínica/Consultório', 'Avenida/Rua', 'Número', 'Complemento', 'Cidade', 'Estado', 'Telefone', 'E-mail', 'Como nos conheceu?']
    for key in keys:
        dic[key] = None

    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
        if lines[i] in dic.keys():
            try:
                # remove \n from next line.
                lines[i+1] = lines[i+1].replace('\n', '')
                # maybe the next line is a form label (in case the current label was left blank)
                if lines[i+1] in dic.keys():
                    continue
                else:
                    dic[lines[i]] = lines[i+1]
            except IndexError:
                # the IndexError indicates that the list is over, nothing to do here.
                pass
    return dic

def createFirstDoctor(portal, context):
    '''
    if there is a doctor in firstdoctor_info.txt, then this functino creates that doctor.
    '''
    from wres.policy.utils.utils import create_base_of_id
    # read firstdoctor_info and create a doctor if there is information there.
    infile = context.openDataFile('firstdoctor_info.txt')
    doctor_info = parseFirstDoctorInputFile(infile)
    full_name = doctor_info['Nome Completo'].split(' ')
    firstname = full_name[0].lower(); lastname = full_name[-1].lower()
    doctor_id = create_base_of_id(firstname, lastname)

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

        createFirstDoctor(portal, context)
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

        createPatientFolder(portal)
        createSecretaryFolder(portal)
        createAjudaFolder(portal)

        # conforme decidido na reuniao 21-10-2011 os medicos indicantes
        # serao removidos, fica aqui comentado caso decida-se voltar atras.
        # Os transcritores serao mantidos apenas na versao paga do CMed.
        # createReferringProviderFolder(portal)
        # createTranscriptionistFolder(portal)

        changePortalLanguage(portal)
        changePortalObjectsConfiguration(portal)
        mailHostConfiguration(portal)
        addUpgradeExternalMethods(portal)
        addExampleTemplate(portal)
        createGroups(portal)


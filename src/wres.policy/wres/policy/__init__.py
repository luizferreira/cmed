from Products.CMFCore.utils import ToolInit
from Products.CMFCore.permissions import setDefaultRoles

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    
    setDefaultRoles('Add Content', ('Manager', 'Doctor', 'Secretary', 'Transcriptionist', 'UemrAdmin' ))
    setDefaultRoles('Create User', ('Manager', 'UemrAdmin'))
    setDefaultRoles('Edit Doc', ('Doctor', 'Manager', 'Secretary', 'Transcriptionist', 'UemrAdmin' ))
    setDefaultRoles('Edit Doctor', ('Doctor', 'Manager', 'UemrAdmin'))
    setDefaultRoles('Edit Insurance', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'UemrAdmin' ))
    setDefaultRoles('Edit Patient', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'Transcriptionist', 'UemrAdmin', 'Patient' ))
    setDefaultRoles('Edit Secretary', ('Doctor', 'Manager', 'Secretary', 'UemrAdmin'))
    setDefaultRoles('Edit Visit', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary'))
    setDefaultRoles('List Patient', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'Transcriptionist', 'UemrAdmin', 'Patient' ))
    setDefaultRoles('List Secretary', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'Transcriptionist', 'UemrAdmin' ))
    setDefaultRoles('List Visit', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'Transcriptionist', 'UemrAdmin' ))
    setDefaultRoles('Set Schedule', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'UemrAdmin' ))
    setDefaultRoles('Sign Progress Notes', ('Doctor', 'FrontDeskTwo', 'Manager', 'Patient', 'Secretary', 'Transcriptionist', 'UemrAdmin' ))
    setDefaultRoles('View Doctor', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'Transcriptionist', 'UemrAdmin' ))
    setDefaultRoles('View Insurance', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'Transcriptionist', 'UemrAdmin' ))
    setDefaultRoles('View Patient', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'Transcriptionist', 'UemrAdmin', 'Patient' ))
    setDefaultRoles('View Schedule', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'Transcriptionist', 'UemrAdmin' ))
    setDefaultRoles('View Secretary', ('Doctor', 'FrontDeskTwo', 'Manager', 'Secretary', 'UemrAdmin', 'Transcriptionist' ))
    setDefaultRoles('View Visit', ('Doctor', 'Manager', 'Owner', 'Secretary', 'Transcriptionist' ))
    
    # Adicao de archetypes
    setDefaultRoles('Add WRESUser', ('Manager', 'Contributor', 'UemrAdmin'))
    setDefaultRoles('Add TranscriptionistFolder', ('Manager', 'Contributor', 'UemrAdmin'))
    setDefaultRoles('Add Transcriptionist', ('Manager', 'Contributor', 'UemrAdmin'))
    setDefaultRoles('Add SecretaryFolder', ('Manager', 'Contributor', 'UemrAdmin'))
    setDefaultRoles('Add Secretary', ('Manager', 'Contributor', 'UemrAdmin'))
    setDefaultRoles('Add Patient', ('Manager', 'Contributor', 'UemrAdmin'))
    setDefaultRoles('Add Doctor', ('Manager', 'Contributor', 'UemrAdmin'))
    setDefaultRoles('Add PatientFolder', ('Manager', 'Contributor', 'UemrAdmin'))
    setDefaultRoles('Add Patient', ('Manager', 'Contributor', 'UemrAdmin'))
    setDefaultRoles('Add DoctorFolder', ('Manager', 'Contributor', 'UemrAdmin'))
    setDefaultRoles('Add Doctor', ('Manager', 'Contributor', 'UemrAdmin'))
    
    allow_modules()
    
    init_tools(context)
    
def allow_modules():
    from AccessControl import ModuleSecurityInfo, ClassSecurityInfo
    from AccessControl import allow_module, allow_class, allow_type
    
    #copied from Products.PythonScript.module_access_examples.py
    ModuleSecurityInfo('re').declarePublic('compile', 'findall',
                                           'match', 'search', 'split', 'sub', 'subn', 'error',
                                           'I', 'L', 'M', 'S', 'X')
    import re
    allow_type(type(re.compile('')))
    allow_type(type(re.match('x','x')))
    
    import copy
	ModuleSecurityInfo('copy').declarePublic('deepcopy')


    """ Modulo Archetypes """
    ModuleSecurityInfo('wres').declarePublic('archetypes')
    ModuleSecurityInfo('wres.archetypes').declarePublic('content')
    
    ModuleSecurityInfo('wres.archetypes.content').declarePublic('patient')
    allow_module('wres.archetypes.content.patient')
    
    ModuleSecurityInfo('wres.archetypes.content').declarePublic('doctor')
    allow_module('wres.archetypes.content.doctor')
    
    ModuleSecurityInfo('wres.archetypes.content').declarePublic('documentfolder')
    allow_module('wres.archeytpes.content.documentfolder')
    
    ModuleSecurityInfo('wres.archetypes.content').declarePublic('secretarydesktop')
    allow_module('wres.archeytpes.content.secretarydesktop')
    from wres.archetypes.content.secretarydesktop import SecretaryDesktopData
    allow_class(SecretaryDesktopData)   
    
    """ Modulo Policy """
    ModuleSecurityInfo('wres').declarePublic('policy')
    ModuleSecurityInfo('wres.policy').declarePublic('utils')
    ModuleSecurityInfo('wres.policy.utils').declarePublic('utils')
    
    allow_module('wres.policy.utils.utils')
    
    """ Modulo Theme """    
    ModuleSecurityInfo('wres').declarePublic('theme')    
    ModuleSecurityInfo('wres.theme').declarePublic('skins')    
    ModuleSecurityInfo('wres.theme.skins').declarePublic('wres_theme_custom_scripts')
    ModuleSecurityInfo('wres.theme.skins').declarePublic('wres_theme_custom_templates')
    ModuleSecurityInfo('wres.theme.skins').declarePublic('wres_theme_custom_images')
    ModuleSecurityInfo('wres.theme.skins').declarePublic('wres_theme_auxiliary')
    ModuleSecurityInfo('wres.theme.skins').declarePublic('wres_theme_widgets')
    ModuleSecurityInfo('wres.theme.skins').declarePublic('wres_theme_custom_styles')
    
def init_tools(context):
    from wres.policy.VocabularyTool import VocabularyTool

    tool_initializer = ToolInit('Vocabulary Tool', tools=(VocabularyTool,), icon='tool.gif')
    tool_initializer.initialize(context)
    

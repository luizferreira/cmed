## coding=utf-8

def reinstall_catalog(context):
    """
    Reinstala o catalogo (foi adicionado a coluna de metadado getProviderId)
    """    
    default_profile = "profile-wres.policy:default"
    context.runImportStepFromProfile(default_profile, 'catalog')




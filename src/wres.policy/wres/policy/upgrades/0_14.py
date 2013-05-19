# coding=utf-8

def chart_system_id_update(context):
    print "Preenchendo o campo chartSystemID nos pacientes antigos"

    patient_folder = context.Patients
    patient_folder.setLastChartSystemID(0)
    
    catalog = context.portal_catalog
    query = dict(meta_type="Patient", sort_on="created")
    brains = catalog.searchResults(query)
    for b in brains:
        print b.getPath()
        obj = b.getObject()
        nextChartSystemID = patient_folder.getLastChartSystemID() + 1
        obj.setChartSystemID(nextChartSystemID)
        patient_folder.setLastChartSystemID(nextChartSystemID)        
        obj.reindexObject()
    
    patient_folder.reindexObject()

    print "..."
    print "Pronto!\n"

def assign_permission(context):
    print "Médicos precisam ter 'Delete Objects' em 'Modelos'"

    template_folder = context.Templates
    template_folder.manage_permission("Delete objects", ["Doctor", "Manage"], acquire=False)
    template_folder.reindexObject()

    print "..."
    print "Pronto!\n"

def assign_permission2(context):
    print "Médicos precisam ter 'Delete Objects' em 'Arquivos Externos'"

    catalog = context.portal_catalog
    query = dict(meta_type="UploadChartFolder")
    brains = catalog.searchResults(query)
    for b in brains:
        print b.getPath()
        obj = b.getObject()
        obj.manage_permission('Delete objects', ["Doctor", "Manager"], acquire=False)
        obj.reindexObject()
        
    print "..."
    print "Pronto!\n"

def reinstall_wres(context):
    """
    Reinstala os produtos do Wres.
    """
    print "Reinstalando os produtos do CommuniMed..."

    qit = context.portal_quickinstaller

    to_uninstall = ["wres.policy", "wres.archetypes", "wres.theme", "wres.tour", "wres.brfields"]

    qit.uninstallProducts(products=to_uninstall)

    installed = [ x['id'] for x in qit.listInstalledProducts() ]

    for product in to_uninstall:
        if product in installed:
            Exception("Some product could not be uninstalled properly.")

    qit.installProduct("wres.policy")

    for product in to_uninstall:
        if product not in installed:
            Exception("Some product could not be installed properly.")

    # # installs wres.policy
    # ids = [ x['id'] for x in qit.listInstallableProducts(skipInstalled=1) ]
    # for product in products:
    #     if product in ids:
    #         qit.installProduct(product)

    # context.runImportStepFromProfile(default_profile, 'actions')
    # context.runImportStepFromProfile(default_profile, 'caching_policy_mgr')
    # context.runImportStepFromProfile(default_profile, 'catalog')
    # context.runImportStepFromProfile(default_profile, 'componentregistry')
    # context.runImportStepFromProfile(default_profile, 'content_type_registry')
    # context.runImportStepFromProfile(default_profile, 'cookie_authentication')
    # context.runImportStepFromProfile(default_profile, 'mailhost')
    # context.runImportStepFromProfile(default_profile, 'properties')
    # context.runImportStepFromProfile(default_profile, 'rolemap')
    # context.runImportStepFromProfile(default_profile, 'skins')
    # context.runImportStepFromProfile(default_profile, 'toolset')
    # context.runImportStepFromProfile(default_profile, 'typeinfo')
    # context.runImportStepFromProfile(default_profile, 'various')
    # context.runImportStepFromProfile(default_profile, 'workflow')
    print "..."
    print "Pronto!\n"

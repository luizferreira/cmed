## coding=utf-8

def reinstall_wres(context):
    """
    Reinstala os produtos do Wres. O wres.policy não é reinstalado totalmente,
    apenas alguns importSteps são executados, fazemos isso porque alguns iS
    causam efeitos colaterais, leia os comentários abaixo para entender melhor.
    """
    print "Reinstalando os produtos do CommuniMed..."

    # não podemos simplesmente reinstalar o produto wres.policy (como é feito
    # com os outros componentes, mais abaixo), uma vez que isso faria com que
    # todos os importSteps fossem executados. Não queremos que todos os
    # importSteps sejam executados, o iS toolset, por exemplo, reseta o
    # VocabularyTool das instâncias.

    default_profile = "profile-wres.policy:default"

    context.runImportStepFromProfile(default_profile, 'actions')
    context.runImportStepFromProfile(default_profile, 'caching_policy_mgr')
    context.runImportStepFromProfile(default_profile, 'catalog')
    context.runImportStepFromProfile(default_profile, 'componentregistry')
    context.runImportStepFromProfile(default_profile, 'content_type_registry')
    context.runImportStepFromProfile(default_profile, 'cookie_authentication')
    context.runImportStepFromProfile(default_profile, 'mailhost')
    context.runImportStepFromProfile(default_profile, 'properties')
    context.runImportStepFromProfile(default_profile, 'portlets')
    context.runImportStepFromProfile(default_profile, 'rolemap')
    context.runImportStepFromProfile(default_profile, 'skins')

    # o importStep toolset reseta todo o vocabulário. Ele deve ser usado apenas
    # caso cadastremos uma nova tool, e sob a pena de ter que migrar o
    # vocabulário das instâncias afetadas.
    # context.runImportStepFromProfile(default_profile, 'toolset')

    context.runImportStepFromProfile(default_profile, 'typeinfo')
    context.runImportStepFromProfile(default_profile, '_various')
    context.runImportStepFromProfile(default_profile, 'workflow')

    qit = context.portal_quickinstaller

    # reinstala os componentes do CommuniMed (exceto wres.policy).
    to_reinstall = ["wres.archetypes", "wres.theme", "wres.tour", "wres.brfields"]

    qit.uninstallProducts(products=to_reinstall)

    installed = [x['id'] for x in qit.listInstalledProducts()]

    for product in to_reinstall:
        if product in installed:
            Exception("Some product could not be uninstalled properly.")

    for product in to_reinstall:
        qit.installProduct(product)

    for product in to_reinstall:
        if product not in installed:
            Exception("Some product could not be installed properly.")

    # os novos índices declarados em catalog.xml não estarão indexados, uma vez
    # o iS catalog foi executado. Por isso, precisamos reconstruir o catálago.
    # Caso isso se mostre uma operação muito despendiosa, podemos comentar o iS
    # catalog e rodá-lo apenas em atualizações onde novos índices foram criados.
    print "Reconstruindo catalogo, isso pode demorar alguns minutos..."
    portal_catalog = context.portal_catalog
    portal_catalog.clearFindAndRebuild()

    print "..."
    print "Pronto!\n"

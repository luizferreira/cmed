def i18n_patch():
    '''
    Change 'Adicionar item...' to 'Adicionar...'This hardpatch workround
    was necessary, since plone.po in our packages is not overriding plone
    translations.
    '''
    from plone.app.contentmenu.menu import FactoriesSubMenuItem
    FactoriesSubMenuItem.title = 'Adicionar...'


def hard_patch():
    '''
    This function is called by the policy __init__.py. To your hard_patch
    to be called, you need to call it here.
    '''
    i18n_patch()

def i18n_patch():
    '''
    Change 'Adicionar item...' to 'Adicionar...'This hardpatch workround
    was necessary, since plone.po in our packages is not overriding plone
    translations.
    '''
    from plone.app.contentmenu.menu import FactoriesSubMenuItem
    FactoriesSubMenuItem.title = 'Adicionar...'

def plone_app_form_patch():
    '''
    plone.app.form has a dumb max date set to 1/1/2021 which was not allowing secretaries to add
    visits after 31/12/2020
    '''
    from DateTime.DateTime import DateTime                                          
    import plone.app.form.widgets.datecomponents                                    
    plone.app.form.widgets.datecomponents.PLONE_CEILING = DateTime(2500, 0) # 2499-12-31


def hard_patch():
    '''
    This function is called by the policy __init__.py. To your hard_patch
    to be called, you need to call it here.
    '''
    i18n_patch()
    plone_app_form_patch()

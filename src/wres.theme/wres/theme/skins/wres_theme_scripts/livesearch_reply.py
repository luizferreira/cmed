## Script (Python) "livescript_reply"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=q,limit=10,path=None
##title=Determine whether to show an id in an edit form

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.CMFPlone.utils import safe_unicode
from Products.PythonScripts.standard import url_quote
from Products.PythonScripts.standard import url_quote_plus
from Products.PythonScripts.standard import html_quote

# ATENCAO:
# este arquivo sofreu modificacoes da equipe CommuniMed. Para saber
# as mudancas e' so' comparar com o arquivo de mesmo nome no egg
# do Plone versao 4.0. As mudancas sao basicamente para adaptar
# o livesearch do Plone a pesquisa de pacientes do CommuniMed.
ploneUtils = getToolByName(context, 'plone_utils')
portal_url = getToolByName(context, 'portal_url')()
pretty_title_or_id = ploneUtils.pretty_title_or_id
plone_view = context.restrictedTraverse('@@plone')
portal_state = context.restrictedTraverse('@@plone_portal_state')

portalProperties = getToolByName(context, 'portal_properties')
siteProperties = getattr(portalProperties, 'site_properties', None)
useViewAction = []
if siteProperties is not None:
    useViewAction = siteProperties.getProperty('typesUseViewActionInListings', [])

# SIMPLE CONFIGURATION
USE_ICON = True
MAX_TITLE = 35
MAX_DESCRIPTION = 93

# generate a result set for the query
catalog = context.portal_catalog

friendly_types = ploneUtils.getUserFriendlyTypes()

def quotestring(s):
    return '"%s"' % s

def quote_bad_chars(s):
    bad_chars = ["(", ")"]
    for char in bad_chars:
        s = s.replace(char, quotestring(char))
    return s

# for now we just do a full search to prove a point, this is not the
# way to do this in the future, we'd use a in-memory probability based
# result set.
# convert queries to zctextindex

# XXX really if it contains + * ? or -
# it will not be right since the catalog ignores all non-word
# characters equally like
# so we don't even attept to make that right.
# But we strip these and these so that the catalog does
# not interpret them as metachars
# See http://dev.plone.org/plone/ticket/9422 for an explanation of '\u3000'
multispace = u'\u3000'.encode('utf-8')
for char in ('?', '-', '+', '*', multispace):
    q = q.replace(char, ' ')
r = q.split()
r = " AND ".join(r)
r = quote_bad_chars(r)+'*'
searchterms = url_quote_plus(r)

site_encoding = context.plone_utils.getSiteEncoding()
if path is None:
    path = getNavigationRoot(context)

# '*' no final do path indica que a busca esta sendo realizada para selecionar 
# um paciente para uma consulta.
selecting_patient_for_visit = False
if path[-1] == '*':
    path = path[0:-1]
    selecting_patient_for_visit = True
    limit = 20 # aumenta o limite de resultados na adição de visita

# no Cmed esta busca eh usada apenas para pacientes, e os inativos nao sao mostrados
pbrains = catalog(SearchableText=r, portal_type='Patient', review_state='active')

REQUEST = context.REQUEST
RESPONSE = REQUEST.RESPONSE
RESPONSE.setHeader('Content-Type', 'text/xml;charset=%s' % site_encoding)

# replace named entities with their numbered counterparts, in the xml the named ones are not correct
#   &darr;      --> &#8595;
#   &hellip;    --> &#8230;
legend_livesearch = _('legend_livesearch', default='LiveSearch &#8595;')
label_no_results_found = _('label_no_results_found', default='No matching results found.')
label_advanced_search = _('label_advanced_search', default='Advanced Search&#8230;')
label_show_all = _('label_show_all', default='Show all items')

ts = getToolByName(context, 'translation_service')

output = []

def verifyViewChartPermission():
    userRoles = context.portal_membership.getAuthenticatedMember().getRoles()
    roles = ['Transcriptionist','Manager','Doctor']
    for role in roles:
     if role in userRoles:
       return 1
    return 0

def write(s):
    output.append(safe_unicode(s))

if not pbrains:
    write('''<fieldset class="livesearchContainer cmedgray">''')
    write('''<legend id="livesearchLegend">%s</legend>''' % "Resultados")
    write('''<h2 id="results_title">%s</h2>''' % "Resultados")
    write('''<div class="LSIEFix">''')
    write('''<div id="LSNothingFound">%s</div>''' % ts.translate(label_no_results_found, context=REQUEST))
    write('''<div class="LSRow">''')
    write('''</div>''')
    write('''</div>''')
    write('''</fieldset>''')

else:
    write('''<fieldset class="livesearchContainer cmedgray">''')
    write('''<legend id="livesearchLegend">%s</legend>''' % "Resultados")
    write('''<h2 id="results_title">%s</h2>''' % "Resultados")
    write('''<div class="LSIEFix">''')
    write('''<ul class="LSTable">''')

    view_chart_permission = verifyViewChartPermission()

    # imprime a mensagem também no início dos resultados para garantir que será vista.
    if len(pbrains)>limit:
        write('''<li class="LSRow" style="width:425px;">''')
        # imprime uma mensagem quando há resultados que não foram mostrados por causa do limite
        write( '<span style="color:red; font-weight:normal;">Alguns resultados não foram exibidos, refina melhor a sua busca.</span>' )
        write('''</li>''')

    for patient in pbrains[:limit]:

        #get patient
        icon = plone_view.getIcon(patient)
        itemUrl = patient.getURL()
        if patient.portal_type in useViewAction:
            itemUrl += '/view'

        write('''<li class="LSRow" style="width:425px;">''')
        write(icon.html_tag() or '')
        full_title = safe_unicode(pretty_title_or_id(patient))
        if len(full_title) > MAX_TITLE:
            display_title = ''.join((full_title[:MAX_TITLE],'...'))
        else:
            display_title = full_title
        full_title = full_title.replace('"', '&quot;')
        klass = 'contenttype-%s' % ploneUtils.normalizeString(patient.portal_type)

        # tratamento especial para o tipo patient
        # o primeiro if se refere ao Procurar do adicionar consulta1
        # o elif se refere a pesquisa da pasta Patients
        dt = patient.genericColumn1
        cf = patient.genericColumn2
        formatted_phone = "%s %s-%s" % (cf[:2], cf[2:6], cf[6:10])
        if selecting_patient_for_visit:
            ppath = patient.getURL()
            if dt:
                write('''<a title="%s" class="%s" onClick="choosePatient('%s', '%s')">%s</a>''' % (full_title, klass, display_title, ppath, display_title))
            else:
                write('''<a title="%s" class="%s" onClick="choosePatient('%s', '%s')">%s</a>''' % (full_title, klass, display_title, ppath, display_title))
        else:
            # add the ID to the link to help amberjack
            patient_id_pessoal = patient.getId + "_pessoal"
            patient_id_prontuario = patient.getId + "_prontuario"
            pchart_url = patient.getURL()+'/initChart'

            if view_chart_permission:
                patient_url = patient.getURL()+'/initChart'
            else:
                patient_url = patient.getURL()+'/view'

            # escreve a linha referente ao paciente
            write('''<a href="%s" id="%s" title="%s" class="%s">%s</a>''' % (patient_url, patient_id_pessoal,full_title, klass, display_title))

        # a descricao do item mostra o telefone e a data de nascimento
        if dt == None:
            display_description = html_quote("(%s)" % (formatted_phone))
        else:
            display_description = html_quote("(%s * %s)" % (formatted_phone, dt.strftime("%d/%m/%Y")))

        write('''<span class="LSDescr">%s</span>''' % (display_description))
        write('''</li>''')
        full_title, display_title, display_description = None, None, None

    write('''<br />''')
    if len(pbrains)>limit:
        write('''<li class="LSRow" style="width:425px;">''')
        # imprime uma mensagem quando há resultados que não foram mostrados por causa do limite
        write( '<span style="color:red; font-weight:normal;">Alguns resultados não foram exibidos, refina melhor a sua busca.</span>' )
        write('''</li>''')
    write('''</ul>''')
    write('''</div>''')
    write('''</div>''')

return '\n'.join(output).encode(site_encoding)


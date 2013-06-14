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
MAX_TITLE = 29
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

# Este trecho faz com que funcione para o search do building blocks (visit)
if path[-1] == '*':
    building_search = True
    path = path[0:-1]
else:
    building_search = False

# transforming this in a 'only chart search' #cmed
# results = catalog(SearchableText=r, portal_type='Patient', path=path, sort_limit=limit)
results_aux = catalog(SearchableText=r, portal_type='Patient', path=path)
results = []
for result in results_aux:
    patient = result.getObject()
    if patient.getState_cmed() == 'inactive':
        continue
    results.append(patient)

# removing yellow highlight #cmed
# searchterm_query = '?searchterm=%s'%url_quote_plus(q)

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
    portal = context.portal_url.getPortalObject()
    userRoles = portal.portal_membership.getAuthenticatedMember().getRoles()
    roles = ['Transcriptionist','Manager','Doctor']
    verify = 0
    for role in roles:
     if role in userRoles:
       verify = 1
    return verify


def write(s):
    output.append(safe_unicode(s))

if not results:
    write('''<fieldset class="livesearchContainer cmedgray">''')
    write('''<legend id="livesearchLegend">%s</legend>''' % "Resultados")
    write('''<h2 id="results_title">%s</h2>''' % "Resultados")
    write('''<div class="LSIEFix">''')
    write('''<div id="LSNothingFound">%s</div>''' % ts.translate(label_no_results_found, context=REQUEST))
    # esse link foi colocado estaticamente na propria pagina.
    # if building_search:
    #     write('''<div><a class="link" onClick="createPatient()">Adicionar Novo Paciente</a></div>''')
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

    for patient in results[:limit]:
        #get patient
        icon = plone_view.getIcon(result)
        itemUrl = result.getURL()
        if result.portal_type in useViewAction:
            itemUrl += '/view'
        # removing yellow highlight #cmed
        # itemUrl = itemUrl + searchterm_query


        write('''<li class="LSRow" style="width:425px;">''')
        write(icon.html_tag() or '')
        full_title = safe_unicode(pretty_title_or_id(patient))
        if len(full_title) > MAX_TITLE:
            display_title = ''.join((full_title[:MAX_TITLE],'...'))
        else:
            display_title = full_title
        #import pdb; pdb.set_trace()
        full_title = full_title.replace('"', '&quot;')
        klass = 'contenttype-%s' % ploneUtils.normalizeString(result.portal_type)

        # tratamento especial para o tipo patient
        # o primeiro if se refere ao Procurar do adicionar consulta1
        # o elif se refere a pesquisa da pasta Patients
        if building_search:
            dt = patient.getBirthDate()
            cf = patient.getContactPhone()
            formatted_phone = "%s %s-%s" % (cf[:2], cf[2:6], cf[6:10])
            ppath = patient.absolute_url_path()
            if dt == None:
                write('''<a title="%s" class="%s" onClick="choosePatient('%s', '%s')">%s (%s)</a>''' % (full_title, klass, display_title, ppath, display_title, formatted_phone))
            else:
                write('''<a title="%s" class="%s" onClick="choosePatient('%s', '%s')">%s (%s * %s)</a>''' % (full_title, klass, display_title, ppath, display_title, formatted_phone, dt.strftime("%d/%m/%Y")))
        else:
            dt = patient.getBirthDate()
            cf = patient.getContactPhone()
            #Added the ID to the link to help amberjack
            patient_id_pessoal = patient.getId() + "_pessoal"
            patient_id_prontuario = patient.getId() + "_prontuario"
            formatted_phone = "%s %s-%s" % (cf[:2], cf[2:6], cf[6:10])
            pchart_url = patient.absolute_url()+'/initChart'

            if dt == None:
                display_text = "%s (%s)" % (display_title, formatted_phone )
            else:
                display_text = "%s (%s * %s)" % (display_title, formatted_phone, dt.strftime("%d/%m/%Y") )
            if verifyViewChartPermission():
                write('''<a href="%s" id="%s" title="%s" class="%s">%s</a>''' % (pchart_url, patient_id_pessoal,full_title, klass, display_text))
            else:
                write('''<a href="%s" id="%s" title="%s" class="%s">%s</a>''' % (itemUrl, patient_id_pessoal,full_title, klass, display_text))


        # only patients returned in search, so this doenst make sense anymore #cmed
        # else:
        #     write('''<a href="%s" title="%s" class="%s">%s</a>''' % (itemUrl, full_title, klass, display_title))
        display_description = safe_unicode(result.Description)
        if len(display_description) > MAX_DESCRIPTION:
            display_description = ''.join((display_description[:MAX_DESCRIPTION],'...'))
        # need to quote it, to avoid injection of html containing javascript and other evil stuff
        display_description = html_quote(display_description)
        write('''<div class="LSDescr">%s</div>''' % (display_description))
        write('''</li>''')
        full_title, display_title, display_description = None, None, None

    write('''<br />''')
    if len(results)>limit:
        # add a more... row
        write('''<li class="LSRow" style="width:425px;">''')
        # just print a message when the results explodes #cmed
        write( '<span style="font-weight:normal; font-size:80%">Alguns resultados não foram exibidos, refina melhor a sua busca.</span>' )
        # write( '<a href="%s" style="font-weight:normal">%s</a>' % ('search?SearchableText=' + searchterms, ts.translate(label_show_all, context=REQUEST)))
        write('''</li>''')
    write('''</ul>''')
    # este link foi colocado estaticamente na propria pagina.
    # if building_search:
    #     write('''<div><a class="link" onClick="createPatient()">Adicionar Novo Paciente</a></div>''')
    write('''</div>''')
    write('''</div>''')

return '\n'.join(output).encode(site_encoding)

